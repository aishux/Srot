from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from django.core import serializers
from .filters import *

# Create your views here.

def discussions(request):
    if request.method == "POST":
        title = request.POST.get("title")
        dis_type= request.POST.get("distype")
        information = request.POST.get("main_info")
        hashtags = request.POST.get("hashtags")
        blood_grp = request.POST.get("blood_group")
        phone_nos = request.POST.get("ph_nos")
        map_link = request.POST.get("location")

        dis = Discussion(user=request.user,title=title,dis_type=dis_type,information=information,hashtags=hashtags,blood_grp=blood_grp,phone_nos=phone_nos,map_link=map_link)

        dis.save()

    all_dis = Discussion.objects.all()

    return render(request,'discussions.html',{"all_dis":all_dis})

def saveDiscussionComment(request):
    dis_id = request.GET.get("dis_id")
    given_comment = request.GET.get("comment")

    parent_discussion = Discussion.objects.filter(id=dis_id)[0]

    comm = DiscussionComment(parent_dis=parent_discussion,user=request.user.username,comment=given_comment)

    comm.save()

    return JsonResponse({"user_name":request.user.username})

def showComments(request):
    discussion_id = request.GET.get("dis_id")
    parent_discussion = Discussion.objects.filter(id=discussion_id)[0]

    params = {}

    all_comments = DiscussionComment.objects.filter(parent_dis=parent_discussion)

    # If there are no comments
    if not all_comments:
        params["has_comments"] = "no"
    
    # If there exists comments
    else:
        params["has_comments"] = "yes"

        # We serialize data to pass it in json friendly format
        params["all_comments"] = serializers.serialize('json',all_comments)

    return JsonResponse(params)


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

        plas = Plasma(plasma_donor_name=plasma_donor_name , plasma_donor_email= plasma_donor_email, plasma_donor_contact=plasma_donor_contact, plasma_donor_bloodgroup=plasma_donor_bloodgroup, plasma_donor_age=plasma_donor_age, plasma_donor_gender=plasma_donor_gender.capitalize(), plasma_donor_confirm=plasma_donor_confirm,plasma_donor_city=plasma_donor_city.capitalize())
        plas.save()
        
    all_plas = Plasma.objects.all()

    return render(request,'donations/plasma.html',{"all_plas":all_plas})

def oxygen(request):
    if request.method == "POST":
        oxygen_lead_name = request.POST.get("oxygen_lead_name")
        oxygen_lead_email = request.POST.get("oxygen_lead_email")
        oxygen_lead_contact = request.POST.get("oxygen_lead_contact")
        oxygen_lead_city = request.POST.get("oxygen_lead_city")
        oxygen_lead_address = request.POST.get("oxygen_lead_address")
        oxygen_lead_verify = request.POST.get("oxygen_lead_verify")
        oxygen_lead_details = request.POST.get("oxygen_lead_details")

        oxy = Oxygen(oxygen_lead_name=oxygen_lead_name, oxygen_lead_email=oxygen_lead_email, oxygen_lead_contact=oxygen_lead_contact, oxygen_lead_city=oxygen_lead_city.capitalize(), oxygen_lead_address=oxygen_lead_address, oxygen_lead_verify=oxygen_lead_verify, oxygen_lead_details=oxygen_lead_details)
        oxy.save()
        
    all_oxy = Oxygen.objects.all()

    return render(request,'donations/oxygen.html',{"all_oxy":all_oxy})

def injections(request):
    if request.method == "POST":
        injection_lead_name = request.POST.get("injection_lead_name")
        injection_lead_email = request.POST.get("injection_lead_email")
        injection_lead_contact = request.POST.get("injection_lead_contact")
        injection_lead_city = request.POST.get("injection_lead_city")
        injection_lead_address = request.POST.get("injection_lead_address")
        injection_lead_drugname = request.POST.get("injection_lead_drugname")
        injection_lead_verify = request.POST.get("injection_lead_verify")
        injection_lead_details = request.POST.get("injection_lead_details")

        inj = Injection(injection_lead_name=injection_lead_name, injection_lead_email=injection_lead_email, injection_lead_contact=injection_lead_contact, injection_lead_city=injection_lead_city.capitalize(), injection_lead_address=injection_lead_address, injection_lead_drugname=injection_lead_drugname, injection_lead_verify=injection_lead_verify, injection_lead_details=injection_lead_details)
        inj.save()
        
    all_inj = Injection.objects.all()

    return render(request,'donations/injections.html',{"all_inj":all_inj})

def food(request):
    if request.method == "POST":
        food_supplier_name = request.POST.get("food_supplier_name")
        food_supplier_email = request.POST.get("food_supplier_email")
        food_supplier_contact = request.POST.get("food_supplier_contact")
        food_supplier_city = request.POST.get("food_supplier_city")
        food_supplier_address = request.POST.get("food_supplier_address")
        food_supplier_service = request.POST.get("food_supplier_service")
        food_supplier_verify = request.POST.get("food_supplier_verify")
        food_supplier_details = request.POST.get("food_supplier_details")

        food = Food(food_supplier_name=food_supplier_name, food_supplier_email=food_supplier_email, food_supplier_contact=food_supplier_contact, food_supplier_city=food_supplier_city.capitalize(), food_supplier_address=food_supplier_address, food_supplier_service=food_supplier_service, food_supplier_verify=food_supplier_verify, food_supplier_details=food_supplier_details)
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

        beds = Beds(hospital_name=hospital_name, hospital_contact=hospital_contact, hospital_city=hospital_city.capitalize(), hospital_address=hospital_address, hospital_beds=hospital_beds, hospital_verify=hospital_verify, hospital_details=hospital_details)
        beds.save()
    all_beds = Beds.objects.all()

    return render(request,'donations/beds.html',{"all_beds":all_beds})

def tables(request):
    all_food = Food.objects.all()
    foodFilter = FoodFilter()
    context = {'foods':all_food}
    return render(request,'tables.html', context)

def foodleads(request):
    all_food = Food.objects.all()
    foodFilter = FoodFilter()
    context = {'foods':all_food}
    return render(request,'leads/foodleads.html', context)

def bedleads(request):
    all_beds = Beds.objects.all()
    context = {'beds':all_beds}
    return render(request,'leads/bedleads.html', context)

def injectionleads(request):
    all_inj = Injection.objects.all()
    context = {'injs':all_inj}
    return render(request,'leads/injectionleads.html', context)

def oxygenleads(request):
    all_oxy = Oxygen.objects.all()
    context = {'oxys':all_oxy}
    return render(request,'leads/oxygenleads.html', context)

def plasmaleads(request):
    all_plasma = Plasma.objects.all()
    context = {'plasmas':all_plasma}
    return render(request,'leads/plasmaleads.html', context)