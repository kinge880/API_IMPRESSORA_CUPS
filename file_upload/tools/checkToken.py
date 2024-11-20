from django.core.management.base import BaseCommand 
from file_upload.models import Arquivo
import logging


class GetToken(BaseCommand):
    help = "Consulta Usuario_Chave de USER_AGENTES onde USUARIO_ATIVO é S"
    
    def handle(self, *args, **kwargs):
        try:
            resultados = Arquivo.objects.filter(usuario_ativo='S').values_list('usuario_chave', flat=True)
            
            if resultados:
                token_list = list(resultados) #Conveerter o queryset para a lista
                
                #fazendo algo com os resultados
                print("Tokens encontrados:", token_list)
                ##tambem pode registrar token nos log
                logging.info(f"Tpokens encontrados:{token_list}")
            else:
                print("nenhum token encontrado para usuarios ativos")
                logging.info("nenhum token encontrdo para usuarios ativos")
                
        except Exception as e:
            logging.error(f"Erro ao consultar tokens: {str(e)}")
            self.stdout.write(self.style.Error(f"Erro: {str(e)}"))
            