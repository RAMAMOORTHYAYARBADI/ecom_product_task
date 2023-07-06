from rest_framework import serializers
from apps.users.models import *
from apps.account.models import *

class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()

    class Meta(object):
        model = User
        extra_kwargs = {'password': {'write_only': True}}
        
    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        self.Meta.exclude = ['updated_at','is_staff','is_superuser']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMstr
        fields = '__all__'

class ProductFeedbackSerializer(serializers.ModelSerializer):
    
    rating_status  = serializers.SerializerMethodField('get_rating_status')
    def to_representation(self, instance):
        primitive_repr = super(ProductFeedbackSerializer, self).to_representation(instance)
        primitive_repr['customer_name'] = User.objects.get(id=instance.customer_id).customer_name
        primitive_repr['customer_email'] = User.objects.get(id=instance.customer_id).email
        primitive_repr['product_name'] = instance.product.product_name
        primitive_repr['product_code'] = instance.product.product_code
        return primitive_repr

        
    def get_rating_status(self,data):
        item = data.rating
        if int(item) == 1:
            res = "Poor"
        elif int(item) == 2:
            res = "Not bad" 
        elif int(item) == 3:
            res = "Good" 
        elif int(item) == 4:
            res = "Very Good"
        elif int(item) == 5:
            res = "Excellent"
        else:
            res = "very Poor"
        return res
    
    class Meta:
        model = ProductFeedbackMstr
        fields='__all__'