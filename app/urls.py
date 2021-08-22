from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from usuarios import urls
from usuarios.views import chekLoginView, index

urlpatterns = [
                  path('', chekLoginView),
                  path('index/', index),
                  path('admin/', admin.site.urls),
                  path('usuarios/', include(urls)),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
