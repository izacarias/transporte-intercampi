# -*-coding: utf-8 -*-
import datetime
from django.db import models
from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


class Usuario(User):

    CATEGORIAS = (
        ('aluno', 'Aluno'),
        ('docente', 'Docente'),
        ('tecnico', 'Técnico Administrativo'),
    )

    categoria = models.CharField('Categoria', max_length=32, choices=CATEGORIAS)
    rg = models.CharField('Número Identidade', max_length=16)
    telefone = models.CharField('Telefone', max_length=16)

    class Meta:
        verbose_name = u'Usuario'
        verbose_name_plural = u'Usuarios'
        ordering = ['first_name','last_name']

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name
        

class Destino(models.Model):
    
    destino = models.CharField('Destino', max_length=64)

    class Meta:
        verbose_name = u'Destino'
        verbose_name_plural = u'Destinos'

    def __unicode__(self):
        return self.destino


class LocalSaida(models.Model):

    local = models.CharField('Local de Saída', max_length=50)
    hora = models.TimeField('Horário')
    origem = models.ForeignKey(Destino, verbose_name=u'Cidade')

    class Meta:
        verbose_name = u'Local Saída'
        verbose_name_plural = u'Locais Saída'
        ordering = ['hora']

    def __unicode__(self):
        return self.hora.strftime('%H:%M') + ' - ' + self.local


class Viagem(models.Model):

    data = models.DateField('Data')
    limite = models.DateTimeField()

    class Meta:
        verbose_name = u'Viagem'
        verbose_name_plural = u'Viagens'
        ordering = ['-data']

    def __unicode__(self):
        return self.data.strftime('%d/%m/%Y')

    def save(self):
        self.limite = datetime.datetime(self.data.year, self.data.month, self.data.day, 00, 00) - datetime.timedelta(hours=12)
        super(Viagem, self).save()


class Agendamento(models.Model):

    viagem = models.ForeignKey(Viagem, verbose_name=u'Viagem')
    destino = models.ForeignKey(Destino,verbose_name=u'Destino')
    localSaida = models.ForeignKey(LocalSaida, verbose_name=u'Local de Saída')
    idaVolta = models.BooleanField('Ida e Volta', help_text="Marque somente se for voltar no mesmo dia para a cidade de origem utilizando o transporte.")
    usuario = models.ForeignKey(Usuario, verbose_name=u'Usuário')

    class Meta:
        verbose_name = u'Agendamento'
        verbose_name_plural = u'Agendamentos'
        ordering = ['-viagem']

    def __unicode__(self):
        return self.viagem.data.strftime('%d/%m/%Y')









