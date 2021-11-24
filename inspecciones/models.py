import uuid

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db import models
from django.db.models import Q

from inspecciones.q_logic import different, if_and_only_if


class Organizacion(models.Model):
    nombre = models.CharField(max_length=120, blank=False)
    logo = models.ImageField(default='blank.jpg', upload_to='logos_organizaciones')
    link = models.URLField(blank=True)
    acerca = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class Perfil(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    celular = models.CharField(max_length=13, blank=True)
    organizacion = models.ForeignKey(Organizacion, related_name='usuarios', on_delete=models.PROTECT, null=True)
    foto = models.ImageField(default='blank.jpg', upload_to='fotos_perfiles')

    class Roles(models.TextChoices):
        inspector = "inspector"
        administrador = "administrador"
        desarrollador = "desarrollador"

    rol = models.CharField(max_length=20, choices=Roles.choices)

    def __str__(self):
        return f'{self.user}'


class EtiquetaJerarquica(models.Model):
    nombre = models.CharField(max_length=120, primary_key=True)
    json = models.JSONField()

    class Meta:
        abstract = True


class EtiquetaJerarquicaDeActivo(EtiquetaJerarquica):
    organizacion = models.ForeignKey(Organizacion, related_name='etiquetas_de_activo', on_delete=models.CASCADE)
    pass


class EtiquetaJerarquicaDePregunta(EtiquetaJerarquica):
    organizacion = models.ForeignKey(Organizacion, related_name='etiquetas_de_pregunta', on_delete=models.CASCADE)
    pass


class EtiquetaManager(models.Manager):
    def get_by_natural_key(self, clave, valor):
        return self.get(clave=clave, valor=valor)


class Etiqueta(models.Model):
    #organizacion = models.ForeignKey(Organizacion, related_name='etiquetas', on_delete=models.PROTECT)
    """Modelo base para crear etiquetas para una tabla, se debería analizar la posibilidad de usar relaciones genéricas
    https://docs.djangoproject.com/en/3.2/ref/contrib/contenttypes/#generic-relations """
    clave = models.CharField(max_length=20)
    valor = models.CharField(max_length=20)

    objects = EtiquetaManager()

    def natural_key(self):
        return self.clave, self.valor

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(fields=['clave', 'valor'], name='%(app_label)s_%(class)s_natural_key')
        ]

    def __str__(self):
        return f"{self.clave}: {self.valor}"


class EtiquetaDeActivo(Etiqueta):
    pass


class Activo(models.Model):
    id = models.CharField(primary_key=True, max_length=120)
    etiquetas = models.ManyToManyField(EtiquetaDeActivo, related_name='activos')
    organizacion = models.ForeignKey(Organizacion, related_name='activos', on_delete=models.CASCADE)

    def __str__(self):
        return self.id


class Cuestionario(models.Model):
    id = models.UUIDField(primary_key=True)
    tipo_de_inspeccion = models.CharField(max_length=120)
    version = models.IntegerField()
    periodicidad_dias = models.IntegerField()
    organizacion = models.ForeignKey(Organizacion, related_name='cuestionarios', on_delete=models.CASCADE)
    # si es null es porque el usuario que lo creó ya no existe
    creador = models.ForeignKey(Perfil, related_name='cuestionarios_creados', null=True, on_delete=models.SET_NULL)
    etiquetas_aplicables = models.ManyToManyField(EtiquetaDeActivo, related_name='cuestionarios')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['organizacion', 'tipo_de_inspeccion', 'version'],
                                    name='version de cuestionario')
        ]

    def __str__(self):
        return f'{self.tipo_de_inspeccion} v{self.version}'


class Bloque(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    n_orden = models.IntegerField(null=True)
    cuestionario = models.ForeignKey(Cuestionario, on_delete=models.CASCADE, related_name='bloques')

    def __str__(self):
        return f'{self.n_orden}'


class FotoCuestionario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    foto = models.ImageField(upload_to='fotos_cuestionarios')
    content_type = models.ForeignKey(ContentType, null=True, on_delete=models.CASCADE)
    object_id = models.UUIDField(null=True)
    content_object = GenericForeignKey()

    def __str__(self):
        return self.foto.path


class Titulo(models.Model):
    id = models.UUIDField(primary_key=True)
    bloque = models.OneToOneField(Bloque, on_delete=models.CASCADE, related_name='titulo')
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=1500, blank=True)
    fotos = GenericRelation(FotoCuestionario, related_query_name='titulo')

    def __str__(self):
        return self.titulo


class EtiquetaDePregunta(Etiqueta):
    pass


class Pregunta(models.Model):
    id = models.UUIDField(primary_key=True)
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=1500, blank=True)
    criticidad = models.IntegerField()
    fotos_guia = GenericRelation(FotoCuestionario, related_query_name='pregunta')
    etiquetas = models.ManyToManyField(EtiquetaDePregunta, related_name='preguntas')

    # uno y solo uno de estos 2 debe ser no nulo
    bloque = models.OneToOneField(Bloque, null=True, on_delete=models.CASCADE, related_name='pregunta')
    cuadricula = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name='preguntas')

    class TiposDePregunta(models.TextChoices):
        # tipo_de_cuadricula debe ser no null, tiene opciones_de_respuesta y preguntas
        cuadricula = 'cuadricula'
        # cuadricula debe ser no null, las demas tienen el bloque no null, no tiene opciones_de_respuesta
        # (son las de la cuadricula asociada)
        parte_de_cuadricula = 'parte_de_cuadricula'
        # en la respuesta opcion_seleccionada debe ser no null, tiene opciones_de_respuesta
        seleccion_unica = 'seleccion_unica'
        # tiene opciones de respuesta
        seleccion_multiple = 'seleccion_multiple'
        # en la respuesta valor debe ser no null, no tiene opciones_de_respuesta, tiene criticidades_numericas
        numerica = 'numerica'

    tipo_de_pregunta = models.CharField(choices=TiposDePregunta.choices, max_length=50)

    class TiposDeCuadricula(models.TextChoices):
        seleccion_unica = 'seleccion_unica'  # todas las preguntas deben ser de tipo unica respuesta
        seleccion_multiple = 'seleccion_multiple'  # todas las preguntas deben ser de tipo multiples respuestas

    # no null para preguntas tipo cuadricula
    tipo_de_cuadricula = models.CharField(choices=TiposDeCuadricula.choices, null=True, max_length=50)

    # no null para las respuestas tipo numerica
    unidades = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=different(Q(bloque__isnull=False), Q(cuadricula__isnull=False)),
                                   name='%(app_label)s_%(class)s_padre'),
            models.CheckConstraint(check=if_and_only_if(Q(tipo_de_pregunta="cuadricula"),
                                                        Q(tipo_de_cuadricula__isnull=False)),
                                   name='%(app_label)s_%(class)s_cuadricula'),
            models.CheckConstraint(check=if_and_only_if(Q(tipo_de_pregunta="parte_de_cuadricula"),
                                                        Q(cuadricula__isnull=False)),
                                   name='%(app_label)s_%(class)s_parte_de_cuadricula'),
        ]

    def __str__(self):
        return f'{self.titulo}'


class OpcionDeRespuesta(models.Model):
    id = models.UUIDField(primary_key=True)
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=1500, blank=True)
    criticidad = models.IntegerField()
    pregunta = models.ForeignKey(Pregunta, null=True, on_delete=models.CASCADE, related_name='opciones_de_respuesta')

    def __str__(self):
        return f'{self.titulo}'


class CriticidadNumerica(models.Model):
    id = models.UUIDField(primary_key=True)
    valor_minimo = models.FloatField()
    valor_maximo = models.FloatField()
    criticidad = models.IntegerField()
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='criticidades_numericas')

    def __str__(self):
        return f'({self.valor_maximo}, {self.valor_maximo}) : {self.criticidad}'


class Inspeccion(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    cuestionario = models.ForeignKey(Cuestionario, on_delete=models.DO_NOTHING, related_name='inspecciones')
    activo = models.ForeignKey(Activo, related_name='inspecciones', on_delete=models.DO_NOTHING)
    inspector = models.ForeignKey(Perfil, related_name='inspecciones_llenadas', null=True, on_delete=models.SET_NULL)

    momento_inicio = models.DateTimeField()
    momento_subida = models.DateTimeField(auto_now_add=True)


class FotoRespuesta(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    foto = models.ImageField(upload_to='fotos_inspecciones')
    respuesta = models.ForeignKey('Respuesta', null=True, on_delete=models.CASCADE, related_name='fotos')

    class TiposDeFoto(models.TextChoices):
        base = 'base'
        reparacion = 'reparacion'

    tipo = models.CharField(choices=TiposDeFoto.choices, max_length=50)

    def __str__(self):
        return f'{self.tipo}: {self.foto.path}'


class Respuesta(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    observacion = models.CharField(max_length=1500, blank=True)
    reparado = models.BooleanField()
    observacion_reparacion = models.CharField(max_length=1500, blank=True)
    momento_respuesta = models.DateTimeField(blank=True, null=True)

    @property
    def fotos_base(self):
        return self.fotos.filter(tipo=FotoRespuesta.TiposDeFoto.base)

    @property
    def fotos_reparacion(self):
        return self.fotos.filter(tipo=FotoRespuesta.TiposDeFoto.reparacion)

    class TiposDeRespuesta(models.TextChoices):
        cuadricula = 'cuadricula'
        seleccion_unica = 'seleccion_unica'
        seleccion_multiple = 'seleccion_multiple'
        parte_de_seleccion_multiple = 'parte_de_seleccion_multiple'
        numerica = 'numerica'

    tipo_de_respuesta = models.CharField(choices=TiposDeRespuesta.choices, max_length=50)

    # solo puede ser null cuando es parte de seleccion multiple
    pregunta = models.ForeignKey(Pregunta, null=True, on_delete=models.CASCADE, related_name='respuestas')

    # una y solo una de las siguientes tres debe ser no null
    # no null para las respuestas hijas de una respuesta de tipo cuadricula
    respuesta_cuadricula = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name='subrespuestas_cuadricula')

    # no null para las respuestas hijas de una respuesta de tipo seleccion multiple
    respuesta_multiple = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name='subrespuestas_multiple')

    # las respuestas que no son hijas de otras (cuadricula, seleccion unica, seleccion multiple y numerica) deben tener
    # inspeccion no null
    inspeccion = models.ForeignKey(Inspeccion, null=True, on_delete=models.CASCADE, related_name='respuestas')

    # no null para las respuestas tipo seleccion unica
    opcion_seleccionada = models.ForeignKey(OpcionDeRespuesta, null=True, on_delete=models.DO_NOTHING,
                                            related_name='respuestas_pregunta_de_seleccion_unica')

    # no null para las respuestas tipo parte de seleccion multiple
    opcion_respondida = models.ForeignKey(OpcionDeRespuesta, null=True, on_delete=models.DO_NOTHING,
                                          related_name='respuestas_pregunta_de_seleccion_multiple')

    # no null para las respuestas tipo parte de seleccion multiple
    opcion_respondida_esta_seleccionada = models.BooleanField(null=True)

    # no null para las respuestas tipo numerica
    valor_numerico = models.FloatField(null=True)

    class Meta:
        constraints = [
            # las contraints que referencian a otras tablas no se pueden aplicar aqui
            # TODO: crear los constraints descritos en los comentarios
            models.CheckConstraint(check=if_and_only_if(Q(tipo_de_respuesta='seleccion_unica'),
                                                        Q(opcion_seleccionada__isnull=False)),
                                   name='%(app_label)s_%(class)s_unica_respuesta'),
        ]
