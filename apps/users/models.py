from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin,BaseUserManager
)
from django.utils import timezone
from django.db import transaction
from django.contrib.auth.models import Group

# Create your models here.



class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise Exception('Model creation Error')

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, password=password, **extra_fields)


class User(AbstractBaseUser):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    """
    email = models.EmailField(max_length=126, unique=True,null = False)
    username = models.CharField(max_length = 256,null = True)
    password = models.CharField(max_length=256,null = True,blank = True)
    phone_number=models.CharField(max_length=128,null=True)
    address_line_1 = models.CharField(max_length=256,null = True)
    address_line_2 = models.CharField(max_length=256,null = True)
    profile_picture = models.CharField(null=True,max_length=126)
    role = models.ForeignKey(Group,on_delete=models.CASCADE,related_name='role',null = True,blank=True)
    is_block = models.BooleanField(default= False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now=True,null = True)   
    last_login = models.DateTimeField(blank=True,null=True)

    class Meta:
        db_table = 'ecom_user_master'

    objects = UserManager()

    USERNAME_FIELD = 'email'
    
    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self
    
class ProductMstr(models.Model):
    product_code = models.CharField(max_length=250, blank=True, null=True)
    product_name = models.CharField(max_length=512, blank=True, null=True)
    product_brand = models.CharField(max_length=512, blank=True, null=True)
    product_description = models.TextField(max_length=250, blank=True, null=True)
    product_price = models.DecimalField(default=0, max_digits = 10, decimal_places = 2)
    product_rating_score = models.DecimalField(default=0, max_digits = 10, decimal_places = 1)
    is_available = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True,null=True)
    updated_on = models.DateTimeField(auto_now=True,null=True)
    is_deleted=models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'ecom_product'
        get_latest_by = 'created_on'


class ProductFeedbackMstr(models.Model):
    product = models.ForeignKey(ProductMstr, related_name='+', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    title = models.CharField(max_length=128, blank=True, null=True)
    review = models.TextField(null=True,blank=True)
    rating = models.IntegerField(default=0)
    is_deleted= models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True,null=True)
    updated_on = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        managed = True
        db_table = 'ecom_product_feedback'

