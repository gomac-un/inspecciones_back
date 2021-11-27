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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponseRedirect
from django.urls import path, include, reverse
import inspecciones.urls
import inspecciones.views


def redirect_to_default(request, *args, **kwargs):
    return HttpResponseRedirect(reverse('lista_inspecciones'))


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
                  path('home/', lambda request: HttpResponseRedirect(reverse('lista_inspecciones')), name='home'),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('inspecciones/', inspecciones.views.lista_inspecciones, name='lista_inspecciones'),
                  path('inspecciones/<int:inspeccion_id>/', redirect_to_default, name='detalle_inspeccion'),
                  path('inspecciones/estadisticas', redirect_to_default, name='estadisticas'),
                  path('inspecciones/descargar_inspecciones/', redirect_to_default, name='descargar_inspecciones'),
                  path('inspecciones/formOtPadre/<str:pk>/', redirect_to_default, name='formOtPadre'),
                  path('inspecciones/api/v1/', include(inspecciones.urls)),
                  path('admin/', admin.site.urls),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
