from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import csv
import random
import string
from django.http import HttpResponse
from RestaurantMonitoring.commons import *
from loguru import logger
import threading
logger.add("RestaurantMonitoring/logs",rotation="10 MB")

class TriggerReportView(APIView):
    def get(self, request, format=None):
        # Trigger the report generation
        report_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        print(report_id)
        # Start a background task to generate the report
        # generate_report(report_id)
        logger.info(f"Started Report Generation for {report_id}")
        threading.Thread(target=generate_report, args=(report_id,)).start()

        return Response({"report_id": report_id}, content_type='application/json')

class GetReportView(APIView):
    def get(self, request, report_id, format=None):
        # Check the status of the report
        status, report = check_report_status(report_id)
        if status == 'Complete':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{report_id}.csv"'
            writer = csv.writer(response)
            writer.writerow(['store_id', 'uptime_last_hour', 'uptime_last_day', 'uptime_last_week', 'downtime_last_hour', 'downtime_last_day', 'downtime_last_week'])
            for row in report:
                writer.writerow(row)
            return response
        else:
            return Response({"status": status})
