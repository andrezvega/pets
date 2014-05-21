#encoding:utf-8
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from principal.forms import MascotasForm
from principal.forms import PreguntaForm
import pdb;
from principal.models import Mascotas
from principal.models import Medicos
from principal.models import Pregunta
from principal.models import ComplementoUsuario
from principal.models import Vacuna
from principal.models import VacunaMascota
from principal.models import Peluqueria

import datetime


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
        return HttpResponseRedirect('/principal')
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    if acceso.is_staff:
                        return HttpResponseRedirect('/principalMedico')
                    else:
                        return HttpResponseRedirect('/principal')    
                else:
                    return render_to_response('noactivo.html', context_instance=RequestContext(request))
            else:
                return render_to_response('index.html', context_instance=RequestContext(request))
      

@login_required(login_url='/inicio')
def bienvenido(request):
    usuario = request.user
    try: 
        informacionUsuario = ComplementoUsuario.objects.get(usuario_id=usuario.id)
    except:
        informacionUsuario=0        
    mascotas = Mascotas.objects.filter(usuario_id=usuario.id)
    return render_to_response('bienvenido.html', {'mascotas':mascotas,'usuario':usuario,'informacionUsuario':informacionUsuario}, context_instance=RequestContext(request))

@login_required(login_url='/inicio')
def agregarMascota(request):
    usuario = request.user
    try: 
        informacionUsuario = ComplementoUsuario.objects.get(usuario_id=usuario.id)
    except:
        informacionUsuario=0 
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
                try:
                    mascota.imagen = request.FILES['imagen']
                except:
                    def __unicode__(self):
                        mascota.imagen = self.imagen                         
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
def medicos(request):
    usuario = request.user
    try: 
        informacionUsuario = ComplementoUsuario.objects.get(usuario_id=usuario.id)
    except:
        informacionUsuario=0
    query = " select medicos.*,especialidad.nombre as nombreEspecialidad  from principal_medicos as medicos, principal_especialidad as especialidad where medicos.especialidad_id = especialidad.id "
    medicos=Medicos.objects.raw(query)
    return render_to_response('medicos.html', {'usuario':usuario,'medicos':medicos,'informacionUsuario':informacionUsuario}, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def perfil(request):
    usuario = request.user
    mascotas = Mascotas.objects.filter(usuario_id=usuario.id)
    user = User.objects.get(id=usuario.id)

    if request.POST:
        user.first_name = request.POST['nombres']
        user.last_name = request.POST['apellidos']
        user.save() 
        try: 
            complemento = ComplementoUsuario.objects.get(usuario_id = usuario.id )
            informacionUsuario = ComplementoUsuario.objects.get(usuario_id=usuario.id)
            complemento.imagen= request.FILES['imagen']
        except:
            complemento = 1    
            if complemento == 1 :
                complemento = ComplementoUsuario()
                complemento.imagen= request.FILES['imagen']
                complemento.usuario= request.user
            else:
                complemento.imagen= request.FILES['imagen']
        complemento.save()
        informacionUsuario = ComplementoUsuario.objects.get(usuario_id=usuario.id)
        return render_to_response('bienvenido.html', {'usuario':usuario,'informacionUsuario':informacionUsuario,'mascotas':mascotas}, context_instance=RequestContext(request))                        
    else:
        formulario = UserCreationForm()
        try:
            informacionUsuario = ComplementoUsuario.objects.get(usuario_id=usuario.id)
        except:
            informacionUsuario=1    
        return render_to_response('perfil.html', {'usuario':usuario,'informacionUsuario':informacionUsuario,'formulario':formulario}, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def perfilMedico(request):
    usuario = request.user
    mascotas = Mascotas.objects.filter(usuario_id=usuario.id)
    user = User.objects.get(id=usuario.id)

    if request.POST:
        user.first_name = request.POST['nombres']
        user.last_name = request.POST['apellidos']
        user.save() 
        try: 
            complemento = ComplementoUsuario.objects.get(usuario_id = usuario.id )
            informacionUsuario = ComplementoUsuario.objects.get(usuario_id=usuario.id)
            complemento.imagen= request.FILES['imagen']
        except:
            complemento = 1    
            if complemento == 1 :
                complemento = ComplementoUsuario()
                complemento.imagen= request.FILES['imagen']
                complemento.usuario= request.user
            else:
                complemento.imagen= request.FILES['imagen']
        complemento.save()
        informacionUsuario = ComplementoUsuario.objects.get(usuario_id=usuario.id)
        return render_to_response('principalMedico.html', {'usuario':usuario,'informacionUsuario':informacionUsuario,'mascotas':mascotas}, context_instance=RequestContext(request))                        
    else:
        formulario = UserCreationForm()
        try:
            informacionUsuario = ComplementoUsuario.objects.get(usuario_id=usuario.id)
        except:
            informacionUsuario=1    
        return render_to_response('perfilMedico.html', {'usuario':usuario,'informacionUsuario':informacionUsuario,'formulario':formulario}, context_instance=RequestContext(request))



@login_required(login_url='/ingresar')
def pregunta(request):
    formulario = PreguntaForm()
    usuario = request.user
    try:
        informacionUsuario = ComplementoUsuario.objects.get(usuario_id=usuario.id)
    except:
        informacionUsuario=1
    preguntas = Pregunta.objects.filter(usuario_id=usuario.id).order_by('-fecha')
    if request.POST:
        try:
            pregunta = Pregunta()
            pregunta.pregunta = request.POST['pregunta']
            pregunta.descripcion = request.POST['descripcion']
            pregunta.fecha = datetime.datetime.now()
            pregunta.usuario= request.user
            pregunta.save()
            estado = 1
        except :
            estado = 2
        return render_to_response('preguntas.html', {'usuario':usuario,'estado':estado,'formulario':formulario,'informacionUsuario':informacionUsuario,'preguntas':preguntas}, context_instance=RequestContext(request))
    else:       
        return render_to_response('preguntas.html', {'usuario':usuario,'informacionUsuario':informacionUsuario,'preguntas':preguntas,'formulario':formulario}, context_instance=RequestContext(request))    

   

@login_required(login_url='/ingresar')


@login_required(login_url='/ingresar')
def cerrar(request):
    logout(request)
    return HttpResponseRedirect('/')    

@login_required(login_url='/ingresar')
def principal(request):
    usuario = request.user
    estado = 0
    try:
        informacionUsuario = ComplementoUsuario.objects.get(usuario_id=usuario.id)
    except:
        informacionUsuario=1
    mascotas=Mascotas.objects.exclude(usuario=usuario.id).order_by('?')
    return render_to_response('principal.html', {'usuario':usuario,'informacionUsuario':informacionUsuario,'mascotas': mascotas}, context_instance=RequestContext(request))    

@login_required(login_url='/ingresar')
def principalMedico(request):
    usuario = request.user
    estado = 0
    try:
        informacionUsuario = ComplementoUsuario.objects.get(usuario_id=usuario.id)
    except:
        informacionUsuario=1
    mascotas=Mascotas.objects.exclude(usuario=usuario.id).order_by('?')
    return render_to_response('principalMedico.html', {'usuario':usuario,'informacionUsuario':informacionUsuario,'mascotas': mascotas}, context_instance=RequestContext(request))  

@login_required(login_url='/ingresar')    
def peluqueria(request):
    usuario = request.user
    estado = 0
    mascotas=Mascotas.objects.filter(usuario=usuario.id)
    try:
        informacionUsuario = ComplementoUsuario.objects.get(usuario_id=usuario.id)
    except:
        informacionUsuario=1
    if request.POST:    
        try:
            peluqueria = Peluqueria() 
            peluqueria.fecha = request.POST['fecha']
            peluqueria = Peluqueria() 
            peluqueria.fecha = request.POST['fecha']
            m = Mascotas.objects.get(id=request.POST['mascota'])
            peluqueria.mascota = m
            peluqueria.save()
            estado = 1
        except:
            estado = 2    
    try:
        peluqueria = Peluqueria.objects.filter(mascota = m).order_by('-fecha')    
        fechaPeluqueria = peluqueria[0]
    except:
        fechaPeluqueria = False    
    return render_to_response('peluqueria.html', {'usuario':usuario,'informacionUsuario':informacionUsuario,'mascotas':mascotas,'estado':estado,'fechaPeluqueria':fechaPeluqueria}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')    
def fechaPeluqueria(request,idMascota):
    usuario = request.user
    estado = 0
    try:
        informacionUsuario = ComplementoUsuario.objects.get(usuario_id=usuario.id)
    except:
        informacionUsuario=1
    if request.POST:    
        try:
            peluqueria = Peluqueria() 
            peluqueria.fecha = request.POST['fecha']
            m = Mascotas.objects.get(id=request.POST['mascota'])
            peluqueria.mascota = m
            peluqueria.save()
            estado = 1
        except:
            estado = 2
    else:
        try:
            mascota = Mascotas.objects.get(id = idMascota)
            peluqueria = Peluqueria.objects.filter(mascota = mascota).order_by('-fecha')    
            fechaPeluqueria = peluqueria[0]
        except:
            fechaPeluqueria = False  
        return render_to_response('fechaPedicure.html', {'usuario':usuario,'informacionUsuario':informacionUsuario,'mascota':idMascota,'estado':estado,'fechaPeluqueria':fechaPeluqueria}, context_instance=RequestContext(request))            
   

@login_required(login_url='/ingresar')
def vacunas(request,idMascota):
    usuario = request.user
    estado=0
    try:
        informacionUsuario = ComplementoUsuario.objects.get(usuario_id=usuario.id)
    except:
        informacionUsuario=1

    query = " select vacunaAplicada.*,mascota.*,vacuna.* from principal_mascotas as mascota,principal_vacuna as vacuna, principal_vacunamascota as vacunaAplicada  where vacuna.id != vacunaAplicada.vacuna_id  AND vacuna.animal = mascota.tipo AND mascota.id = %s " % idMascota 
    vacunas=Vacuna.objects.raw(query)

    return render_to_response('vacunas.html', {'usuario':usuario,'informacionUsuario':informacionUsuario,'estado':estado,'vacunas':vacunas}, context_instance=RequestContext(request))    


@login_required(login_url='/ingresar')    
def mascotaVacuna(request):
    usuario = request.user
    estado = 0
    try:
        informacionUsuario = ComplementoUsuario.objects.get(usuario_id=usuario.id)
    except:
        informacionUsuario=1
    if request.POST:    
        vacunas = request.POST['vacuna[]']
        m = Mascotas.objects.get(id=request.POST['mascota'])
        vacunaM = VacunaMascota() 
        for v in vacunas:
            try:
                vac = Vacuna.objects.get(id=v)
                vacunaM.vacuna = vac
                vacunaM.mascota = m
                vacunaM.save()
                estado = 1
            except:
                estado= 0   
        mascotas=Mascotas.objects.filter(usuario=usuario.id)
        return render_to_response('mascotaVacuna.html', {'usuario':usuario,'informacionUsuario':informacionUsuario,'mascotas':mascotas,'estado':estado}, context_instance=RequestContext(request))                    
    else:
        try:
            mascotas=Mascotas.objects.filter(usuario=usuario.id)
        except:
            mascotas = False  
        return render_to_response('mascotaVacuna.html', {'usuario':usuario,'informacionUsuario':informacionUsuario,'mascotas':mascotas,'estado':estado}, context_instance=RequestContext(request))            
    

