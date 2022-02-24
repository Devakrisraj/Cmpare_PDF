from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from . import views
#urlpatterns = [
#   url(r'^admin/', admin.site.urls),
 #  path("",views.home,name='home'),
# ]
#if settings.DEBUG:
#  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns = [path("",views.home, name='home'),
        url(r'^pdfcompare',views.pdfcompare, name='pdfcompare')]

if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)