from django.db import models
import random, string

def gerar_codigo_unico():
    # Gera um código de 7 caracteres apenas com letras e números
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))

class Dedicatory(models.Model):
    OPCOES_TIPO = [
        
        ('mae',  'Mother'),
        ('pai', 'Father'),
        ('namorado',  'GirlFriend/BoyFriend'),
        ('irmao',  'Brother/Sister'),
        ('amigo', 'Friend'),
    ]
    OPCOES_CONTEXTO = [
        ('amor',  'Loving'),
        ('carinho',  'Cart'),
        ('amizade',  'Friendship'),
    ]
    
  
    teu=models.CharField(max_length=100)
    nome = models.CharField(max_length=100)
    
    email = models.EmailField()
    
    tipo = models.CharField(max_length=20, choices=OPCOES_TIPO)
    contexto = models.CharField(max_length=20, choices=OPCOES_CONTEXTO)
    
    
    codigo = models.CharField(max_length=20, unique=True, default=gerar_codigo_unico)
    
    photo1 = models.ImageField(upload_to='dedicatorias/', blank=True, null=False)
    
    photo2 = models.ImageField(upload_to='dedicatorias/', blank=True, null=True)
    
    photo3 = models.ImageField(upload_to='dedicatorias/', blank=True, null=True)
    
    photo4 = models.ImageField(upload_to='dedicatorias/', blank=True, null=True)
 
    photo5 = models.ImageField(upload_to='dedicatorias/', blank=True, null=True)
    
    mensagem = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dedicatória de {self.nome} ({self.codigo})"