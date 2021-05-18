from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone as tz
# Create your models here.

class Discussion(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    dis_type = models.CharField(choices=(("Helping",'Helping'),("Help Needed","Help Needed")),max_length=100)
    blood_grp = models.CharField(max_length=50,blank=True,null=True)
    phone_nos = models.CharField(max_length=100,blank=True,null=True)
    map_link = models.CharField(max_length=1000,blank=True,null=True)
    is_verified = models.CharField(choices=(("yes","Yes"),("no","No")),max_length=20,default="no")
    information = models.TextField()
    hashtags = models.TextField()
    timestamp = models.DateTimeField(default=tz.now)

    def __str__(self):
        return self.title

class DiscussionComment(models.Model):
    parent_dis = models.ForeignKey(Discussion,on_delete=models.CASCADE)
    user = models.CharField(max_length=1000)
    comment = models.TextField()
    timestamp = models.DateTimeField(default=tz.now)
    
    
class Plasma(models.Model):
    volunteer_verify = models.CharField(max_length=100, default="Unverified")
    plasma_donor_name = models.CharField(max_length=100)
    plasma_donor_email = models.CharField(max_length=100)
    plasma_donor_contact = models.CharField(max_length=100)
    plasma_donor_city= models.CharField(max_length=100)
    plasma_donor_bloodgroup = models.CharField(max_length=100)
    plasma_donor_age = models.IntegerField()
    plasma_donor_gender = models.CharField(max_length=100)
    plasma_donor_confirm = models.CharField(max_length=100)
    

    def __str__(self):
        return self.plasma_donor_name + " - "  + self.plasma_donor_city

class Oxygen(models.Model):
    volunteer_verify = models.CharField(max_length=100, default="Unverified")
    oxygen_lead_name = models.CharField(max_length=100)
    oxygen_lead_email = models.CharField(max_length=100)
    oxygen_lead_contact = models.CharField(max_length=100)
    oxygen_lead_city = models.CharField(max_length=100)
    oxygen_lead_address = models.CharField(max_length=500)
    oxygen_lead_verify = models.CharField(max_length=100)
    oxygen_lead_details = models.CharField(max_length=500)

    def __str__(self):
        return self.oxygen_lead_name + " - "  + self.oxygen_lead_city

class Injection(models.Model):
    volunteer_verify = models.CharField(max_length=100, default="Unverified")
    injection_lead_name = models.CharField(max_length=100)
    injection_lead_email = models.CharField(max_length=100)
    injection_lead_contact = models.CharField(max_length=100)
    injection_lead_city = models.CharField(max_length=100)
    injection_lead_address = models.CharField(max_length=500)
    injection_lead_drugname = models.CharField(max_length=100)
    injection_lead_verify = models.CharField(max_length=100)
    injection_lead_details = models.CharField(max_length=500)

    def __str__(self):
        return self.injection_lead_name + " - "  + self.injection_lead_city

class Food(models.Model):
    volunteer_verify = models.CharField(max_length=100, default="Unverified")
    food_supplier_name = models.CharField(max_length=100)
    food_supplier_email = models.CharField(max_length=100)
    food_supplier_contact = models.CharField(max_length=100)
    food_supplier_city = models.CharField(max_length=100)
    food_supplier_address = models.CharField(max_length=500)
    food_supplier_service = models.CharField(max_length=100)
    food_supplier_verify = models.CharField(max_length=100)
    food_supplier_details = models.CharField(max_length=500)

    def __str__(self):
        return self.food_supplier_name + " - "  + self.food_supplier_city

class Beds(models.Model):
    volunteer_verify = models.CharField(max_length=100, default="Unverified")
    hospital_name = models.CharField(max_length=100)
    hospital_contact = models.CharField(max_length=100)
    hospital_city = models.CharField(max_length=100)
    hospital_address = models.CharField(max_length=500)
    hospital_beds = models.CharField(max_length=100)
    hospital_verify = models.CharField(max_length=100)
    hospital_details = models.CharField(max_length=500)

    def __str__(self):
        return self.hospital_name + " - "  + self.hospital_city

class Volunteer(models.Model):
    volunteer_name = models.CharField(max_length=100)
    volunteer_email = models.CharField(max_length=100)
    volunteer_age = models.CharField(max_length=100)
    volunteer_phone = models.CharField(max_length=100)
    volunteer_hours = models.CharField(max_length=100)
    volunteer_aadhar = models.FileField(upload_to='vol_aadhar')
    volunteer_why = models.CharField(max_length=5000)

    def __str__(self):
        return self.volunteer_name