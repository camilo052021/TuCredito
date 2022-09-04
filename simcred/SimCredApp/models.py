from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from . import choicer
from . import calculos

# Create your models here.

class Empresa(models.Model): ## Clase que se usara para la creación de las empresas
    nombre_empresa = models.CharField(verbose_name='Nombre de Empresa', max_length=200, null=False, blank=False)
    nit = models.CharField(verbose_name='NIT', max_length=15, null=False, blank=False)
    actividad = models.CharField(verbose_name='Actividad Económica', max_length=255, null=False, blank=False)
    direccion_empresa = models.CharField(verbose_name='Dirección', max_length=255, null=False, blank=False)
    ciudad_empresa = models.CharField(verbose_name='Ciudad', max_length=255, blank=True, null=True)
    departamento_empresa = models.CharField(verbose_name='Departamento', max_length=255, blank=True, null=True)
    telefono_empresa = models.CharField(verbose_name='Teléfonos de contacto', max_length=50)
    correo_empresa = models.EmailField(verbose_name='Correo electrónico', max_length=255, null=False, blank=False)
    create_at = models.DateField(auto_now_add=True, verbose_name="Creado el", null=True)  
    modify_at = models.DateField(auto_now=True, verbose_name="Actualizado el")

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'

    def __str__(self):
        return f'Nombre Empresa {self.nombre_empresa}'

class Area(models.Model):## Clase que se usara para la creación de las áreas que tiene la empresa ingresada
    empresa = models.ForeignKey(Empresa, on_delete= CASCADE)
    nombre_area = models.CharField(verbose_name='Nombre Area', max_length= 255, null=False, blank=False)
    create_at = models.DateField(auto_now_add=True, verbose_name="Creado el", null=True)
    modify_at = models.DateField(auto_now=True, verbose_name="Actualizado el")
     
    class Meta:
        verbose_name = 'Nombre Area'
        verbose_name_plural = 'Areas de la empresa'

    def __str__(self):
        return f'Nombre Area {self.nombre_area}'

class Cargo(models.Model):
    nombre_cargo = models.CharField(verbose_name='Nombre Cargo', max_length=50,null=False, blank=False)
    created = models.DateField(auto_now_add=True, verbose_name="Creado el", null=True)  
    updated = models.DateField(auto_now=True, verbose_name="Actualizado el")

    def __str__(self):
        return self.nombre_cargo

    class Meta:
        verbose_name = 'cargo'
        verbose_name_plural = 'cargos'


class Cliente(models.Model):
    usuario_cliente = models.ForeignKey(User, on_delete=models.CASCADE, default=usuario)
    nombre_cliente = models.CharField(verbose_name='Nombres',max_length=30, null=False, blank=False)
    apellido_cliente = models.CharField(verbose_name='Apellidos',max_length=30, null=False, blank=False)
    ciudad_cliente = models.CharField(verbose_name='Ciudad',max_length=50, null=False, blank=False)
    departamento_cliente  = models.CharField(verbose_name='Departamento', max_length=255, blank=True, null=True)
    direccion_cliente = models.CharField(verbose_name='Dirección',max_length=100, null=False, blank=False)
    telefono_cliente = models.CharField(verbose_name='Teléfono',max_length=50, null=False, blank=False)
    correo_cliente = models.EmailField(verbose_name='Correo electrónico', max_length=255, null=False, blank=False)
    estado_civil = models.CharField(verbose_name='Estado Civil',max_length=50, null=False, choices=choicer.ESTADO_CIVIL)
    ocupacion = models.CharField(verbose_name='Ocupación',max_length=50)
    genero = models.CharField(verbose_name='Género',max_length=50, null=False, choices=choicer.GENERO)
    edad = models.IntegerField(verbose_name='Edad', default= 0)
    ingresos = models.IntegerField(verbose_name='Ingresos', default= 0)
    created = models.DateField(auto_now_add=True, verbose_name="Creado el", null=True)  
    updated = models.DateField(auto_now=True, verbose_name="Actualizado el")

    def usuario(self):
        return self.nombre_cliente

    def __str__(self):
        return self.nombre_cliente

    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfiles'


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    ciudad_perfil = models.CharField(verbose_name='Ciudad',max_length=50, default='Ciudad')
    departamento_perfil = models.CharField(verbose_name='Departamento', max_length=255, blank=True, null=True)
    direccion_perfil = models.CharField(verbose_name='Dirección',max_length=100, default='Dirección')
    telefono_perfil = models.CharField(verbose_name='Teléfono',max_length=50, default='Teléfono')
    created = models.DateField(auto_now_add=True, verbose_name="Creado el", null=True)  
    updated = models.DateField(auto_now=True, verbose_name="Actualizado el")

    def __str__(self):
        return self.usuario.username

    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfiles'

class Tasa(models.Model):
    usuario_t = models.ForeignKey(User, on_delete=models.CASCADE, default=usuario)
    banco_tasa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    tasa = models.FloatField(verbose_name='Tasa EA',null=False, verbose_name="Tasa E.A")
    tasa_nominal = models.FloatField(verbose_name='Tasa Nominal',default=0)
    periodicidad = models.CharField(verbose_name='Tipo de periodo',max_length=50, null=False, choices=choicer.TIPO_PERIODO)
    created = models.DateField(auto_now_add=True, verbose_name="Creado el", null=True)  
    updated = models.DateField(auto_now=True, verbose_name="Actualizado el")
    
    
    def usuario(self):
        return self.User.username
    
    @property
    def calculo_tasa(self):
        #TNMV=[(1+i)^(1/12)-1]

        if self.periodicidad == "MENSUAL":
            tasanom = (1+(self.tasa/100))**(1/12)-1
            return round(tasanom*100,2)

        if self.periodicidad == "BIMENSUAL":
            tasanom = (1+(self.tasa/100))**(1/6)-1
            return round(tasanom*100,2)

        if self.periodicidad == "TRIMESTAR":
            tasanom = (1+(self.tasa/100))**(1/4)-1
            return round(tasanom*100,2)

        if self.periodicidad == "CUATRIMESTRAL":
            tasanom = (1+(self.tasa/100))**(1/3)-1
            return round(tasanom*100,2)

        if self.periodicidad == "SEMESTRAL":
            tasanom = (1+(self.tasa/100))**(1/2)-1
            return round(tasanom*100,2)

    def save(self):
        self.tasa_nominal = self.calculo_tasa
        super (Tasa, self).save()

    class Meta:
        verbose_name ='tasa'
        verbose_name_plural ='tasas'

    def __str__(self):
        return str(self.tasa)


class Seguro(models.Model):
    valor_seguro = models.FloatField(verbose_name='Valor Seguro',null=False)
    monto_asegurar = models.FloatField(verbose_name='Monto del crédito',null=False)
    aseguradora = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True, verbose_name="Creado el", null=True)  
    updated = models.DateField(auto_now=True, verbose_name="Actualizado el")

    @property
    def calculo_seguro(self):
        #valor_seguro=monto_asegurar * 10%
        return seguro = self.monto_asegurar * 0.10

    def save(self):
        self.valor_seguro = self.calculo_seguro
        super (Seguro, self).save()

    class Meta:
        verbose_name ='seguro'
        verbose_name_plural ='seguros'

    def __str__(self):
        return self.aseguradora


### calcula cuota mensual

class Credito(models.Model):
    usuario_credito = models.ForeignKey(User, on_delete=models.CASCADE, default=usuario, verbose_name="Usuario Creador")
    cliente_credito = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo = models.CharField(verbose_name='Tipo crédito',max_length=50, choices=choicer.TIPO_CREDITO, null=False)
    tasa = models.ForeignKey(Tasa, on_delete=models.CASCADE, verbose_name='Tasa NV',)
    plazo = models.IntegerField(verbose_name='Plazo',null=False)
    monto = models.FloatField(verbose_name='Valor del Crédito',null=False)
    cuota = models.FloatField(verbose_name='Cuota',default=0)
    seguro_credito = models.ForeignKey(Seguro, on_delete=models.CASCADE,verbose_name='Seguro Tomado')
    created = models.DateField(auto_now_add=True, verbose_name="Creado el", null=True)  
    updated = models.DateField(auto_now=True, verbose_name="Actualizado el")
    
    def usuario(self):
        return self.User.username
    @property
    def calculo_cuota(self):
        tasa_nom = self.tasa.tasa_nominal/100
        cuota = (self.monto*(tasa_nom*(1+tasa_nom)**(self.plazo)))/(((1+tasa_nom)**(self.plazo))-1)
        return round(cuota,2)
    def save(self):
        self.cuota = self.calculo_cuota
        super (Credito, self).save()

    class Meta:
        verbose_name ='Credito'
        verbose_name_plural ='Creditos'

    def __str__(self):
        return f'{self.tipo} {self.cliente_credito} {self.cuota}'    
