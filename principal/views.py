#encoding:utf-8
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from principal.forms import MascotasForm
import pdb;
from principal.models import Mascotas


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
                    return HttpResponseRedirect('/bienvenido')
                else:
                    return render_to_response('noactivo.html', context_instance=RequestContext(request))
            else:
                return render_to_response('index.html', context_instance=RequestContext(request))
      

@login_required(login_url='/inicio')
def bienvenido(request):
    usuario = request.user
    mascotas = Mascotas.objects.filter(usuario_id=usuario.id)
    return render_to_response('bienvenido.html', {'mascotas':mascotas,'usuario':usuario}, context_instance=RequestContext(request))

@login_required(login_url='/inicio')
def agregarMascota(request):
    usuario = request.user
    
    if request.POST:
        try:
            mascota = Mascotas()
            mascota.nombre = request.POST['nombre']
            mascota.edad = request.POST['edad']
            mascota.usuario = request.user
            mascota.imagen =  request.FILES['imagen']
            mascota.tipo = request.POST['tipo']
            mascota.save()
            estado = 1
        except :
            estado = 2
        return render_to_response('agregar_mascota.html', {'usuario':usuario,'estado':estado}, context_instance=RequestContext(request))
    if request.method=='POST':
        formulario = MascotasForm(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/agregar/mascota')
    else:            
        usuario = request.user
        formulario = MascotasForm()
        return render_to_response('agregar_mascota.html', {'formulario':formulario,'usuario':usuario}, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def modificarMascota(request,idMascota):
        usuario = request.user
        mascota = Mascotas.objects.get(id=idMascota)
        if request.POST:
            try:
                mascota.nombre = request.POST['nombre']
                mascota.edad = request.POST['edad']
                mascota.tipo = request.POST['tipo']                    
                mascota.save()
                estado = 1
            except :
                estado = 2
            return render_to_response('modificar_mascota.html', {'mascota':mascota,'usuario':usuario,'estado':estado}, context_instance=RequestContext(request))
        else:            
            formulario = MascotasForm()
        return render_to_response('modificar_mascota.html', {'formulario':formulario,'mascota':mascota,'usuario':usuario}, context_instance=RequestContext(request)) 

@login_required(login_url='/ingresar')
def eliminarMascota(request,idMascota):        
        usuario = request.user
        mascota = Mascotas.objects.filter(id=idMascota)
        try:
            mascota.delete()
            estado=1 
        except :
            estado = 2
        mascotas = Mascotas.objects.filter(usuario_id=usuario.id)
        return render_to_response('bienvenido.html', {'mascotas':mascotas,'usuario':usuario,'estado':estado}, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def cerrar(request):
    logout(request)
    return HttpResponseRedirect('/')    

  