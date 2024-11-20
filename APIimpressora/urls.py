
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 
from file_upload.views import FileUploadView, PrinterListView




urlpatterns = [
    path('admin/', admin.site.urls),
    path('file-upload/', include('file_upload.urls')),
    path('api/upload/',FileUploadView.as_view(), name='file-upload'),
    path('api/printers/', PrinterListView.as_view(), name='printer-list'),
    path('', PrinterListView.as_view(), name='root'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    