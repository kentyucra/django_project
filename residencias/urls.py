from django.conf.urls import patterns, include, url

from views import *

urlpatterns = patterns('',
    url(r'^$', show_main),
    url(r'^test/$', show_residencias),
    url(r'^test2/$', test),
    url(r'^form/search/$', super_function_show),
    url(r'^form/save/$', super_function_save),
    url(r'^utils/uri.js', uri),
    url(r'^instituciones/$', all_institutions),
    url(r'^institucion/sedes/$', sedes_by_insitutions),
    url(r'^institucion/sede/ubicacion/$', sede_ubication),
    #url(r'^sedes/$', all_sedes),
)
