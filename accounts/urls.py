from django.urls import path
from . import views

urlpatterns = [

    # Employee
    path("user/login/", views.user_login),

    # Organization
    path("org/register/", views.org_register),
    path("org/login/", views.org_login),
    path("org/dashboard/", views.org_dashboard),
    path("org/logout/", views.org_logout),

    # Employee management
    path("org/employees/", views.employee_list),
    path("org/create-employee/", views.create_employee),

]