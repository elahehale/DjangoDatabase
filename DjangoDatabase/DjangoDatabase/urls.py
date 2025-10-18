# gamelog_proj/urls.py
from django.contrib import admin
from django.urls import path

from core.views import submit_log, get_by_id, export_logs_csv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/logs/', submit_log),
    path("api/<int:id>/", get_by_id , name="detail"),
    path("api/logs/export.csv", export_logs_csv),

]
