from django.shortcuts import render
from attendance.models import Attendance
from django.utils import timezone
from django.shortcuts import redirect
from .models import Organization
from .models import Employee, Organization
from accounts.models import Employee
from django.http import HttpResponse
import pandas as pd


def create_employee(request):

    org_id = request.session.get("org_id")

    if not org_id:
        return redirect("/org/login-org")

    if request.method == "POST":

        name = request.POST.get("name")
        password = request.POST.get("password")

        org = Organization.objects.get(id=org_id)

        Employee.objects.create(
            name=name,
            password=password,
            organization=org
        )

        return redirect("/org/employees")

    return render(request,"org/create_employee.html")

def employee_list(request):

    org_id = request.session.get("org_id")

    if not org_id:
        return redirect("/org/login-org")

    employees = Employee.objects.filter(organization_id=org_id)

    return render(request,"org/employees.html",{"employees":employees})


def org_register(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        lat = request.POST.get("latitude")
        lon = request.POST.get("longitude")
        radius = request.POST.get("radius")

        Organization.objects.create(
            name=name,
            email=email,
            password=password,
            latitude=lat,
            longitude=lon,
            radius=radius
        )

        return redirect("/org/login")

    return render(request, "org/register.html")

def org_login(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            org = Organization.objects.get(email=email, password=password)

            request.session["org_id"] = org.id

            return redirect("/org/dashboard/?name=&date=2026-03-14&start=&end=")

        except:
            return render(request,"org/login.html",{"error":"Invalid login"})

    return render(request,"org/login.html")


def org_dashboard(request):

    org_id = request.session.get("org_id")

    if not org_id:
        return redirect("/org/login")

    today = timezone.now().date()

    # Employees of this organization
    employees = Employee.objects.filter(organization_id=org_id)

    total_employees = employees.count()

    # Attendance today
    today_records = Attendance.objects.filter(
        employee__organization_id=org_id,
        date=today
    )

    present_ids = today_records.values_list("employee_id", flat=True)

    present_today = today_records.count()

    present_list = today_records

    absent_list = employees.exclude(id__in=present_ids)

    absent_today = absent_list.count()

    # Attendance history (for table)
    records = Attendance.objects.filter(employee__organization_id=org_id)

    # GET filters
    name = request.GET.get("name")
    date = request.GET.get("date")
    start = request.GET.get("start")
    end = request.GET.get("end")

    if name and name.strip():
        records = records.filter(employee__name__icontains=name.strip())

    if date:
        records = records.filter(date=date)

    if start and end:
        records = records.filter(date__range=[start, end])

    # Excel Export
    if "export" in request.GET:

        data = []

        for r in records:
            data.append({
                "Employee": r.employee.name,
                "Date": r.date,
                "Entry": r.entry_time.strftime("%H:%M:%S") if r.entry_time else "",
                "Exit": r.exit_time.strftime("%H:%M:%S") if r.exit_time else ""
            })

        df = pd.DataFrame(data)

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        response["Content-Disposition"] = 'attachment; filename="attendance.xlsx"'

        df.to_excel(response, index=False)

        return response

    return render(request, "org/dashboard.html", {
        "records": records,
        "employees": employees,
        "total_employees": total_employees,
        "present_today": present_today,
        "absent_today": absent_today,
        "present_list": present_list,
        "absent_list": absent_list
    })


def user_login(request):
    return render(request, "user/login.html")

def org_logout(request):
    request.session.flush()
    return redirect("/")