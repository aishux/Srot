from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from .models import *
from django.core import serializers
from .filters import *
from django.db.models import Q

# ------------------------------------ Discusion Panel ----------------------------------------

def discussions(request):
    if request.method == "POST":
        title = request.POST.get("title")
        dis_type= request.POST.get("distype")
        information = request.POST.get("main_info")
        hashtags = request.POST.get("hashtags")
        blood_grp = request.POST.get("blood_group")
        phone_nos = request.POST.get("ph_nos")
        map_link = request.POST.get("location")
        is_verified = request.POST.get("verify_status")

        dis = Discussion(user=request.user,title=title,dis_type=dis_type,information=information,hashtags=hashtags,blood_grp=blood_grp,phone_nos=phone_nos,map_link=map_link,is_verified=is_verified)

        dis.save()

    params = {}


    # Get the page number passed in the url
    page_no = int(request.GET.get('page','1').replace("?",""))
    hashtag_filters = request.GET.get('tags',"")

    query = Q()

    if "Food" in hashtag_filters:
        query.add(Q(hashtags__icontains="Food"),Q.OR)
    
    if "Plasma" in hashtag_filters:
        query.add(Q(hashtags__icontains="Plasma"),Q.OR)
    
    if "Beds" in hashtag_filters:
        query.add(Q(hashtags__icontains="Beds"),Q.OR)

    if "Medicine" in hashtag_filters:
        query.add(Q(hashtags__icontains="Medicine"),Q.OR)
    
    if "Needhelp" in hashtag_filters:
        query.add(Q(dis_type="Help Needed"),Q.AND)
    
    elif "Helping" in hashtag_filters:
        query.add(Q(dis_type="Helping"),Q.AND)

    if "Verified" in hashtag_filters:
        query.add(Q(is_verified="yes"),Q.AND)

    filtered_discussions = Discussion.objects.filter(query)

    discussion_count = len(filtered_discussions)
    total_pages = discussion_count // 10
    if discussion_count % 10 != 0:
        total_pages += 1
    

    if page_no == 1:
        params["prev"] = ""
        params["actual_page"] = page_no
        params["next"] = min(page_no+1,total_pages)
        params["last_page"] = total_pages
    
    elif page_no == total_pages:
        params["prev"] = max(page_no-1,1)
        params["actual_page"] = page_no
        params["next"] = ""
        params["last_page"] = total_pages

    else:
        params["prev"] = max(page_no-1,1)
        params["actual_page"] = page_no
        params["next"] = min(page_no+1,total_pages)
        params["last_page"] = total_pages

    # Display 10 discussion per page
    from_range,to_range = (page_no-1)*10, page_no*10

    all_dis = filtered_discussions.order_by('-id')[from_range:to_range]

    params["all_dis"] = all_dis
    return render(request,'discussions.html',params)


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

# ------------------------------------ Lead Collection ----------------------------------------

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

# ------------------------------------ Lead Display ----------------------------------------

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

def filter(request):
    return render(request,'leads/filter.html')

# ------------------------------------ Home & Landing Page ----------------------------------------
def home(request):
    return render(request,'home.html')

def landing(request):
    return render(request,'volunteer/landing.html')

# ------------------------------------ Volunteer Data ----------------------------------------

def volfood(request):
    all_food = Food.objects.all()
    context = {'foods':all_food}
    return render(request,'volunteer/food.html',context)

def volbeds(request):
    all_beds = Beds.objects.all()
    context = {'beds':all_beds}
    return render(request,'volunteer/beds.html',context)

def volinjection(request):
    all_injs = Injection.objects.all()
    context = {'injs':all_injs}
    return render(request,'volunteer/injections.html',context)

def voloxygen(request):
    all_oxys = Oxygen.objects.all()
    context = {'oxys':all_oxys}
    return render(request,'volunteer/oxygen.html',context)

def volplasma(request):
    all_plass = Plasma.objects.all()
    context = {'plass':all_plass}
    return render(request,'volunteer/plasma.html',context)

# ------------------------------------ Volunteer Edit & Verify ----------------------------------------

def deleteLead(request,resource,id):
    deleted_item = 0
    if resource =='Food':
        deleted_item = Food.objects.filter(id=id)[0]
    elif resource =='Beds':
        deleted_item = Beds.objects.filter(id=id)[0]
    elif resource =='Oxygen':
        deleted_item = Oxygen.objects.filter(id=id)[0]
    elif resource =='Plasma':
        deleted_item = Plasma.objects.filter(id=id)[0]
    else:
        deleted_item = Injection.objects.filter(id=id)[0]
    deleted_item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

def verifyLead(request,resource,id):
    verified_item = 0
    if resource =='Food':
        verified_item = Food.objects.filter(id=id)[0]
    elif resource =='Beds':
        verified_item = Beds.objects.filter(id=id)[0]
    elif resource =='Oxygen':
        verified_item = Oxygen.objects.filter(id=id)[0]
    elif resource =='Plasma':
        verified_item = Plasma.objects.filter(id=id)[0]
    else:
        verified_item = Injection.objects.filter(id=id)[0]
    verified_item.volunteer_verify = 'Verified'
    verified_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

# ------------------------------------ Volunteer Food Edit ----------------------------------------

def editfood(request):
    if request.method == "POST":
        food_id = request.POST.get("form_id")
        food_supplier_name = request.POST.get("food_supplier_name")
        food_supplier_email = request.POST.get("food_supplier_email")
        food_supplier_contact = request.POST.get("food_supplier_contact")
        food_supplier_city = request.POST.get("food_supplier_city")
        food_supplier_address = request.POST.get("food_supplier_address")
        food_supplier_service = request.POST.get("food_supplier_service")
        food_supplier_details = request.POST.get("food_supplier_details")
        food_supplier_vol_verify = request.POST.get("food_supplier_vol_verify")

        ele = Food.objects.filter(id=food_id)[0]
        ele.food_supplier_name = food_supplier_name
        ele.food_supplier_email = food_supplier_email
        ele.food_supplier_contact = food_supplier_contact
        ele.food_supplier_city = food_supplier_city
        ele.food_supplier_address = food_supplier_address
        ele.food_supplier_service = food_supplier_service
        ele.food_supplier_details = food_supplier_details
        ele.volunteer_verify = food_supplier_vol_verify
        ele.save()

        return redirect('volfood')

    food_id = request.GET.get('food_id')[1:]
    food_details = Food.objects.filter(id=food_id).values()
    return JsonResponse({'details': list(food_details)})

# ------------------------------------ Volunteer Hospital Edit----------------------------------------

def edithospital(request):
    if request.method == "POST":
        hospital_id = request.POST.get("form_id")
        hospital_name = request.POST.get("hospital_name")
        hospital_contact = request.POST.get("hospital_contact")
        hospital_city = request.POST.get("hospital_city")
        hospital_address = request.POST.get("hospital_address")
        hospital_beds = request.POST.get("hospital_beds")
        hospital_details = request.POST.get("hospital_details")
        hospital_vol_verify = request.POST.get("hospital_vol_verify")

        ele = Beds.objects.filter(id=hospital_id)[0]
        ele.hospital_name = hospital_name
        ele.hospital_contact = hospital_contact
        ele.hospital_city = hospital_city
        ele.hospital_address = hospital_address
        ele.hospital_beds = hospital_beds
        ele.hospital_details = hospital_details
        ele.volunteer_verify = hospital_vol_verify
        ele.save()

        return redirect('volbeds')

    hospital_id = request.GET.get('hospital_id')[1:]
    hospital_details = Beds.objects.filter(id=hospital_id).values()
    return JsonResponse({'details': list(hospital_details)})


# ------------------------------------ Volunteer Plasma Edit----------------------------------------

def editplasma(request):
    if request.method == "POST":
        plasma_id = request.POST.get("form_id")
        plasma_donor_name = request.POST.get("plasma_donor_name")
        plasma_donor_email = request.POST.get("plasma_donor_email")
        plasma_donor_contact = request.POST.get("plasma_donor_contact")
        plasma_donor_city = request.POST.get("plasma_donor_city")
        plasma_donor_bloodgroup = request.POST.get("plasma_donor_bloodgroup")
        plasma_donor_age = request.POST.get("plasma_donor_age")
        plasma_donor_gender = request.POST.get("plasma_donor_gender")
        plasma_vol_verify = request.POST.get("plasma_vol_verify")

        ele = Plasma.objects.filter(id=plasma_id)[0]
        ele.plasma_donor_name = plasma_donor_name
        ele.plasma_donor_email = plasma_donor_email
        ele.plasma_donor_contact = plasma_donor_contact
        ele.plasma_donor_city = plasma_donor_city
        ele.plasma_donor_bloodgroup = plasma_donor_bloodgroup
        ele.plasma_donor_age = plasma_donor_age
        ele.plasma_donor_gender = plasma_donor_gender
        ele.volunteer_verify = plasma_vol_verify
        ele.save()

        return redirect('volplasma')

    plasma_id = request.GET.get('plasma_id')[1:]
    plasma_details = Plasma.objects.filter(id=plasma_id).values()
    return JsonResponse({'details': list(plasma_details)})
  

# ------------------------------------ Volunteer Medicine Edit----------------------------------------

def editinjection(request):
    if request.method == "POST":
        injection_id = request.POST.get("form_id")
        injection_lead_name = request.POST.get("injection_lead_name")
        injection_lead_email = request.POST.get("injection_lead_email")
        injection_lead_contact = request.POST.get("injection_lead_contact")
        injection_lead_city = request.POST.get("injection_lead_city")
        injection_lead_address = request.POST.get("injection_lead_address")
        injection_lead_drugname = request.POST.get("injection_lead_drugname")
        injection_lead_details = request.POST.get("injection_lead_details")
        injection_vol_verify = request.POST.get("injection_vol_verify")

        ele = Injection.objects.filter(id=injection_id)[0]
        ele.injection_lead_name = injection_lead_name
        ele.injection_lead_email = injection_lead_email
        ele.injection_lead_contact = injection_lead_contact
        ele.injection_lead_city = injection_lead_city
        ele.injection_lead_address = injection_lead_address
        ele.injection_lead_drugname = injection_lead_drugname
        ele.injection_lead_details = injection_lead_details
        ele.volunteer_verify = injection_vol_verify
        ele.save()

        return redirect('volinjection')

    injection_id = request.GET.get('injection_id')[1:]
    injection_details = Injection.objects.filter(id=injection_id).values()
    return JsonResponse({'details': list(injection_details)})


# ------------------------------------ Volunteer Oxygen Edit----------------------------------------

def editoxygen(request):
    if request.method == "POST":
        oxygen_id = request.POST.get("form_id")
        oxygen_lead_name = request.POST.get("oxygen_lead_name")
        oxygen_lead_email = request.POST.get("oxygen_lead_email")
        oxygen_lead_contact = request.POST.get("oxygen_lead_contact")
        oxygen_lead_city = request.POST.get("oxygen_lead_city")
        oxygen_lead_address = request.POST.get("oxygen_lead_address")
        oxygen_lead_details = request.POST.get("oxygen_lead_details")
        oxygen_vol_verify = request.POST.get("oxygen_vol_verify")

        ele = Oxygen.objects.filter(id=oxygen_id)[0]
        ele.oxygen_lead_name = oxygen_lead_name
        ele.oxygen_lead_email = oxygen_lead_email
        ele.oxygen_lead_contact = oxygen_lead_contact
        ele.oxygen_lead_city = oxygen_lead_city
        ele.oxygen_lead_address = oxygen_lead_address
        ele.oxygen_lead_details = oxygen_lead_details
        ele.volunteer_verify = oxygen_vol_verify
        ele.save()

        return redirect('voloxygen')

    oxygen_id = request.GET.get('oxygen_id')[1:]
    oxygen_details = Oxygen.objects.filter(id=oxygen_id).values()
    return JsonResponse({'details': list(oxygen_details)})