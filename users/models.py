
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.contrib.auth.hashers import make_password

#------------------------- MODEL FOR SALUTION --------------------------

    
def validate_file_size(value):
    max_size = 5 * 1024 * 1024  # 5 MB
    if value.size > max_size:
        raise ValidationError({"status_code":604, "error":"profile photo must be less than 5MB"})
    
def profile_photo(instance, filename):
    filename = f"profile_photo_{instance.id}{filename[-4:]}"
    return f"profile_photos/{filename}"

#------------------------------- BASE USER MANAGER FOR CREATE CUSTOM USER AND SUPER USER -----------------------
class MyUserManager(BaseUserManager):
    def create_user(self, firstname, lastname, username, email, password=None, is_admin=False, is_customer=False, is_active=True, is_staff=False):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            firstname = firstname,
            lastname = lastname,
            username = username,
            password = password,
            is_admin = is_admin,
            is_customer = is_customer,
            is_active = is_active,
            is_staff = is_staff,
        )

        user.save(using=self._db)
        return user
    
    def create_superuser(self, firstname, lastname, username, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            firstname = firstname,
            lastname = lastname,
            username = username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True
        user.set_password(password)
        user.save(using = self._db)
        return user

#---------------------------- ABSTRACT BASE USER USER MODEL ----------------------------------------------
class User(AbstractBaseUser):
    firstname       = models.CharField(max_length=50)
    lastname        = models.CharField(max_length=50)
    email           = models.EmailField(max_length=50, unique=True)
    password        = models.CharField(max_length=128, null=True)
    profile_photo = models.FileField(upload_to='profile_photo', blank=True, null=True, validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),  # Add allowed image file extensions
            validate_file_size,
        ],
    )
    confirmed    = models.BooleanField(default=False)
    
    #additional fields
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    last_login  = models.DateTimeField(null=True, blank=True)
    is_admin    = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    #Registering usermanager
    objects = MyUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname']
    

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()
        
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
    def get_full_name(self):
        return f'{self.firstname} {self.lastname}'
    
    def update_last_login(self):
        self.last_login = timezone.now()
        self.save()
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    # def has_enabled_2fa(self):
    #     return self.otp_device.confirmed() if self.otp_device else False
    
class UserAddresses(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    alternate_phone = models.CharField(max_length=10, null=True, blank=True)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, null=True, blank=True)
    land_mark = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    pincode = models.CharField(max_length=6)
    is_shipping_address = models.BooleanField(default=False)
    is_billing_address = models.BooleanField(default=False)
    
    
    

class RecoveryCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    codes = models.JSONField(default=list)
    
    def __str__(self):
        return str(self.user)  
    



class UserForgotPassword(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    code    = models.CharField(max_length=200, null=True, blank=True)
    expired_at = models.DateTimeField()
    is_expired = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.user_id)
    

    
class UserLoginLogs(models.Model):
    user_id             = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    browser             = models.CharField(max_length=300, null=True, blank=True)
    operating_system    = models.CharField(max_length=300, null=True, blank=True)
    device             = models.CharField(max_length=300, null=True, blank=True)
    ip_address          = models.CharField(max_length=300, null=True, blank=True)
    last_login          = models.DateTimeField(max_length=300, null=True, blank=True)
    
    def __str__(self):
        return str(self.user_id)
    
    class Meta:
        verbose_name_plural = "User login logs"
