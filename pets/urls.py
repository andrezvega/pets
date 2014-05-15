from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from principal import views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$','principal.views.index'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^registro/$','principal.views.registro'),
    url(r'^inicio/$','principal.views.inicio'),
    url(r'^principal/$','principal.views.principal'),
    url(r'^nuestros/medicos/$','principal.views.nuestrosMedicos'),
    url(r'^preguntas/frecuentes/$','principal.views.preguntasFrecuentes'),
    url(r'^bienvenido/$','principal.views.bienvenido'),
    url(r'^preguntas/$','principal.views.pregunta'),
    url(r'^vacunas/$','principal.views.vacunas'),
    url(r'^cerrar/$', 'principal.views.cerrar'),
    url(r'^agregar/mascota/$','principal.views.agregarMascota'),
    url(r'^modificar/mascota/(?P<idMascota>[-\w]+)/$', views.modificarMascota),
    url(r'^eliminar/mascota/(?P<idMascota>[-\w]+)/$', views.eliminarMascota),
    url(r'^perfil/$','principal.views.perfil'),
    url(r'^medicos/$','principal.views.medicos'),
    url(r'^peluqueria/$','principal.views.peluqueria'),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',
		{'document_root':settings.MEDIA_ROOT,}
	),
    
)
