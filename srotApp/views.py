from django.shortcuts import render, redirect
from .models import *

# Create your views here.

def discussions(request):
    if request.method == "POST":
        user = User.objects.filter(username="srot")[0]
        title = request.POST.get("title")
        dis_type= request.POST.get("distype")
        information = request.POST.get("main_info")
        hashtags = request.POST.get("hashtags")

        dis = Discussion(user=user,title=title,dis_type=dis_type,information=information,hashtags=hashtags)

        dis.save()

    all_dis = Discussion.objects.all()

    return render(request,'discussions.html',{"all_dis":all_dis})

def sidebar(request):
    return render(request,'donations/sidebar.html')

def plasma(request):
    if request.method == "POST":
        plasma_donor_name = request.POST.get("plasma_donor_name")
        plasma_donor_email = request.POST.get("plasma_donor_email")
        plasma_donor_contact = request.POST.get("plasma_donor_contact")
        plasma_donor_city = request.POST.get("plasma_donor_city")
        plasma_donor_bloodgroup = request.POST.get("plasma_donor_bloodgroup")
        plasma_donor_age = request.POST.get("plasma_donor_age")
        plasma_donor_gender = request.POST.get("plasma_donor_gender")
        plasma_donor_confirm = request.POST.get("plasma_donor_confirm")

        plas = Plasma(plasma_donor_name=plasma_donor_name , plasma_donor_email= plasma_donor_email, plasma_donor_contact=plasma_donor_contact, plasma_donor_bloodgroup=plasma_donor_bloodgroup, plasma_donor_age=plasma_donor_age, plasma_donor_gender=plasma_donor_gender, plasma_donor_confirm=plasma_donor_confirm)
        plas.save()
        
    all_plas = Plasma.objects.all()

    return render(request,'donations/plasma.html',{"all_plas":all_plas})

def oxygen(request):
    if request.method == "POST":
        oxygen_lead_name = request.POST.get("oxygen_lead_name")
        oxygen_lead_email = request.POST.get("oxygen_lead_email")
        oxygen_lead_contact = request.POST.get("oxygen_lead_contact")
        oxygen_lead_city = request.POST.get("oxygen_lead_city")
        oxygen_lead_verify = request.POST.get("oxygen_lead_verify")
        oxygen_lead_details = request.POST.get("oxygen_lead_details")

        oxy = Oxygen(oxygen_lead_name=oxygen_lead_name, oxygen_lead_email=oxygen_lead_email, oxygen_lead_contact=oxygen_lead_contact, oxygen_lead_city=oxygen_lead_city, oxygen_lead_verify=oxygen_lead_verify, oxygen_lead_details=oxygen_lead_details)
        oxy.save()
        
    all_oxy = Oxygen.objects.all()

    return render(request,'donations/oxygen.html',{"all_oxy":all_oxy})

def injections(request):
    if request.method == "POST":
        injection_lead_name = request.POST.get("injection_lead_name")
        injection_lead_email = request.POST.get("injection_lead_email")
        injection_lead_contact = request.POST.get("injection_lead_contact")
        injection_lead_city = request.POST.get("injection_lead_city")
        injection_lead_drugname = request.POST.get("injection_lead_drugname")
        injection_lead_verify = request.POST.get("injection_lead_verify")
        injection_lead_details = request.POST.get("injection_lead_details")

        inj = Injection(injection_lead_name=injection_lead_name, injection_lead_email=injection_lead_email, injection_lead_contact=injection_lead_contact, injection_lead_city=injection_lead_city, injection_lead_drugname=injection_lead_drugname, injection_lead_verify=injection_lead_verify, injection_lead_details=injection_lead_details)
        inj.save()
        
    all_inj = Injection.objects.all()

    return render(request,'donations/injections.html',{"all_inj":all_inj})

def food(request):
    if request.method == "POST":
        food_supplier_name = request.POST.get("food_supplier_name")
        food_supplier_email = request.POST.get("food_supplier_email")
        food_supplier_contact = request.POST.get("food_supplier_contact")
        food_supplier_city = request.POST.get("food_supplier_city")
        food_supplier_service = request.POST.get("food_supplier_service")
        food_supplier_verify = request.POST.get("food_supplier_verify")
        food_supplier_details = request.POST.get("food_supplier_details")

        food = Food(food_supplier_name=food_supplier_name, food_supplier_email=food_supplier_email, food_supplier_contact=food_supplier_contact, food_supplier_city=food_supplier_city, food_supplier_service=food_supplier_service, food_supplier_verify=food_supplier_verify, food_supplier_details=food_supplier_details)
        food.save()
        
    all_food = Food.objects.all()

    return render(request,'donations/food.html',{"all_food":all_food})

def beds(request):
    if request.method == "POST":
        hospital_name = request.POST.get("hospital_name")
        hospital_contact = request.POST.get("hospital_contact")
        hospital_city = request.POST.get("hospital_city")
        hospital_address = request.POST.get("hospital_address")
        hospital_beds = request.POST.get("hospital_beds")
        hospital_verify = request.POST.get("hospital_verify")
        hospital_details = request.POST.get("hospital_details")

        beds = Beds(hospital_name=hospital_name, hospital_contact=hospital_contact, hospital_city=hospital_city, hospital_address=hospital_address, hospital_beds=hospital_beds, hospital_verify=hospital_verify, hospital_details=hospital_details)
        beds.save()
    all_beds = Beds.objects.all()

    return render(request,'donations/beds.html',{"all_beds":all_beds})