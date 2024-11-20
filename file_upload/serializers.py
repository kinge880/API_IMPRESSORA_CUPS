from rest_framework import serializers
from file_upload.models import Arquivo


# class FileUploadSerializer(serializers.Serializer):
#     printer_name = serializers.CharField()
#     file = serializers.FileField()
    
#     def validate_printer_name(self, value):
#         if not value:
#             raise serializers.ValidationError("nome da impresora nao pode esta vazio")
#         return value
        
#     def validate_file(self,value):
#         MAX_SIZE = 10 * 1024 * 1024
#         if value.size > MAX_SIZE:
#             raise serializers.ValidationError("o arquivo excede o tamanho maximo permitido de 10MB")
#         return value

class FileUploadSerializer(serializers.Serializer):
    printer_name = serializers.CharField(max_length=100)
    file = serializers.FileField(required=False)
    text = serializers.CharField(required=False, allow_blank=True)
    
class ArquivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arquivo
        fields = ['id','nome_arquivo', 'arquivo', 'data_upload']
        
    def get_arquivo_url(self, obj):
        return obj.arquivo.url if obj.arquivo else None