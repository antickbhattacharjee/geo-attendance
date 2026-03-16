from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)

    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.IntegerField(default=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    user_id = models.CharField(max_length=10, unique=True, blank=True)
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        if not self.user_id:
            last_employee = Employee.objects.all().order_by('id').last()

            if not last_employee:
                self.user_id = "EMP0001"
            else:
                last_id = int(last_employee.user_id[3:])
                new_id = last_id + 1
                self.user_id = "EMP" + str(new_id).zfill(4)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.user_id})"