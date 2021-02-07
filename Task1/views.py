from django.shortcuts import render
from django.conf import settings
from django.views import View
from .models import *
from .mixins import *
from django.core.mail import send_mail
import threading
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect
from django.views.generic import ListView
import datetime
from django.contrib.auth.decorators import login_required
# Create your views here.


class CreateAccount(View,ApiMixins):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.body={}
        self.activities=list()
    def loadBody(self):
        list(map(lambda key:self.body.update({key:self.request.POST[key]} if key not in ["csrfmiddlewaretoken","g-recaptcha-response"] else []),self.request.POST.keys()))

    def post(self,request,*args,**kwrgs):
        try:
            self.loadBody()
            if not Account.objects.filter(email=self.body.get("email")).exists():
                accObj=Account.objects.create_user(**self.body)
                self.get_jsonObjects(accObj)
                threading.Thread(target=self.SendEmailTouser,args=(accObj,)).start()
                return render(request,"succses.html",{"data":self.activities})
            return render(request,"index.html",{"error":"Email already exists"})
        except Exception as exc:
            return render(request,"index.html",{"error":str(exc)})

    def get(self,request,*args,**kwrgs):
        if request.user.is_authenticated:
            return redirect('Home')
        return render(request,"index.html")

    def get_jsonObjects(self,user):
        count=0
        while count<10:
            activityJson=self.get_activities(user.type_of_user)
            if not UserActivities.objects.filter(type_of_activity=user.type_of_user,activity=activityJson.get("activity")).exists():
                self.activities.append(UserActivities.objects.create(activity=activityJson.get("activity"),
                type_of_activity=user.type_of_user,
                user=user,
                participants=activityJson.get("participants"),
                price=activityJson.get("price"),
                link=activityJson.get("link"),
                key=activityJson.get("key"),
                accessibility=activityJson.get("accessibility")
                ))
                count+=1

    def SendEmailTouser(self,accObj):
        send_mail('Welcome',"THis is welcome mail to you",settings.EMAIL_HOST_USER,[accObj.email])

class Login(CreateAccount):
    def get(self,request,*args,**kwrgs):
        if request.user.is_authenticated:
            return redirect('Home')
        return render(request,"login.html")
    def post(self,request,*args,**kwrgs):
        try:
            self.loadBody()
            user = authenticate(username=self.body.get("email"), password=self.body.get("password"))
            if user:
                login(request,user)
                return redirect("Home")
            return render(request,"login.html",{"error":"Username or email not found"})
        except Exception as exc:
            return render(request,"login.html",{"error":str(exc)})

class UserHome(View):

    def get(self,request,*args,**kwrgs):
        if request.user.is_authenticated:
            return render(request,"home.html",{"username":request.user.username})
        return redirect("Login")

class Logout(View):
    def get(self,request):
        logout(request)
        return redirect("Login")

class Loadactivities(ListView):
    model=UserActivities
    paginate_by = 2
    context_object_name = "activities"
    template_name="activities.html"

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return UserActivities.objects.filter(user=user)
        return []

class FetchmoreActivites(View,ApiMixins):
    def __init__(self):
        self.count=0
        self.activities=[]
    def get(self,request):
        user = self.request.user
        if user.is_authenticated:
            if UserActivities.objects.filter(user=user,created_on__icontains=datetime.datetime.now().strftime("%Y-%m-%d")).count()==0:
                while self.count<2:
                    activityJson=self.get_activities(user.type_of_user)
                    if not UserActivities.objects.filter(type_of_activity=user.type_of_user,activity=activityJson.get("activity")).exists():
                        self.activities.append(UserActivities.objects.create(activity=activityJson.get("activity"),
                        type_of_activity=user.type_of_user,
                        user=user,
                        participants=activityJson.get("participants"),
                        price=activityJson.get("price"),
                        link=activityJson.get("link"),
                        key=activityJson.get("key"),
                        accessibility=activityJson.get("accessibility")
                        ))
                        self.count+=1
                return render(request,"activities.html",{"activities":self.activities})
            return render(request,"activities.html",{"validation":"Today limit is complete Please try again tommorow"})
        return redirect("Login")


class UpdateActivites(View):
    def get_object(self,id):
        try:
            return UserActivities.objects.get(activitie_id=id)
        except UserActivities.DoesNotExist:
            return None

    def get(self,request,*args,**kwrgs):
        obj=self.get_object(self.request.GET.get("id"))
        if obj:
            return render(request,"updateActivity.html",{"data":obj})
        return render(request,"updateActivity.html",{"validation":"Object deleted or not found"})
      
    def post(self,request,*args,**kwrgs):
        if not request.user.is_authenticated:
            return redirect("Login")
        obj=self.get_object(self.request.POST.get("id"))
        if obj:
            obj.activity=self.request.POST.get("activity",obj.activity)
            obj.participants=self.request.POST.get("participants",obj.participants)
            obj.price=self.request.POST.get("price",obj.price)
            obj.link=self.request.POST.get("link",obj.link)
            obj.key=self.request.POST.get("key",obj.key)
            obj.accessibility=self.request.POST.get("accessibility",obj.accessibility)
            obj.save()
            return render(request,"updateActivity.html",{"data":obj,"status":"Object Updated"})
        return render(request,"updateActivity.html",{"validation":"Object deleted or not found"})

class DeleteActivity(UpdateActivites):

    def get(self,request,*args,**kwrgs):
        if not request.user.is_authenticated:
            return redirect("Login")
        user=self.request.user
        if user.is_superuser:
            obj=self.get_object(self.request.GET.get("id"))
            if obj:
                obj.delete()
                return redirect("Loadactivities")
            return render(request,"delete.html",{"status":"Object not found"})
        return render(request,"delete.html",{"status":"Forbidden You doesnt have permission to do this action"})
        



