from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect,HttpResponse
from .models import *
from django.core import serializers
from .filters import *
from django.db.models import Q
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.core.mail import BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from email.message import EmailMessage
import smtplib
from .validators import validate_is_pdf
from django.core.exceptions import ValidationError
from itertools import chain
# ------------------------------------ Pagination ----------------------------------------
def pagination(resource,var_type,page_no):
    if page_no == 0:
        return 0
    params = {}
    discussion_count = len(resource)
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

    all_dis = resource[from_range:to_range]

    params[var_type] = all_dis

    params["items_length"] = len(all_dis)

    return params

# ------------------------------------ Discusion Panel ----------------------------------------

def discussions(request):
    if request.method == "POST":
        
        if not request.user.is_authenticated:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
        
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

    filtered_discussions = Discussion.objects.filter(query).order_by('-id')

    params = pagination(filtered_discussions,"all_dis",page_no)
    return render(request,'discussions.html',params)


def saveDiscussionComment(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

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
        plasma_donor_state = request.POST.get("plasma_donor_state")
        plasma_donor_city = request.POST.get("plasma_donor_city").strip()
        plasma_donor_bloodgroup = request.POST.get("plasma_donor_bloodgroup")
        plasma_donor_age = request.POST.get("plasma_donor_age")
        plasma_donor_gender = request.POST.get("plasma_donor_gender")
        plasma_donor_confirm = request.POST.get("plasma_donor_confirm")

        plas = Plasma(plasma_donor_name=plasma_donor_name , plasma_donor_email= plasma_donor_email, plasma_donor_contact=plasma_donor_contact, plasma_donor_bloodgroup=plasma_donor_bloodgroup, plasma_donor_age=plasma_donor_age, plasma_donor_gender=plasma_donor_gender.capitalize(), plasma_donor_confirm=plasma_donor_confirm,plasma_donor_city=plasma_donor_city,plasma_donor_state=plasma_donor_state)
        plas.save()
        
    all_plas = Plasma.objects.all()

    return render(request,'donations/plasma.html',{"all_plas":all_plas})

def oxygen(request):
    if request.method == "POST":
        oxygen_lead_name = request.POST.get("oxygen_lead_name")
        oxygen_lead_email = request.POST.get("oxygen_lead_email")
        oxygen_lead_contact = request.POST.get("oxygen_lead_contact")
        oxygen_lead_state = request.POST.get("oxygen_lead_state")
        oxygen_lead_city = request.POST.get("oxygen_lead_city").strip()
        oxygen_lead_address = request.POST.get("oxygen_lead_address")
        oxygen_lead_verify = request.POST.get("oxygen_lead_verify")
        oxygen_lead_details = request.POST.get("oxygen_lead_details")

        oxy = Oxygen(oxygen_lead_name=oxygen_lead_name, oxygen_lead_email=oxygen_lead_email, oxygen_lead_contact=oxygen_lead_contact, oxygen_lead_city=oxygen_lead_city, oxygen_lead_address=oxygen_lead_address, oxygen_lead_verify=oxygen_lead_verify, oxygen_lead_details=oxygen_lead_details,oxygen_lead_state=oxygen_lead_state)
        oxy.save()
        
    all_oxy = Oxygen.objects.all()

    return render(request,'donations/oxygen.html',{"all_oxy":all_oxy})

def injections(request):
    if request.method == "POST":
        injection_lead_name = request.POST.get("injection_lead_name")
        injection_lead_email = request.POST.get("injection_lead_email")
        injection_lead_contact = request.POST.get("injection_lead_contact")
        injection_lead_state = request.POST.get("injection_lead_state")
        injection_lead_city = request.POST.get("injection_lead_city").strip()
        injection_lead_address = request.POST.get("injection_lead_address")
        injection_lead_drugname = request.POST.get("injection_lead_drugname")
        injection_lead_verify = request.POST.get("injection_lead_verify")
        injection_lead_details = request.POST.get("injection_lead_details")

        inj = Injection(injection_lead_name=injection_lead_name, injection_lead_email=injection_lead_email, injection_lead_contact=injection_lead_contact, injection_lead_city=injection_lead_city, injection_lead_address=injection_lead_address, injection_lead_drugname=injection_lead_drugname, injection_lead_verify=injection_lead_verify, injection_lead_details=injection_lead_details,injection_lead_state=injection_lead_state)
        inj.save()
        
    all_inj = Injection.objects.all()

    return render(request,'donations/injections.html',{"all_inj":all_inj})

def food(request):
    if request.method == "POST":
        food_supplier_name = request.POST.get("food_supplier_name")
        food_supplier_email = request.POST.get("food_supplier_email")
        food_supplier_contact = request.POST.get("food_supplier_contact")
        food_supplier_state = request.POST.get("food_supplier_state")
        food_supplier_city = request.POST.get("food_supplier_city").strip()
        food_supplier_address = request.POST.get("food_supplier_address")
        food_supplier_service = request.POST.get("food_supplier_service")
        food_supplier_verify = request.POST.get("food_supplier_verify")
        food_supplier_details = request.POST.get("food_supplier_details")

        food = Food(food_supplier_name=food_supplier_name, food_supplier_email=food_supplier_email, food_supplier_contact=food_supplier_contact, food_supplier_city=food_supplier_city, food_supplier_address=food_supplier_address, food_supplier_service=food_supplier_service, food_supplier_verify=food_supplier_verify, food_supplier_details=food_supplier_details,food_supplier_state=food_supplier_state)
        food.save()
        
    all_food = Food.objects.all()

    return render(request,'donations/food.html',{"all_food":all_food})

def beds(request):
    if request.method == "POST":
        hospital_name = request.POST.get("hospital_name")
        hospital_contact = request.POST.get("hospital_contact")
        hospital_state = request.POST.get("hospital_state")
        hospital_city = request.POST.get("hospital_city").strip()
        hospital_address = request.POST.get("hospital_address")
        hospital_beds = request.POST.get("hospital_beds")
        hospital_verify = request.POST.get("hospital_verify")
        hospital_details = request.POST.get("hospital_details")

        beds = Beds(hospital_name=hospital_name, hospital_contact=hospital_contact, hospital_city=hospital_city, hospital_address=hospital_address, hospital_beds=hospital_beds, hospital_verify=hospital_verify, hospital_details=hospital_details,hospital_state=hospital_state)
        beds.save()
    all_beds = Beds.objects.all()

    return render(request,'donations/beds.html',{"all_beds":all_beds})


# ------------------------------------ Lead Display ----------------------------------------

def foodleads(request,pageno):
    all_food = list(chain(Food.objects.filter(volunteer_verify="Verified").order_by('-id'),Food.objects.filter(volunteer_verify="Unverified").order_by('-id')))
    context = pagination(all_food,"foods",pageno)
    if context == 0:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    return render(request,'leads/foodleads.html', context)

def bedleads(request,pageno):
    all_beds = list(chain(Beds.objects.filter(volunteer_verify="Verified").order_by('-id'),Beds.objects.filter(volunteer_verify="Unverified").order_by('-id')))
    context = pagination(all_beds,"beds",pageno)
    if context == 0:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    return render(request,'leads/bedleads.html', context)

def injectionleads(request,pageno):
    all_inj = list(chain(Injection.objects.filter(volunteer_verify="Verified").order_by('-id'),Injection.objects.filter(volunteer_verify="Unverified").order_by('-id')))
    context = pagination(all_inj,"injs",pageno)
    if context == 0:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    return render(request,'leads/injectionleads.html', context)

def oxygenleads(request,pageno):
    all_oxy = list(chain(Oxygen.objects.filter(volunteer_verify="Verified").order_by('-id'),Oxygen.objects.filter(volunteer_verify="Unverified").order_by('-id')))
    context = pagination(all_oxy,"oxys",pageno)
    if context == 0:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    return render(request,'leads/oxygenleads.html', context)

def plasmaleads(request,pageno):
    all_plasma = list(chain(Plasma.objects.filter(volunteer_verify="Verified").order_by('-id'),Plasma.objects.filter(volunteer_verify="Unverified").order_by('-id')))
    context = pagination(all_plasma,"plasmas",pageno)
    if context == 0:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    return render(request,'leads/plasmaleads.html', context)

def filter(request):
    return render(request,'leads/filter.html')


def filterleads(request,resource,state="",pageno=1,city=""):

    if city != "":
        city = city.strip()
    

    if resource == "Oxygen":
        if city == "":
            all_oxy = Oxygen.objects.filter(oxygen_lead_state=state)
        else:
            all_oxy = Oxygen.objects.filter(oxygen_lead_state=state,oxygen_lead_city=city)
        
        all_oxy =  list(chain(all_oxy.filter(volunteer_verify="Verified").order_by('-id'),all_oxy.filter(volunteer_verify="Unverified").order_by('-id')))

        context = pagination(all_oxy,"oxys",pageno)
        if context == 0:
            context = {}
        context["state"] = state
        context["city"] = city
        return render(request,'leads/oxygenleads.html', context)
            
    elif resource == "Plasma Donor":
        if city == "":
            all_plasma = Plasma.objects.filter(plasma_donor_state=state)
        else:
            all_plasma = Plasma.objects.filter(plasma_donor_state=state,plasma_donor_city=city)

        all_plasma =  list(chain(all_plasma.filter(volunteer_verify="Verified").order_by('-id'),all_plasma.filter(volunteer_verify="Unverified").order_by('-id')))
        
        context = pagination(all_plasma,"plasmas",pageno)
        if context == 0:
            context = {}
        context["state"] = state
        context["city"] = city
        return render(request,'leads/plasmaleads.html', context)

    elif resource == "Food Supplier":
        if city == "":
            all_food = Food.objects.filter(food_supplier_state=state)
        else:
            all_food = Food.objects.filter(food_supplier_state=state,food_supplier_city=city)

        all_food =  list(chain(all_food.filter(volunteer_verify="Verified").order_by('-id'),all_food.filter(volunteer_verify="Unverified").order_by('-id')))

        context = pagination(all_food,"foods",pageno)
        if context == 0:
            context = {}
        context["state"] = state
        context["city"] = city
        return render(request,'leads/foodleads.html', context)

    elif resource == "injections":
        if city == "":
            all_inj = Injection.objects.filter(injection_lead_state=state)
        else:
            all_inj = Injection.objects.filter(injection_lead_state=state,injection_lead_city=city)
        
        all_inj =  list(chain(all_inj.filter(volunteer_verify="Verified").order_by('-id'),all_inj.filter(volunteer_verify="Unverified").order_by('-id')))

        context = pagination(all_inj,"injs",pageno)
        if context == 0:
            context = {}
        context["state"] = state
        context["city"] = city
        return render(request,'leads/injectionleads.html', context)

    else:
        if city == "":
            all_beds = Beds.objects.filter(hospital_state=state)
        else:
            all_beds = Beds.objects.filter(hospital_state=state,hospital_city=city)
        
        all_beds = list(chain(all_beds.filter(volunteer_verify="Verified").order_by('-id'),all_beds.filter(volunteer_verify="Unverified").order_by('-id')))

        context = pagination(all_beds,"beds",pageno)
        if context == 0:
            context = {}
        context["state"] = state
        context["city"] = city
        return render(request,'leads/bedleads.html', context)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

# ------------------------------------ Home & Landing Page ----------------------------------------
def home(request):
    return render(request,'home.html')

def landing(request):
    return render(request,'volunteer/landing.html')

def volForm(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            volunteer_name = request.POST.get("volunteer_name")
            volunteer_email = request.POST.get("volunteer_email")
            volunteer_age = request.POST.get("volunteer_age")
            volunteer_phone = request.POST.get("volunteer_phone")
            volunteer_hours = request.POST.get("volunteer_hours")
            volunteer_aadhar = request.FILES["volunteer_aadhar"]

            try:
                validate_is_pdf(volunteer_aadhar)
            except ValidationError:
                messages.error(request,"Only pdf files are allowed!")
                return render(request,'volForm.html')
                
            volunteer_why = request.POST.get("volunteer_why")

            vols = Volunteer(user=request.user,volunteer_name=volunteer_name,volunteer_email=volunteer_email,volunteer_age=volunteer_age,volunteer_phone=volunteer_phone,volunteer_hours=volunteer_hours,volunteer_aadhar=volunteer_aadhar, volunteer_why=volunteer_why )
            vols.save()
        else:
            messages.error(request,"Please make sure you are logged In!")

    return render(request,'volForm.html')

# ------------------------------------ Volunteer Data ----------------------------------------

def volfood(request):
    if request.user.groups.filter(name="Volunteer").exists():
        all_food = Food.objects.filter(volunteer_deleted = "No")
        context = {'foods':all_food}
    else:
        return redirect("home")
    return render(request,'volunteer/food.html',context)

def volbeds(request):
    if request.user.groups.filter(name="Volunteer").exists():
        all_beds = Beds.objects.filter(volunteer_deleted = "No")
        context = {'beds':all_beds}
    else:
        return redirect("home")
    return render(request,'volunteer/beds.html',context)

def volinjection(request):
    if request.user.groups.filter(name="Volunteer").exists():
        all_injs = Injection.objects.filter(volunteer_deleted = "No")
        context = {'injs':all_injs}
    else:
        return redirect("home")
    return render(request,'volunteer/injections.html',context)

def voloxygen(request):
    if request.user.groups.filter(name="Volunteer").exists():
        all_oxys = Oxygen.objects.filter(volunteer_deleted = "No")
        context = {'oxys':all_oxys}
    else:
        return redirect("home")
    return render(request,'volunteer/oxygen.html',context)

def volplasma(request):
    if request.user.groups.filter(name="Volunteer").exists():
        all_plass = Plasma.objects.filter(volunteer_deleted = "No")
        context = {'plass':all_plass}
    else:
        return redirect("home")
    return render(request,'volunteer/plasma.html',context)

# ------------------------------------ Volunteer Edit & Verify ----------------------------------------

def deleteLead(request,resource,id):
    if request.user.groups.filter(name="Volunteer").exists():
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
        # deleted_item.delete()
        deleted_item.volunteer_deleted = "Yes"
        deleted_item.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    else:
        return redirect("home")

def verifyLead(request,resource,id):
    if request.user.groups.filter(name="Volunteer").exists():
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
    else:
        return redirect("home")

# ------------------------------------ Volunteer Food Edit ----------------------------------------

def editfood(request):
    if request.user.groups.filter(name="Volunteer").exists():
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
    else:
        return redirect("home")

# ------------------------------------ Volunteer Hospital Edit----------------------------------------

def edithospital(request):
    if request.user.groups.filter(name="Volunteer").exists():
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
    else:
        return redirect("home")


# ------------------------------------ Volunteer Plasma Edit----------------------------------------

def editplasma(request):
    if request.user.groups.filter(name="Volunteer").exists():
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
    else:
        return redirect("home")
  

# ------------------------------------ Volunteer Medicine Edit----------------------------------------

def editinjection(request):
    if request.user.groups.filter(name="Volunteer").exists():
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
    else:
        return redirect("home")


# ------------------------------------ Volunteer Oxygen Edit----------------------------------------

def editoxygen(request):
    if request.user.groups.filter(name="Volunteer").exists():
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
    else:
        return redirect("home")

# ------------------------------------ Authentication ----------------------------------------

def handleSignUp(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("pass1")
        if User.objects.filter(email=email).exists():
            messages.error(request,"Email already exists")
        else:
            try:
                user = User.objects.create_user(username=username,email=email,password=password)

                user.save()

                login(request,user,backend="django.contrib.auth.backends.ModelBackend")

                messages.success(request,"Successfully logged In")

            except Exception as e:

                messages.error(request,e)

    else:
        username = request.GET.get("username")
        print(username)
        if User.objects.filter(username=username).exists():
            return JsonResponse({"exists":"yes"})
        else:
            return JsonResponse({"exists":"no"})

    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

def handleLogin(request):

    if request.method == "POST":
        username = request.POST.get("login_username")
        password = request.POST.get("login_password")

        user = authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            messages.success(request,"Successfully logged In")

        else:
            messages.error(request,'Invalid credentials, Please try again')
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


def handleLogout(request):
    logout(request)
    messages.success(request,"Successfully Logged Out")
    return redirect("home")

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    "username": user.username
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        EMAIL_ADDRESS = 'srot.tech@gmail.com'
                        ############## ADD PASSWORD WHEN HOSTED ######################
                        EMAIL_PASSWORD = 'qxlhlpksflyowqzk'

                        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                            smtp.ehlo()
                            smtp.starttls()
                            smtp.ehlo()
                            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                            msg = EmailMessage()
                            msg['Subject'] = "SROT Password Reset"
                            msg['From'] = "Srot"
                            msg['To'] = data
                            msg.set_content(email)
                            smtp.send_message(msg)

                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("/password_reset/done/")
                    
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})
