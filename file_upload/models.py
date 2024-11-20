from django.db import models

# Create your models here.
class Arquivo(models.Model):
    STATUS_CHOICES = [
        ('S', 'Sim'),
        ('N', 'Nao'),
        ('P', 'Pendente'),
        ('B', 'Bloqueado'),
    ]
    nome_arquivo = models.CharField(max_length=255)
    arquivo = models.FileField(upload_to='uploads/%Y/%m/%d/')#caminho onde o arquivo sera salvo
    data_upload = models.DateTimeField(auto_now_add=True)
    usuario_ativo = models.CharField(max_length=1, choices=[('S', 'Sim'), ('N', 'Nao')], default='S')
    usuario_chave = models.CharField(max_length=255, default= 1)
    
    def __str__(self):
        return f"{self.nome_arquivo} - {self.arquivo} - {self.data_upload}"
    
class Usuario(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField()
    
    def __str__(self):
        return self.nome