# -*- coding:utf-8 -*-
from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from models import Usuario,Viagem,Agendamento

class FormUsuario(ModelForm):
    username = forms.CharField(label='Matrícula/SIAPE',widget=forms.TextInput())
    email = forms.CharField(label='E-mail',widget=forms.TextInput(attrs={'class': 'form-row'}))
    first_name = forms.CharField(label='Nome',widget=forms.TextInput(attrs={'class': 'form-row'}))
    last_name = forms.CharField(label='Sobrenome',widget=forms.TextInput(attrs={'class': 'form-row'}))
    telefone = forms.CharField(label='Telefone',widget=forms.TextInput(attrs={'class': 'form-row', 'placeholder': '(xx) xxxx-xxxx', 'mask': 'fone'}))
    rg = forms.CharField(label='RG',widget=forms.TextInput(attrs={'class': 'form-row'}))
    password = forms.CharField(label='Senha',widget=forms.PasswordInput(attrs={'class': 'form-row'}))
    confirm_password = forms.CharField(label='Confirmação de senha',widget=forms.PasswordInput(attrs={'class': 'form-row'}))
    
    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'email', 'username', 'password', 'telefone', 'rg', 'categoria')

    def clean(self):

        if (self.cleaned_data.get('password') != self.cleaned_data.get('confirm_password')):

            raise ValidationError(
                "Confirmação de senha não confere com a senha digitada."
            )
        return self.cleaned_data


class FormAgendamento(ModelForm):
    viagem = forms.ModelChoiceField(Viagem.objects.filter(limite__gte = datetime.now), help_text="Caso o dia de interesse não conste para seleção, entre em contato com a direção.")
    class Meta:
        model = Agendamento