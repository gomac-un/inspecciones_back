from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from inspecciones.models import Organizacion, Inspeccion, Perfil


@login_required(login_url="login")
def lista_inspecciones(request):
    inspecciones = Inspeccion.objects.all().order_by('-momento_subida')
    context = {'finalizadas': inspecciones}
    return render(request, 'inspecciones/list_inspecciones.html', context)


class OrganizacionListView(ListView):
    model = Organizacion


class OrganizacionDetailView(DetailView):
    model = Organizacion

    def get_context_data(self, **kwargs):
        """Agrega todas las caracteristicas."""
        context = {'caracteristicas': Organizacion.Caracteristicas.values}
        context.update(kwargs)
        return super().get_context_data(**context)


class OrganizacionCreateView(CreateView):
    model = Organizacion
    fields = ['nombre', 'logo', 'link', 'acerca', 'caracteristicas']


class OrganizacionUpdateView(UpdateView):
    model = Organizacion
    fields = ['nombre', 'logo', 'link', 'acerca', 'caracteristicas']


class OrganizacionDeleteView(DeleteView):
    model = Organizacion
    success_url = reverse_lazy('organizacion-list')


class UsuarioDetailView(DetailView):
    model = Perfil


class UsuarioCreateView(CreateView):
    model = Perfil
    fields = ['nombre', 'logo', 'link', 'acerca']


class UsuarioUpdateView(UpdateView):
    model = Perfil
    fields = ['nombre', 'logo', 'link', 'acerca']


class UsuarioDeleteView(DeleteView):
    model = Perfil
    success_url = reverse_lazy('organizacion-list')
