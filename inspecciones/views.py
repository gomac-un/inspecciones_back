from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View

from inspecciones.forms import PerfilForm, UserForm
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


class MiOrganizacionView(OrganizacionDetailView):
    def get_object(self, queryset=None):
        self.kwargs[self.pk_url_kwarg] = self.request.user.perfil.organizacion.pk
        return super().get_object(queryset)


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


class RegistrationView(TemplateResponseMixin, ContextMixin, View):
    template_name = "django_registration/registration_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add blank forms to context with prefixes
        context["form_user"] = UserForm(prefix="user_form")
        context["form_perfil"] = PerfilForm(prefix="perfil_form")
        return context

    def get(self, request, *args, **kwargs):
        if "org" not in self.request.GET:
            return HttpResponseBadRequest(b'No organizacion_id provided.')

        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        try:
            organizacion_id = self.request.GET["org"]
        except MultiValueDictKeyError:
            return HttpResponseBadRequest(b'No organizacion_id provided.')
        context = self.get_context_data()
        # Process forms
        form_user = UserForm(request.POST, prefix="user_form")
        form_perfil = PerfilForm(request.POST, prefix="perfil_form")
        if form_user.is_valid() and form_perfil.is_valid():
            # Save user
            new_user = form_user.save(commit=False)
            new_user.first_name = form_user.cleaned_data["nombre"]
            new_user.last_name = form_user.cleaned_data["apellido"]
            new_user.save()
            # Save profile
            new_perfil = form_perfil.save(commit=False)
            new_perfil.user = new_user
            new_perfil.organizacion = Organizacion.objects.get(pk=organizacion_id)
            new_perfil.rol = Perfil.Roles.inspector
            new_perfil.save()
            # Redirect to success page
            return HttpResponseRedirect(reverse("login"))
        else:
            # overwrite context data for this form so that it is   \
            # returned to the page with validation errors
            context["form_user"] = form_user
            context["form_perfil"] = form_perfil

        # Pass context back to render_to_response() including any invalid forms
        return self.render_to_response(context)
