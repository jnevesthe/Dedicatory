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
        ('parceiro(a)', 'Partner'),
        ('namorado', 'Boyfriend'),
        ('namorada', 'Girlfriend'),
        ('irmao(a)', 'Sibling'),
        ('amigo(a)', 'Friend'),
        ('celebridade', 'Celebrity'),
        ('eu_mesmo', 'Myself'),
    ]

    OPCOES_CONTEXTO = [
        ('amor', 'Loving'),
        ('carinho', 'Care'),
        ('amizade', 'Friendship'),
        ('admiracao', 'Admiration'),
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

        # Se for público, garante código
        if self.status == 'publico':
            self.codigo = gerar_codigo_unico(self.__class__)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Dedicatória de {self.nome} ({self.status})"



# models.py
from django.db import models
from ckeditor.fields import RichTextField

class FAQ(models.Model):
    pergunta = models.CharField(max_length=255, verbose_name="Pergunta")
    resposta = RichTextField(verbose_name="Resposta")
    ordem = models.IntegerField(default=0, help_text="Define a ordem de exibição no site")
    ativo = models.BooleanField(default=True, verbose_name="Ativo no site")

    class Meta:
        ordering = ['ordem']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.pergunta
