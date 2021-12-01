from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View

from inspecciones.forms import PerfilForm, UserForm, UserEditForm, PerfilEditForm
from inspecciones.models import Organizacion, Inspeccion, Perfil, Activo


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


class UsuarioUpdateView(TemplateResponseMixin, ContextMixin, View):
    """adaptado de https://stackoverflow.com/a/65847099/5076677"""

    template_name = "inspecciones/usuario_form.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        perfil = Perfil.objects.get(pk=self.kwargs['pk'])
        context["form_user"] = UserEditForm(prefix="user_form", instance=perfil.user)
        context["form_perfil"] = PerfilEditForm(prefix="perfil_form", instance=perfil)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        perfil = Perfil.objects.get(pk=self.kwargs['pk'])
        # Process forms
        form_user = UserEditForm(request.POST, prefix="user_form", instance=perfil.user)
        form_perfil = PerfilEditForm(request.POST, prefix="perfil_form", instance=perfil)
        if form_user.is_valid() and form_perfil.is_valid():
            # Save user
            form_user.save()
            # Save profile
            form_perfil.save()
            # Redirect to success page
            return HttpResponseRedirect(reverse("mi-organizacion"))
        else:
            # overwrite context data for this form so that it is   \
            # returned to the page with validation errors
            context["form_user"] = form_user
            context["form_perfil"] = form_perfil

        # Pass context back to render_to_response() including any invalid forms
        return self.render_to_response(context)


class UsuarioDeleteView(DeleteView):
    model = Perfil
    success_url = reverse_lazy('mi-organizacion')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.user.delete()
        return HttpResponseRedirect(success_url)


class RegistrationView(TemplateResponseMixin, ContextMixin, View):
    """adaptado de https://stackoverflow.com/a/65847099/5076677"""

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


class InspeccionListView(ListView):
    def get_queryset(self):
        return Inspeccion.objects.filter(cuestionario__organizacion=self.request.user.perfil.organizacion) \
            .order_by('-momento_inicio')


class InspeccionDetailView(DetailView):
    model = Inspeccion
    pk_url_kwarg = 'inspeccion_id'


class ActivoListView(ListView):
    def get_queryset(self):
        return Activo.objects.filter(organizacion=self.request.user.perfil.organizacion)
