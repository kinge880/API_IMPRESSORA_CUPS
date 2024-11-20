from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArquivoViewSet, FileUploadView, PrinterListView, DeletedTempFilesView, PrintersStatusViews

router = DefaultRouter()
router.register(r'arquivos', ArquivoViewSet, basename='arquivo')

urlpatterns = [
    path('api/upload/', FileUploadView.as_view(), name='file-upload'),
    path('api/printer-status/<str:printer_name>/', PrintersStatusViews.as_view(), name='printer-status'),
    path('api/printers/', PrinterListView.as_view(), name='printer-list'),
    path('deleted-temp-files/', DeletedTempFilesView.as_view(), name='delete_temp_files'),
    path('', PrinterListView.as_view(), name='root'),
    path('api/', include(router.urls)),
]