"""inspecciones_back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import logout_then_login
from django.http import HttpResponseRedirect
from django.urls import path, include, reverse
import inspecciones.urls
import inspecciones.views


def redirect_to_default(*args, **kwargs):
    return HttpResponseRedirect(reverse('lista_inspecciones'))


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
                  path('', redirect_to_default),
                  path('admin/', admin.site.urls),
                  path('accounts/register/', inspecciones.views.RegistrationView.as_view(), name="registro", ),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('logout/', logout_then_login, name='logout'),
                  path('home/', redirect_to_default, name='home'),
                  path('inspecciones/api/v1/', include(inspecciones.urls)),

                  path('inspecciones/', include([
                      path('', inspecciones.views.lista_inspecciones, name='lista_inspecciones'),
                      path('<int:inspeccion_id>/', redirect_to_default, name='detalle_inspeccion'),
                      path('estadisticas/', redirect_to_default, name='estadisticas'),
                      path('descargar_inspecciones/', redirect_to_default, name='descargar_inspecciones'),
                      path('formOtPadre/<str:pk>/', redirect_to_default, name='formOtPadre'),
                  ])),

                  path('organizaciones/', include([
                      path('', inspecciones.views.OrganizacionListView.as_view(), name='organizacion-list'),
                      path('mi-organizacion/', inspecciones.views.MiOrganizacionView.as_view(), name='mi-organizacion'),
                      path('<int:pk>/', inspecciones.views.OrganizacionDetailView.as_view(),
                           name='organizacion-detail'),

                      path('add/', inspecciones.views.OrganizacionCreateView.as_view(), name='organizacion-add'),
                      path('<int:pk>/update/', inspecciones.views.OrganizacionUpdateView.as_view(),
                           name='organizacion-update'),
                      path('<int:pk>/delete/', inspecciones.views.OrganizacionDeleteView.as_view(),
                           name='organizacion-delete'),

                  ])),

                  path('usuarios/', include([
                      # path('', inspecciones.views.OrganizacionListView.as_view(), name='organizacion-list'),
                      path('<int:pk>/', inspecciones.views.UsuarioDetailView.as_view(), name='usuario-detail'),
                      path('add/', inspecciones.views.UsuarioCreateView.as_view(), name='usuario-add'),
                      path('<int:pk>/update/', inspecciones.views.UsuarioUpdateView.as_view(), name='usuario-update'),
                      path('<int:pk>/delete/', inspecciones.views.UsuarioDeleteView.as_view(), name='usuario-delete'),
                  ])),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
