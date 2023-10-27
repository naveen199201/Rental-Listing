from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

TENANT='T'
LANDLORD='L'
ROLE_CHOICES= (
    (TENANT,'Tenant'),
    (LANDLORD,'Landlord'),
)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(null=True,max_length=1, choices=ROLE_CHOICES)
    phone_number=models.IntegerField(null=True)
    name = models.CharField(blank=True, max_length=255)
    def __str__(self):
        return self.email

class Property(models.Model):
    landlord=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    address = models.TextField()
    title= models.TextField(default='null')
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    rent = models.FloatField(default=0.0, null=True)
    
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.address

class Applicant(models.Model):
    tenant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="customer")
    address = models.ForeignKey(Property, on_delete=models.CASCADE)
    duration = models.CharField(max_length=50)
    
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "{}-{}".format(self.tenant.email, self.address)


