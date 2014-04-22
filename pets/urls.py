from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$','principal.views.index'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^registro/$','principal.views.registro'),
    url(r'^inicio/$','principal.views.inicio'),
    url(r'^nuestros/medicos/$','principal.views.nuestrosMedicos'),
    url(r'^preguntas/frecuentes/$','principal.views.preguntasFrecuentes'),
    url(r'^bienvenido/$','principal.views.bienvenido'),
    url(r'^cerrar/$', 'principal.views.cerrar'),
    
)