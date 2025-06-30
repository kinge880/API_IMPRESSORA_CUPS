from django.shortcuts import render
import os 
import subprocess
import shutil
import requests
from bs4 import BeautifulSoup
from rest_framework.response import Response 
from rest_framework.views import APIView 
from rest_framework import status, viewsets
from .serializers import FileUploadSerializer, ArquivoSerializer
from .models import Arquivo
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action 
from django.utils.decorators import method_decorator
from concurrent.futures import ThreadPoolExecutor
from django.conf import settings  
from django.http import JsonResponse

# Executar threads para manusear impressões simultâneas 
executor = ThreadPoolExecutor(max_workers=1024) # Configura o número máximo de impressões simultâneas

@method_decorator(csrf_exempt, name='dispatch') # Aplica csrf_exempt na classe inteira
class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        
        if serializer.is_valid():
            printer_name = serializer.validated_data['printer_name']
            uploaded_file = serializer.validated_data['file']
            
            if uploaded_file is None:
                return Response({"messages": "Nenhum arquivo foi enviado."}, status=status.HTTP_400_BAD_REQUEST)
            
            print(f"Recebido arquivo: {uploaded_file}")

            # Criação do diretório de upload
            temp_dir = 'temp_uploads'
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
                
            # Defina o caminho do arquivo após verificar que o arquivo foi recebido
            file_path = os.path.join(temp_dir, uploaded_file.name)
            print(f"Caminho do arquivo: {file_path}")
            
            try:
                # Escrevendo o arquivo no sistema
                with open(file_path, 'wb') as f:
                    for chunk in uploaded_file.chunks():
                        f.write(chunk)
                    print(f"Arquivo {file_path} salvo com sucesso.")
            except Exception as e:
                return Response({"messages": f"Erro ao salvar o arquivo: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Verifique se o arquivo existe no caminho
            if os.path.exists(file_path):
                print(f"Arquivo encontrado no caminho: {file_path}")
                try:
                    result = subprocess.run(['lp', '-d', printer_name, file_path], check=True, capture_output=True, text=True)
                    print(f"Arquivo {file_path} simulado para a impressão de {printer_name}")
                    return Response({"messages": "Arquivo salvo localmente e simulado para impressora com sucesso."}, status=status.HTTP_201_CREATED)
                except subprocess.CalledProcessError as e:
                    print(f"Erro ao simular a impressão: {e.stderr}")
                    return Response({"messages": f"Erro ao simular a impressão: {e.stderr}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except Exception as e:
                    print(f"Erro desconhecido ao simular a impressão: {str(e)}")
                    return Response({"messages": f"Erro desconhecido ao simular a impressão: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                print(f"Erro: arquivo {file_path} não encontrado.")
                return Response({"messages": f"Erro: arquivo {file_path} não encontrado."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Se o serializer não for válido
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PrinterListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            response = requests.get('http://172.16.23.19:631/printers/')
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            printers = []

            # Encontra todas as linhas da tabela de impressoras
            for row in soup.select('table.list tbody tr'):
                columns = row.find_all('td')
                if len(columns) >= 1:
                    printer_name = columns[0].text.strip()
                    printers.append(printer_name)
        except requests.exceptions.RequestException as e:
            # Captura a mensagem de erro mais detalhada
            return Response({"error": f"Não foi possível listar as impressoras: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # Captura outros erros
            return Response({"error": f"Erro desconhecido: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({"printers": printers})

class ArquivoViewSet(viewsets.ModelViewSet):
    queryset = Arquivo.objects.all()
    serializer_class = ArquivoSerializer
    
    def create(self, request, *args, **kwargs):
        # O arquivo será enviado no corpo da requisição
        arquivo = request.FILES.get('arquivo')
        
        if not arquivo:
            return Response({'detail': 'Arquivo não enviado'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Criação do objeto arquivo e salvando
        arquivo_obj = Arquivo(nome_arquivo=request.data.get('nome_arquivo'), arquivo=arquivo)
        arquivo_obj.save()
        
        return Response({'detail': 'Arquivo salvo com sucesso!'}, status=status.HTTP_201_CREATED)

class DeletedTempFilesView(APIView):
    def delete(self, request, *args, **kwargs):
        temp_uploads = 'temp_uploads' # Caminho da pasta de arquivos temporários
        
        # Verificar se a pasta existe
        if os.path.exists(temp_uploads):
            try:
                # Deleta todos os arquivos da pasta
                for file_name in os.listdir(temp_uploads):
                    file_path = os.path.join(temp_uploads, file_name)
                    if os.path.isfile(file_path):
                        os.remove(file_path) # Remove o arquivo
                        
                if not os.listdir(temp_uploads):
                    os.rmdir(temp_uploads)
                return Response({"message": "Arquivos temporários deletados com sucesso"}, status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response({"error": f"Erro ao tentar deletar arquivos: {str(e)}"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Pasta de arquivos temporários não encontrada"}, status=status.HTTP_404_NOT_FOUND)

class PrintersStatusViews(APIView):
    def get(self, request, printer_name, *args, **kwargs):
        try:
            response = requests.get(f'http://172.16.23.19:631/printers/{printer_name}')
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            printer_status = self.parse_printer_status(soup)
        except requests.exceptions.RequestException as e:
            # Captura a mensagem de erro mais detalhada
            return Response({"error": f"Não foi possível obter o status da impressora {printer_name}: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # Captura outros erros
            return Response({"error": f"Erro desconhecido: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({"printer_status": printer_status})

    def parse_printer_status(self, soup):
        # Analisa o HTML e extrai as informações relevantes
        printer_info = {}
        table = soup.find('table', {'class': 'list'})
        if table:
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                if len(columns) >= 5:
                    printer_info = {
                        "queue_name": columns[0].text.strip(),
                        "description": columns[1].text.strip(),
                        "location": columns[2].text.strip(),
                        "make_and_model": columns[3].text.strip(),
                        "status": columns[4].text.strip()
                    }
                    break  # Encontramos a impressora, podemos sair do loop
        return printer_info