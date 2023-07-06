from django.utils import timezone
from math import ceil
from rest_framework.views import APIView
from rest_framework import generics,permissions,status,viewsets
from rest_framework.response import Response
from utils.pagination import *
from apps.users.models import *
from apps.users.serializer import *
from utils.enum import *
from utils import json,validators
from utils import permissions as cust_permissions
from datetime import datetime
from django.contrib.auth.hashers import make_password,check_password
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.parsers import JSONParser,MultiPartParser,FormParser
import os
import pandas as pd 
import numpy as np

class Signup(APIView):
    permission_classes=[permissions.AllowAny]
 
    def post(self,request):
        try:
            data = request.data
            val = validators.Signup_Validators(data)
            if val == False:
                return Response({'status':False,'data':'Required Feild is Missing'},status=status.HTTP_400_BAD_REQUEST)
            data['role'] = RoleEnum.user.value
            if User.objects.filter(email=data['email'],is_active=True).exists():
                return json.Response("User already register", 400, False)
            if data['password'] != data['confirm_password']:
                return json.Response("password are mismatched", 400, False)
            data['password'] = make_password(data['password']) 
            userdata = UserSerializer(data=data)
            if userdata.is_valid(raise_exception=True):    
                userdata.save()
            return json.Response("signup successfully", 201, True)
        except:
            return json.Response("Internal Server Error", 400, False)
        
def auth_token(user):
   access = AccessToken.for_user(user)
   refresh=RefreshToken.for_user(user)

   access['email']=user.email
   access['id']=user.id
   refresh['email']=user.email
   refresh['id']=user.id
   
   return {"access_token": str(access),
   "refresh_token":str(refresh)}
        
class Login(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self,request):
        try:
            email = request.data['email']
            password = request.data['password']
            if email == None:
                res = {'status':False,'message':'Kindly Enter The Email','data':[]}
                return Response(res,status=status.HTTP_400_BAD_REQUEST)
            if password == None:
                res = {'status':False,'message':'Kindly Enter The Password','data':[]}
                return Response(res,status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(email=email)
            ch_password = check_password(password,user.password)
            if user and ch_password:
                user_details = {}
                get_jwt = auth_token(user)
                user_details['access_token'] = get_jwt['access_token']
                user_details['refresh_token'] = get_jwt['refresh_token']
                user_details['email'] = email
                user_details['message'] = 'Logged In Successfully'
                res = {'status':True,'data':user_details}
                return Response(res,status=status.HTTP_200_OK)
            else:
                res = {'status':False,'data':'Incorrect Login Details'}
                return Response(res,status = status.HTTP_400_BAD_REQUEST)           
        except Exception as e:
            res = {'status':False,'message':'Internal Server Error','data':[]}
            return Response(res,status=status.HTTP_400_BAD_REQUEST)

class BulkUploadView(APIView):
    permission_classes=[permissions.IsAuthenticated,cust_permissions.Is_SuperAdmin]
    parser_classes = (MultiPartParser,FormParser,JSONParser)

    def post(self, request):
        if 'csv' not in request.FILES:
            return json.Response('Please select the file',400, False)
        document = request.FILES['csv']
        file_extension = os.path.splitext(document.name)[1]
        
        if not ((file_extension == ".csv") or (file_extension == ".xlsx")):
            return json.Response('Invalid file format',400, False)
        if file_extension == ".xlsx":
            df = pd.read_excel(document)
        if file_extension == ".csv":
            df = pd.read_csv(document)

        df.dropna(how="all", inplace=True)
        total_rows = len(df.axes[0])
        if total_rows > 200:
            return json.Response('You connot upload more than 200 products',400, False)
        
        df = pd.DataFrame(df).replace(np.nan, '',regex=True)
        column = list(df.columns)
        column_name = ["PRODUCT CODE","PRODUCT DESCRIPTION","PRODUCT NAME","PRODUCT PRICE","PRODUCT BRAND","PRODUCT AVAILABLE"]
        missing_columns = list(set(column_name).difference(column))
        if len(missing_columns) !=0:
            return Response({'status':False,'data':f"Column name {','.join(missing_columns)} is missing"},status=status.HTTP_400_BAD_REQUEST)
        for x in range(len(column)):            
            if column[x] == f"Unnamed: {x}":
                return Response({'status':False,'data':f"Column name {column_name[x]} is missing"},status=status.HTTP_400_BAD_REQUEST)

            if (list(df.columns)[x]) != column_name[x]:
                return Response({'status':False,'data':f"Invalid column name {column[x]}"},status=status.HTTP_400_BAD_REQUEST)

        row_iter = df.iterrows()
        
        arr = []
        for index, row in row_iter:
            error_key=[]
            error_msg=[]
            if row['PRODUCT PRICE']=="":
                text_key = "PRODUCT PRICE"
                error_key.append(text_key)
                text_msg = "Product Price Missing"
                error_msg.append(text_msg)

            try:
                spiritual = float(row['PRODUCT PRICE'])
            except:
                text_key = "PRODUCT PRICE-Numeric"
                error_key.append(text_key)
                text_msg = "Product Price must be Numeric"
                error_msg.append(text_msg)
                spiritual = 0.0

            if row['PRODUCT CODE']=="":
                text_key = "PRODUCT CODE"
                error_key.append(text_key)
                text_msg = "Product Code is missing"
                error_msg.append(text_msg)

            if ProductMstr.objects.filter(product_code=row['PRODUCT CODE'],is_deleted=False).exists():
                text_key = "PRODUCT CODE DUPLICATE"
                error_key.append(text_key)
                text_msg = "Product CODE already exist"
                error_msg.append(text_msg)

            if row['PRODUCT DESCRIPTION']=="":
                text_key = "PRODUCT DESCRIPTION"
                error_key.append(text_key)
                text_msg = "Product description is missing"
                error_msg.append(text_msg)

            if row['PRODUCT NAME']=="":
                text_key = "PRODUCT NAME"
                error_key.append(text_key)
                text_msg = "Product Name is missing"
                error_msg.append(text_msg)

            if row['PRODUCT BRAND']=="":
                text_key = "PRODUCT BRAND"
                error_key.append(text_key)
                text_msg = "Product brand is missing"
                error_msg.append(text_msg)

            if row['PRODUCT AVAILABLE']=="":
                text_key = "AVAILABLE"
                error_key.append(text_key)
                text_msg = "Product available is missing"
                error_msg.append(text_msg)
            
            error_key = ",".join(error_key)
            row['ERROR STATUS'] = error_key

            error_msg = ",".join(error_msg)
            row['ERROR MESSAGE'] = error_msg
            if len(error_key) != 0 or len(error_msg) !=0:
                arr.append(dict(row))
                  
            product=ProductMstr(
                product_code = row['PRODUCT CODE'],
                product_name = row['PRODUCT NAME'],
                product_description = row['PRODUCT DESCRIPTION'],
                product_brand = row['PRODUCT BRAND'],
                is_available = row['PRODUCT AVAILABLE'],
                product_price = row['PRODUCT PRICE']
                
            )
            product.save()
                
                
        
        new = pd.DataFrame.from_dict(arr)
        test=new.to_csv('mediafiles/sample/error_products.csv', encoding='utf-8', index=False)#BASE_DIR+"/media/sample/error_products.csv","http://127.0.0.1:8000/media/sample/error_products.csv"
        error = 'http://127.0.0.1:8000/media/sample/error_products.csv'
        if total_rows == (total_rows - len(arr)):
            key = "success"
        elif total_rows == len(arr):
            key = "failed"
        else:
            key = "partial"
        return Response({'status':True,
                        "data":"Products- Bulk Upload",
                        "total_row":total_rows,
                        "uploaded":total_rows - len(arr),
                        "download_error_url":error,
                        "unupload":len(arr),
                        "key":key,
                        "arr":arr},
                        status=status.HTTP_200_OK)
    

#------------------------CUSTOMER FEEDBACK -------------
class FeedbackView(viewsets.ViewSet):
    permission_classes=[permissions.IsAuthenticated,cust_permissions.Is_User]

    """
    Once the customer received the ordered products that time they gave a feedback about his products
    """
    def post_feedback(self, request):
        data = request.data
        try:

            val = validators.ProductFeedback_Validators(data)
            if val == False:
                return Response({'status':False,'data':'Required Feild is Missing'},status=status.HTTP_400_BAD_REQUEST)

            product_id = request.data['product_id']
            try:
                product = ProductMstr.objects.get(id=product_id,is_deleted=False)
            except:
                return Response({'status':False,'data':'Invalid products'},status=status.HTTP_400_BAD_REQUEST)
            title = request.data['title']
            review = request.data['review']
            rating = request.data['rating']
            #guest user check
            if 'HTTP_AUTHORIZATION' not in request.META:
                return Response({'status':True,'data':'Please login'},status=status.HTTP_200_OK)
            else:
                try:
                    cust = User.objects.get(is_active= True,id=request.user.id)
                except:
                    return Response({'status':False,'data':'User is deactivated'},status=status.HTTP_400_BAD_REQUEST)
              
            data = ProductFeedbackMstr.objects.filter(customer_id=cust, product_id=product)

            if data.exists():
                report_obj = data.first()
                report_obj.title = title
                report_obj.product_id = product
                report_obj.review = review
                report_obj.rating = rating
                report_obj.user_id = cust
                report_obj.updated_on = datetime.now()
                report_obj.save()
                return Response({'status':True,'data':'Feedback Updated Successfully'},status=status.HTTP_200_OK)

            ProductFeedbackMstr.objects.create(**{
                'title':title,
                'customer': cust,
                'product': product,
                'review': review,
                'rating':rating,
                'updated_on':datetime.now()
            })

            sum_of_rating  = sum(ProductFeedbackMstr.objects.filter(product_id=product).values_list('rating'))
            length =  len(ProductFeedbackMstr.objects.filter(product_id=product))
            average = round((sum_of_rating / length),1)
            ProductMstr.objects.filter(id=product_id).update(product_rating_score=average)
                    
            return Response({'status':True,'data':'Feedback Added Successfully'},status=status.HTTP_200_OK)
        except Exception as e:
            return json.Response("Internal Server Error", 400, False)

    """
    Customer view the feedback based on product
    """
    def get_feedback_list(self, request):
        
        try:
            data = request.data
            product_id = data['product_id']
            page = data['page']
            if not ProductFeedbackMstr.objects.filter(product_id=product_id,is_deleted = False,status='approved').exists():
                return Response({'status':True,'data':'Nothing to Show'},status=status.HTTP_200_OK)
            feedback = ProductFeedbackMstr.objects.filter(product_id=product_id,is_deleted = False,status='approved')
            #pagination calculation
            total_count=len(feedback)
            count_1 = total_count % 12
            count_2 = total_count // 12
            
            if  count_1 != 0:
                count_2 +=1
            #pagination
            offset = 0
            limit = 12
            page_ = product_pagination(offset,limit,page)
            result = feedback[page_[0]:page_[1]]
            if request.method == 'POST':
                serializer = ProductFeedbackSerializer(result,many=True)
                return Response({'status':True,'available_data':total_count,'total_no_of_pages':count_2,'current_page':page,'limit_per_page':limit,'data':serializer.data},status=status.HTTP_200_OK)
        except Exception:
            return json.Response("Internal Server Error", 400, False)
        
class ProductListView(generics.ListAPIView):
    permission_classes=[permissions.IsAuthenticated,cust_permissions.Is_User]
    
    queryset = ProductMstr.objects.all().order_by('-product_rating_score')  
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    def get(self, request):
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            datas = result['data'] # pagination data
            data = json.Response(result,200,True)
        else:
            serializer = self.get_serializer(self.queryset, many=True)
            data = json.Response(serializer.data,200,True)

        return data