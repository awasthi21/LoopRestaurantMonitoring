from django.urls import path
from .views import TriggerReportView, GetReportView

urlpatterns = [
    path('generate-report/', TriggerReportView.as_view(), name='generate_report'),
    path('get-report/<str:report_id>/', GetReportView.as_view(), name='get_report'),
]

