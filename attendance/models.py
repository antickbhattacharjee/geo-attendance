from django.db import models
from accounts.models import Employee, Organization


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    date = models.DateField(auto_now_add=True)

    entry_time = models.DateTimeField(null=True, blank=True)
    exit_time = models.DateTimeField(null=True, blank=True)

    entry_lat = models.FloatField(null=True, blank=True)
    entry_long = models.FloatField(null=True, blank=True)

    exit_lat = models.FloatField(null=True, blank=True)
    exit_long = models.FloatField(null=True, blank=True)

    status = models.CharField(max_length=20, default="Present")

    def __str__(self):
        return f"{self.employee.name} - {self.date}"