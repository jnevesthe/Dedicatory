from django.db import models
import random
import string
from django.core.validators import RegexValidator

def gerar_codigo_unico(model_class):
    while True:
        codigo = ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=7)
        )
        if not model_class.objects.filter(codigo=codigo).exists():
            return codigo


class Dedicatory(models.Model):

    OPCOES_TIPO = [
        ('mae', 'Mother'),
        ('pai', 'Father'),
        ('namorado', 'Girlfriend/Boyfriend'),
        ('irmao', 'Brother/Sister'),
        ('amigo', 'Friend'),
        ('celebridade', 'Celebrity'),
        ('eu_mesmo', 'Myself'),
    ]

    OPCOES_CONTEXTO = [
        ('amor', 'Loving'),
        ('carinho', 'Care'),
        ('amizade', 'Friendship'),
    ]

    OPCOES_STATUS = [
        ('publico', 'Public'),
        ('privado', 'Private'),
    ]

    teu = models.CharField(max_length=100)
    nome = models.CharField(max_length=100)
    pin = models.CharField(
    max_length=4,
    null=True,
    blank=True,
    validators=[
        RegexValidator(
            regex=r'^\d{4}$',
            message='PIN must be exactly 4 digits'
            )
        ]
    )

    tipo = models.CharField(max_length=20, choices=OPCOES_TIPO)
    contexto = models.CharField(max_length=20, choices=OPCOES_CONTEXTO)

    status = models.CharField(
        max_length=10,
        choices=OPCOES_STATUS,
        default='privado'
    )

    codigo = models.CharField(
        max_length=7,
        unique=True,
        blank=True,
        null=True
    )

    photo1 = models.ImageField(upload_to='dedicatorias/', blank=True, null=True)
    photo2 = models.ImageField(upload_to='dedicatorias/', blank=True, null=True)
    photo3 = models.ImageField(upload_to='dedicatorias/', blank=True, null=True)
    photo4 = models.ImageField(upload_to='dedicatorias/', blank=True, null=True)
    photo5 = models.ImageField(upload_to='dedicatorias/', blank=True, null=True)

    mensagem = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        # Se for privado, garante código
        if self.status == 'privado':
            if not self.codigo:
                self.codigo = gerar_codigo_unico(self.__class__)

        # Se for público, remove código
        if self.status == 'publico':
            self.codigo = gerar_codigo_unico(self.__class__)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Dedicatória de {self.nome} ({self.status})"
