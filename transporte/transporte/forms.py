# -*- coding:utf-8 -*-
from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError
from transporte.settings import LUGARES
from django.forms import ModelForm
from models import Usuario,Viagem,Agendamento

class FormUsuario(ModelForm):
    username = forms.CharField(label='Matrícula/SIAPE',widget=forms.TextInput())
    email = forms.CharField(label='E-mail',widget=forms.TextInput(attrs={'class': 'form-row'}))
    first_name = forms.CharField(label='Nome',widget=forms.TextInput(attrs={'class': 'form-row'}))
    last_name = forms.CharField(label='Sobrenome',widget=forms.TextInput(attrs={'class': 'form-row'}))
    telefone = forms.CharField(label='Telefone',widget=forms.TextInput(attrs={'class': 'form-row', 'placeholder': '(xx) xxxx-xxxx'}))
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

    def clean(self):

        viagem = self.cleaned_data.get('viagem')
        destino = self.cleaned_data.get('destino')
        origem = self.cleaned_data.get('localSaida').origem.id
        idaVolta = self.cleaned_data.get('idaVolta')

        if destino.id == origem:
                raise ValidationError(
                    "Seu destino e origem são iguais."
                )

        if (origem == 1 and idaVolta) or ((origem == 3 and destino.id == 2) and idaVolta):
                raise ValidationError(
                    "Não há como voltar deste destino."
                )

        mensagemVagas = "Não há vagas para esta viagem, cadastre-se no cadastro de reservas."

        if origem == 1: #SM
            if destino.id == 2:
                ida_volta_fw_pm__sm = Agendamento.objects.filter(viagem = viagem, localSaida__origem__id__in = [2,3], destino = 1, idaVolta = 1).count()
                ida_volta_sm__fw_pm = Agendamento.objects.filter(viagem = viagem, localSaida__origem__id = origem, destino__in = [2,3]).count()
                ida_volta_pm__fw = Agendamento.objects.filter(viagem = viagem, localSaida__origem__id = 3, destino = 2).count();
                ida_volta_fw__pm = Agendamento.objects.filter(viagem = viagem, localSaida__origem__id = 2, destino = 3, idaVolta = 1).count();
                if (ida_volta_fw_pm__sm + ida_volta_fw__pm + ida_volta_sm__fw_pm + ida_volta_pm__fw) >= LUGARES:
                    raise ValidationError(
                        mensagemVagas 
                    )

            if destino.id == 3:
                ida_volta_fw_pm__sm = Agendamento.objects.filter(viagem = viagem, localSaida__origem__id__in = [2,3], destino = 1, idaVolta = 1).count()
                ida_volta_sm__fw_pm = Agendamento.objects.filter(viagem = viagem, localSaida__origem__id = origem, destino__in = [2,3]).count()
                if (ida_volta_fw_pm__sm + ida_volta_sm__fw_pm) >= LUGARES:
                    raise ValidationError(
                        mensagemVagas 
                    )
            
        if origem == 2: #FW
            if destino.id == 3 and not idaVolta:
                ida_fw__pm = Agendamento.objects.filter(viagem = viagem, localSaida__origem__id = origem, destino__in = [1,3]).count()
                if ida_fw__pm >= LUGARES:
                    raise ValidationError(
                        mensagemVagas 
                    )
            if destino.id == 3 and idaVolta:
                ida_volta_fw__pm_sm = Agendamento.objects.filter(viagem = viagem, localSaida__origem__id = origem, destino__in = [1,3]).count()
                ida_volta_pm__fw = Agendamento.objects.filter(viagem = viagem, localSaida__origem__id__in = [1,3], destino = 2).count();
                if (ida_volta_fw__pm_sm + ida_volta_pm__fw) >= LUGARES:
                    raise ValidationError(
                        mensagemVagas 
                    )
            if destino.id == 1 and not idaVolta:
                ida_fw__sm = Agendamento.objects.filter(viagem = viagem, localSaida__origem__id = origem, destino__in = [1,3]).count()
                ida_pm__sm = Agendamento.objects.filter(viagem = viagem, localSaida__origem__id = 3, destino = 1).count()
                if (ida_fw__sm + ida_pm__sm) >= LUGARES:
                    raise ValidationError(
                        mensagemVagas 
                    )
            if destino.id == 1 and idaVolta:
                ida_volta_fw__sm = Agendamento.objects.filter(viagem = viagem, localSaida__origem__id = origem, destino__in = [1,3]).count()
                ida_volta_pm__sm = Agendamento.objects.filter(viagem = viagem, localSaida__origem__id = 3, destino = 1).count()
                ida_volta_sm__pm = Agendamento.objects.filter(viagem = viagem, localSaida__origem__id = 1, destino = 3).count()
                ida_volta_sm__fw = Agendamento.objects.filter(viagem = viagem, localSaida__origem__id__in = [1,3], destino = 2).count()
                print ida_volta_fw__sm + ida_volta_pm__sm + ida_volta_sm__pm + ida_volta_sm__fw
                if (ida_volta_fw__sm + ida_volta_pm__sm + ida_volta_sm__pm + ida_volta_sm__fw) >= LUGARES:
                    raise ValidationError(
                        mensagemVagas 
                    )
        if origem == 3: #PM
            if destino.id == 1 and not idaVolta:
                ida_pm_fw__sm = Agendamento.objects.filter(viagem = viagem, localSaida__origem__id__in = [origem,2], destino = 1).count()
                if (ida_pm_fw__sm) >= LUGARES:
                    raise ValidationError(
                        mensagemVagas 
                    )
            if destino.id == 1 and idaVolta:
                ida_volta_pm__sm = Agendamento.objects.filter(viagem = viagem, localSaida__origem__id = origem, destino = 1).count()
                ida_volta_fw__sm = Agendamento.objects.filter(viagem = viagem, localSaida__origem__id = 2, destino = 1).count()
                ida_volta_sm__pm_fw = Agendamento.objects.filter(viagem = viagem, localSaida__origem__id = 1, destino__in = [2,3]).count()
                if (ida_volta_fw__sm + ida_volta_pm__sm + ida_volta_sm__pm_fw) >= LUGARES:
                    raise ValidationError(
                        mensagemVagas 
                    )
            if destino.id == 2:
                ida_volta_fw__sm = Agendamento.objects.filter(viagem = viagem, localSaida__origem__id = 2, destino__in = [1,3], idaVolta = 1).count()
                ida_volta_sm__fw = Agendamento.objects.filter(viagem = viagem, localSaida__origem__id = 1, destino = 2).count()
                ida_volta_pm__fw = Agendamento.objects.filter(viagem = viagem, localSaida__origem__id = origem, destino = 2).count()
                if (ida_volta_fw__sm + ida_volta_sm__fw + ida_volta_pm__fw) >= LUGARES:
                    raise ValidationError(
                        mensagemVagas 
                    )
        return self.cleaned_data