from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context
from django.shortcuts import render
from django.db.models import Q
from models import Sede, Institucion, Residencia, Tipo_residencia
from django.core import serializers
import datetime

import json

def super_function_show(request):
    residencias_filters = Residencia.objects.all()
    print residencias_filters
    errors = []

    c = Context()
    if len(request.GET) > 0:

        if  int(request.GET['price_from']) > int(request.GET['price_until']):
            (request.GET['price_from'] , request.GET['price_until']) = ( request.GET['price_until'] , request.GET['price_from']  )
        if not ('tipo_residencia' in request.GET):
            errors.append("Seleccione un tipo de residencia")

        if not errors: # si no hay errores comienzo a realizar los filtros

            tipo_residencias = request.GET.getlist('tipo_residencia')
            query = Q()
            for tipo_residencia in tipo_residencias:
                query = query | Q(tipo_residencia__name = tipo_residencia)

            residencias = Residencia.objects.all().filter(query)

            if request.GET['genero'] == "Masculino y Femenino":
                tipo_genero =  ["Masculino y Femenino", "Femenino", "Masculino"]
                query = Q()
                for genero in tipo_genero:
                    query = query | Q(gender = genero)

                residencias = residencias.filter(query)
            else:
                residencias = residencias.filter(gender = request.GET['genero'])

            print len(residencias)

            #print 'comparar = ' + '[' + str(request.GET['price_from']) + ' : ' + str(request.GET['price_until']) + ']'
            residencias_filters = []
            #------------------------------- FILTRO POR PRECIOS ------------------------------------------------------
            for residencia in residencias:
                if (residencia.price_until < int(request.GET['price_from'])) or (int(request.GET['price_until']) < residencia.price_from):
                    print 'nada'
                    #print '[' + str(residencia['price_from']) + ' : ' + str(residencia['price_until']) + ']'
                else:
                    residencias_filters.append(residencia)

            #----------------------------------FALTA LA FUNCION FILTRO POR AREA-------------------------------------------

            c['residencias_filters'] = residencias_filters

            data = serializers.serialize('json', residencias_filters)

            #return render(request, 'form2.html', c)
            return HttpResponse(data, content_type="application/json")

    c['residencias_filters'] = residencias_filters
    c['errors'] = errors

    #return render(request, 'form1.html', c)

    data = serializers.serialize('json', residencias_filters)

    return HttpResponse(data, content_type="application/json")

def isnumber(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def super_function_save(request):
    errors = []
    c = Context()
    if len(request.GET) > 0:
        new_residencia = Residencia()
        if 'titulo' in request.GET and request.GET['titulo']:
            new_residencia.title = request.GET['titulo']
        else:
            errors.append("coloque un titulo valido!!")

        print Tipo_residencia.objects.filter(name = request.GET['tipo_residencia'])

        new_residencia.tipo_residencia = Tipo_residencia.objects.filter(name = request.GET['tipo_residencia'])[0]

        new_residencia.gender = request.GET['genero']

        if 'direccion' in request.GET and request.GET['direccion']:
            new_residencia.address = request.GET['direccion']
        else:
            errors.append("Coloque una dirrecion valida!!")

        if 'phone1' in request.GET and request.GET['phone1'] and isnumber(request.GET['phone1']):
            new_residencia.phone1 = request.GET['phone1']
        else:
            errors.append("Coloque un numero telefonico valido!!")

        if 'phone2' in request.GET and request.GET['phone2'] and isnumber(request.GET['phone2']):
            new_residencia.phone2 = request.GET['phone2']

        if 'email' in request.GET and request.GET['email']:
            new_residencia.email = request.GET['email']

        if 'descripcion' in request.GET and request.GET['descripcion']:
            new_residencia.description = request.GET['descripcion']
        else:
            errors.append("Coloque un descripcion")

        if 'price_from' in request.GET and request.GET['price_from'] and 'price_until' in request.GET and request.GET['price_until'] and isnumber(request.GET['price_from']) and isnumber(request.GET['price_until']):
            if int(request.GET['price_from']) < int(request.GET['price_until']):
                new_residencia.price_from = request.GET['price_from']
                new_residencia.price_until = request.GET['price_until']
            else:
                errors.append("Precio hasta debe ser MENOR que Precio desde")
        else:
            errors.append("Ponga valores validos!!")


        today = datetime.datetime.now()

        new_residencia.date = today.day
        new_residencia.latitude = request.GET['latitude']
        #new_residencia.latitude = -15.83218238
        new_residencia.longitude = request.GET['longitude']
        #new_residencia.longitude = -70.02137303

        new_residencia.save()

        return HttpResponse(json.dumps({'estado':'registrado'}))

    return render(request, 'save.html' , c)


def all_institutions(request):
    universities = Institucion.objects.all()
    data = serializers.serialize('json', universities)
    return HttpResponse(data, content_type="application/json")

def sedes_by_insitutions(request):
    if len(request.GET):
        sedes = Sede.objects.all().filter(institucion__id = request.GET['id'])
        data = serializers.serialize('json', sedes)
        return HttpResponse(data, content_type="application/json")
    else:
        return HttpResponse("Ningun dato fue recibido")

def sede_ubication(request):

    if len(request.GET):
        sede = Sede.objetcs.all().filter(id = request.GET['id'])
        data = serializers.serialize('json', sede)
        return HttpResponse(data, content_type = "application/json")
    else:
        HttpResponse("Ningun dato fue recibido")


def thanks(request):
    return HttpResponse("Gracias por insertar una nueva residencia para alquilar.")

def show_main(request):
    sede = Sede.objects.get(id = 1)
    institucion = Institucion.objects.get(id = int(sede.institucion.id))

    data = {}
    data['id_sede'] = sede.id
    data['name_institucion'] = institucion.name
    data['short_name_institucion'] = institucion.short_name
    data['name_sede'] = sede.name
    data['latitude_sede'] = sede.latitude
    data['longitude_sede'] = sede.longitude

    return HttpResponse(json.dumps(data), content_type="application/json")

def test(request):
    instituciones = Institucion.objects.all().order_by('id')
    sedes = Sede.objects.all().order_by('institucion__id')

    data = {}

    for institucion in instituciones:
        data[institucion.id] = {'institucion':institucion, 'sedes':[]}

    for sede in sedes:
        data[sede.institucion.id]['sedes'].append(sede)

    data_end = []

    for row in data:
        data_end.append(data[row])
        print data[row]

    tipo = Tipo_residencia.objects.all()

    return render(request, 'index.html', {'data':data_end, 'tipo':tipo})


def show_residencias(request):
    #residencias = Residencia.objects.order_by('latitude').order_by('longitude')

    residencias = Residencia.objects.all()

    datas = []
    for residencia in residencias:
        data = {}
        data['id_residencia'] = residencia.id
        data['latitude_residencia'] = residencia.latitude
        data['longitude_residencia'] = residencia.longitude
        data['color_residencia'] =residencia.tipo_residencia.color
        datas.append(data)

    return HttpResponse(json.dumps(datas), content_type="application/json")

def show_residencias_in_nav(request):

    residencias = Residencia.objects.order_by('latitude').order_by('longitude')
    datas = []
    for residencia in residencias:
        data = {}
        data['id_residencia'] = residencia.id
        data['longitude_residencia'] = residencia.longitude
        data['color_residencia'] =residencia.tipo_residencia.color
        datas.append(data)

    return HttpResponse(json.dumps(datas), content_type="application/json")



def another_main(request):
    sede = Sede.objects.get(id = 1)
    data={}
    data['latitude']=sede.latitude
    data['longitude']=sede.longitude
    data['id']=sede.id
    return HttpResponse(json.dumps(data), content_type="application/json")

def uri(request):
    return render(request, 'uri.js')




# Create your views here.
