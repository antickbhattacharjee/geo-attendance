from django.utils import timezone
from django.http import JsonResponse
from accounts.models import Employee
from .models import Attendance
import math


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)

    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(delta_lambda/2)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R*c


def mark_entry(request):

    user_id = request.POST.get("user_id")
    password = request.POST.get("password")
    lat = float(request.POST.get("latitude"))
    lon = float(request.POST.get("longitude"))

    try:
        employee = Employee.objects.get(user_id=user_id, password=password)
    except Employee.DoesNotExist:
        return JsonResponse({"status": "Invalid Employee ID or Password"})

    org = employee.organization
    today = timezone.now().date()

    already_marked = Attendance.objects.filter(
        employee=employee,
        date=today
    ).first()

    if already_marked:
        return JsonResponse({"status": "Entry already marked today"})

    distance = calculate_distance(lat, lon, org.latitude, org.longitude)

    if distance <= org.radius:

        Attendance.objects.create(
            employee=employee,
            organization=org,
            entry_time=timezone.now(),
            entry_lat=lat,
            entry_long=lon
        )

        return JsonResponse({"status": "Entry Marked Successfully"})

    return JsonResponse({"status": "Outside Office Location"})

def mark_exit(request):

    user_id = request.POST.get("user_id")
    password = request.POST.get("password")
    lat = float(request.POST.get("latitude"))
    lon = float(request.POST.get("longitude"))

    try:
        employee = Employee.objects.get(user_id=user_id, password=password)
    except Employee.DoesNotExist:
        return JsonResponse({"status": "Invalid Employee ID or Password"})

    today = timezone.now().date()

    attendance = Attendance.objects.filter(
        employee=employee,
        date=today
    ).first()

    if not attendance:
        return JsonResponse({"status": "Entry not marked yet"})

    if attendance.exit_time:
        return JsonResponse({"status": "Exit already marked"})

    attendance.exit_time = timezone.now()
    attendance.exit_lat = lat
    attendance.exit_long = lon
    attendance.save()

    return JsonResponse({"status": "Exit Marked Successfully"})