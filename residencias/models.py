from django.db import models

class Tipo_residencia(models.Model):
    name = models.CharField(max_length = 30,  choices = ( ('Habitacion' , 'Habitacion') , ('Departamento' , 'Departamento' ), ('Casa','Casa') ) )
    color = models.CharField(max_length = 30, choices = ( ('grey','grey') , ('green','green'), ('yellow','yellow')  ) )

    def __unicode__(self):
        return str(self.name)

class Residencia(models.Model):
    latitude = models.FloatField(null = False)
    longitude = models.FloatField(null = False)
    title = models.CharField(max_length = 100, null = False)
    address = models.CharField(max_length = 50, null = False)
    phone1 = models.CharField(max_length = 15, null = False)
    phone2 = models.CharField(max_length = 15, null = True, blank = True)
    email = models.EmailField(null = True, blank = True)
    description = models.CharField(max_length = 300, null = False)
    date = models.DateField(auto_now = False, auto_now_add = True)
    gender = models.CharField(max_length = 30, choices = ( ('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('Masculino y Femenino', 'Masculino y Femenino')) )
    price_from = models.PositiveIntegerField(null = False)
    price_until = models.PositiveIntegerField(null = False)
    tipo_residencia = models.ForeignKey(Tipo_residencia)

    def __unicode__(self):
        return self.title

class Imagenes(models.Model):
    url = models.URLField()
    residencia = models.ForeignKey(Residencia)

    def __unicode__(self):
        return self.url

class Institucion(models.Model):
    name = models.CharField(max_length = 100)
    short_name = models.CharField(max_length = 10)

    def __unicode__(self):
        return self.name

class Sede(models.Model):
    name = models.CharField(max_length = 20)
    latitude = models.FloatField(null = False)
    longitude = models.FloatField(null = False)
    institucion = models.ForeignKey(Institucion)

    def __unicode__(self):
        return self.name