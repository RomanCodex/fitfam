from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.
class CustomUserManager(UserManager):
    def get_user_count(self):
        return self.model.objects.filter(is_client=True).count()
    
    def get_trainer_count(self):
        return self.model.objects.filter(is_trainer=True).count()

    def get_staff_count(self):
        return self.model.objects.filter(is_staff=True).count()


GENDER = (("M", "Male"), ("F", "Female"))
PLAN = (("S", "Silver"), ("G", "Gold"), ("C", "Couple"))

class User(AbstractUser):
    is_client = models.BooleanField(default=False)
    is_trainer = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    gender = models.CharField(max_length=1, choices=GENDER, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=60, blank=True, null=True)
    # picture = models.ImageField()
    email = models.EmailField(blank=True, null=True)
    objects = CustomUserManager()
    
    class Meta:
        ordering = ("-date_joined",)

    @property
    def get_full_name(self):
        full_name = self.username
        if self.first_name and self.last_name:
            full_name = self.first_name + " " + self.last_name
        return full_name

    def __str__(self):
        return "{} ({})".format(self.username, self.get_full_name)

    @property
    def get_user_role(self):
        if self.is_superuser:
            role = "Admin"
        if self.is_client:
            role = "Client"
        if self.is_trainer:
            role = "Trainer"
        if self.is_staff:
            role = "Staff"

        return role
    
    def get_absolute_url(self):
        return reverse("profile_single", kwargs={"id": self.id})
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

def Client(models.Model):
    client = models.OneToOneField(User, on_delete=models.CASCADE)
    id_number - models.CharField(max_length=20, unique=True, blank=True)
    goal = models.CharField(max_length=1024, blank=True, null=True)
    plan = models.CharField(max_length=1, choices=PLAN, blank=False, null=False)
    weight = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ("-client_date_joined",)

    def __str__(self):
        return self.client.get_full_name
    
    @classmethod
    def get_absolute_url(self):
        return reverse("profile_single", kwargs={"id": self.id})

    def delete(self, *args, **kwargs):
        self.student.delete()
        super().delete(*args, **kwargs)
    
