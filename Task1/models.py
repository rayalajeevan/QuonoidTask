from django.db import models
from django.conf import settings
from django.contrib.auth.models import UserManager,AbstractBaseUser,PermissionsMixin

# Create your models here.
class User(models.Model):
    def create_user(self,first_name,last_name,username,email,type_of_user,password,created_on,edited_on,**kwrgs):
        user_account=self.model(first_name=first_name,last_name=last_name,username=username,email=email,type_of_user=type_of_user,
        created_on=created_on,edited_on=edited_on)
        user_account.set_password(password)
        user_account.save(using=self._db)
        return user_account
    def create_superuser(self,first_name,last_name,username,email,type_of_user,password,created_on,edited_on,**kwrgs):
        user_account=self.create_user(first_name,last_name,username,email,type_of_user,password,created_on,edited_on)
        user_account.is_admin =True
        user_account.is_superuser = True
        user_account.is_staff = True
        user_account.save(using=self._db)
        return user_account
class Account(AbstractBaseUser,PermissionsMixin):
    user_id=models.AutoField(primary_key=True)
    first_name=models.CharField(max_length=250)
    last_name=models.CharField(max_length=250)
    username=models.CharField(max_length=250)
    email=models.EmailField(max_length=250,unique=True)
    is_staff = models.BooleanField(default=False)
    type_of_user=models.CharField(max_length=50,choices=settings.ACCOUNT_TYPES)
    created_on=models.DateTimeField(auto_now=True)
    edited_on=models.DateTimeField(null=True,blank=True)
    objects = UserManager()
    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['username',]
    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return f"{self.first_name}, {self.last_name}"
    

class UserActivities(models.Model):
    activitie_id=models.AutoField(primary_key=True)
    activity=models.CharField(max_length=250)
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    type_of_activity=models.CharField(max_length=50)
    participants=models.IntegerField()
    price=models.FloatField()
    link=models.CharField(max_length=250)
    key=models.CharField(max_length=250)#it is numerous digit but taking as a charfield due to becuase of doc
    accessibility=models.FloatField()
    created_on=models.DateTimeField(auto_now=True)
    edited_on=models.DateTimeField(null=True,blank=True)
    
