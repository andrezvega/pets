#encoding:utf-8
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
import pdb;


""" Gestor de usuarios  """

from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required           

# Aquí va todo lo que esta en el index todo el contenido de la página inicial 

def index(request):
	formulario = UserCreationForm()
        formularioLogin = AuthenticationForm()
	return render_to_response('index.html',{'formulario':formulario, 'formularioLogin':formularioLogin},context_instance=RequestContext(request))


def nuestrosMedicos(request):
    formulario = UserCreationForm()
    formularioLogin = AuthenticationForm()
    return render_to_response('nuestros_medicos.html',{'formulario':formulario,'formularioLogin':formularioLogin},context_instance=RequestContext(request))

def preguntasFrecuentes(request):
    formulario = UserCreationForm()
    formularioLogin = AuthenticationForm()
    return render_to_response('preguntas_frecuentes.html',{'formulario':formulario,'formularioLogin':formularioLogin},context_instance=RequestContext(request))

# registro 

def registro(request):
    if request.method=='POST':
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid:
            formulario.save()
            return HttpResponseRedirect('/')
    else:
        formulario = UserCreationForm()
        return HttpResponseRedirect('/')

#________________________Fin registro    


def inicio(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/bienvenido')
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    return render_to_response('bienvenido.html', context_instance=RequestContext(request))
                else:
                    return render_to_response('noactivo.html', context_instance=RequestContext(request))
            else:
                return render_to_response('index.html', context_instance=RequestContext(request))
      

@login_required(login_url='/inicio')
def bienvenido(request):
    
    usuario = request.user
    return render_to_response('bienvenido.html', {'usuario':usuario,'request': request}, context_instance=RequestContext(request))

  