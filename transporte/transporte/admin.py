# -*-coding: utf-8 -*-
from django.contrib import admin
from models import *
from forms import FormAgendamento


class UsuarioAdmin(admin.ModelAdmin):
    
    fields = (('first_name','last_name'),'categoria','rg','telefone')

class ViagemAdmin(admin.ModelAdmin):
    fields = ('data',)
    def queryset(self, request):
        if request.user.is_superuser or request.user.groups.filter(name='almoxerifado').exists():
            return Viagem.objects.all()
        return Viagem.objects.filter(id = 1)

class AgendamentoAdmin(admin.ModelAdmin):
    form = FormAgendamento

admin.site.register(Usuario,UsuarioAdmin)
admin.site.register(Destino)
admin.site.register(LocalSaida)
admin.site.register(Viagem,ViagemAdmin)
admin.site.register(Agendamento,AgendamentoAdmin)