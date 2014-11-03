# -*-coding: utf-8 -*-
from django.shortcuts import render
from django.core.context_processors import csrf
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate,login
from transporte.forms import FormUsuario
from transporte.models import Usuario, Viagem

def new_user(request):
    
    ctoken = {}
    ctoken.update(csrf(request))
    if request.method == 'POST':
        form = FormUsuario(request.POST)
        if form.is_valid():
            usuario = Usuario.objects.create_user(request.POST.get('username'),request.POST.get('email'),request.POST.get('password'))
            usuario.first_name = request.POST.get('first_name')
            usuario.last_name = request.POST.get('last_name')
            usuario.categoria = request.POST.get('categoria')
            usuario.rg = request.POST.get('rg')
            usuario.telefone = request.POST.get('telefone')
            usuario.is_staff = True
            grupo = Group.objects.get(name='normal')
            usuario.groups.add(grupo)
            usuario.backend='django.contrib.auth.backends.ModelBackend'
            usuario.save()
            user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            login(request,user)
            return redirect('/')
        else:
            return render(request,"admin/new_user.html",{'form':form})
    else:
        form = FormUsuario()
        return render(request,"admin/new_user.html",{'form':form})

