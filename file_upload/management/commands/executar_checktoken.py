## FAZER ESSA logica
from django.core.management import BaseCommand 
from file_upload.tools.checkToken import GetToken 

class Command(BaseCommand):
    help = 'aqui deixo uma mensagem de ajuda'
    
    def handle(self, *args, **kwargs):
        command = GetToken()
        command.handle()