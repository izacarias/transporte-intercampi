# -*-coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class Usuario(AbstractBaseUser):

    CATEGORIAS = (
        ('Aluno', 'Aluno'),
        ('Docente', 'Docente'),
        ('Técnico Administrativo', 'Técnico Administrativo'),
    )

    matricula = models.CharField('Matrícula/SIAPE', max_length=32)
    categoria = models.CharField('Categoria', max_length=32, choices=CATEGORIAS)
    rg = models.CharField('Número Identidade', max_length=16)
    telefone = models.CharField('Telefone', max_length=16)

    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')

    def __unicode__(self):
        self.first_name + ' ' + self.last_name

    USERNAME_FIELD = 'matricula'