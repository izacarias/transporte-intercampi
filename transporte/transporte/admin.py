# -*-coding: utf-8 -*-
import datetime
from django.contrib import admin
from models import *
from forms import FormAgendamento


class UsuarioAdmin(admin.ModelAdmin):
    
    fields = (('first_name','last_name'),'categoria','rg','telefone')

class ViagemAdmin(admin.ModelAdmin):
    fields = ('data',)

    def queryset(self, request):
        return Viagem.objects.filter(data__gte = datetime.datetime.now)

class AgendamentoAdmin(admin.ModelAdmin):
    form = FormAgendamento
    list_display = ('viagem','usuario')

    fieldsets = [
            (None, {
                    'fields':('viagem','destino','localSaida','idaVolta','usuario'),
        }),
    ]
    restricted_fieldsets = [
        (None, {
                    'fields':('viagem','destino','localSaida','idaVolta'),
        }),
    ]

    def queryset(self, request):
        if request.user.is_superuser or request.user.groups.filter(name='almoxerifado').exists():
            return Agendamento.objects.filter(viagem__data__gte = datetime.datetime.now)
        return Agendamento.objects.filter(usuario = request.user.id, viagem__data__gte = datetime.datetime.now)

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser or request.user.groups.filter(name='almoxerifado').exists():
            return super(AgendamentoAdmin, self).get_fieldsets(request, obj=obj)
        else:
            return self.restricted_fieldsets

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and not request.user.groups.filter(name='almoxerifado').exists():
            obj.usuario = Usuario.objects.get(id=request.user.id)
        obj.save()

admin.site.register(Usuario,UsuarioAdmin)
admin.site.register(Destino)
admin.site.register(LocalSaida)
admin.site.register(Viagem,ViagemAdmin)
admin.site.register(Agendamento,AgendamentoAdmin)