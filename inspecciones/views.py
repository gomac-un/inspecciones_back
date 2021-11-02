from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser

from rest_framework.response import Response
from rest_framework.settings import api_settings

from inspecciones.mixins import PutAsCreateMixin
from inspecciones.models import Perfil, Organizacion, Activo, Cuestionario, Inspeccion
from inspecciones.serializers import PerfilCreateSerializer, \
    OrganizacionSerializer, ActivoSerializer, CuestionarioSerializer, CuestionarioCompletoSerializer, \
    InspeccionCompletaSerializer, PerfilSerializer, SubirFotosSerializer, SubirFotosSerializer2, \
    SubirFotosCuestionarioSerializer, SubirFotosInspeccionSerializer


class OrganizacionViewSet(viewsets.ModelViewSet):
    queryset = Organizacion.objects.all()
    serializer_class = OrganizacionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def mi_organizacion(self, request):
        self.kwargs['pk'] = request.user.perfil.organizacion.pk
        return self.retrieve(request)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = PerfilSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        elif self.action in {'retrieve', 'list', 'destroy'}:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES
        return [permission() for permission in permission_classes]

    def get_parsers(self):
        """
        Instantiates and returns the list of parsers that this view can use.
        """
        if self.action == 'create':
            parser_classes = [MultiPartParser]
        else:
            parser_classes = api_settings.DEFAULT_PARSER_CLASSES

        return [parser() for parser in parser_classes]

    def initialize_request(self, request, *args, **kwargs):
        """Machete para que [get_permissions] pueda conocer [self.action] """
        self.action = self.action_map.get(request.method.lower())
        return super().initialize_request(request, *args, **kwargs)

    def get_queryset(self):
        # solo conoce los perfiles que pertenecen a la organizacion del perfil actual
        return Perfil.objects.filter(organizacion=self.request.user.perfil.organizacion)

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        if self.action == 'list':
            kwargs.setdefault('fields', ['id', 'nombre', 'foto', 'rol'])
        elif self.action in {'retrieve', 'mi_perfil'}:
            kwargs.setdefault('fields', ['id', 'esta_activo', 'fecha_registro', 'username', 'nombre', 'email', 'foto',
                                         'celular', 'organizacion', 'rol'])
        return serializer_class(*args, **kwargs)

    def create(self, request):
        serializer = PerfilCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        res = serializer.save()
        return Response(res, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        perfil = self.get_object()
        user = perfil.user
        self.perform_destroy(user)
        self.perform_destroy(perfil)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def mi_perfil(self, request):
        self.kwargs['pk'] = request.user.perfil.pk
        return self.retrieve(request)


class ActivoViewSet(PutAsCreateMixin, viewsets.ModelViewSet):
    def get_queryset(self):
        # solo muestra los activos que pertenecen a la organizacion del perfil actual
        return Activo.objects.filter(organizacion=self.request.user.perfil.organizacion)

    serializer_class = ActivoSerializer
    permission_classes = [permissions.IsAuthenticated]


class CuestionarioViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        # solo muestra los cuestionarios que pertenecen a la organizacion del perfil actual
        return Cuestionario.objects.filter(organizacion=self.request.user.perfil.organizacion)

    serializer_class = CuestionarioSerializer
    permission_classes = [permissions.IsAuthenticated]


class CuestionarioCompletoViewSet(CuestionarioViewSet):
    serializer_class = CuestionarioCompletoSerializer

    @action(detail=False, methods=['post'])
    def subir_fotos(self, request):
        serializer = SubirFotosCuestionarioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        res = serializer.save()
        return Response(res, status=status.HTTP_201_CREATED)


class InspeccionCompletaViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        # solo muestra las inspecciones de la organizacion del perfil actual
        return Inspeccion.objects.filter(cuestionario__organizacion=user.perfil.organizacion)

    serializer_class = InspeccionCompletaSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def subir_fotos(self, request):
        serializer = SubirFotosInspeccionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        res = serializer.save()
        return Response(res, status=status.HTTP_201_CREATED)

