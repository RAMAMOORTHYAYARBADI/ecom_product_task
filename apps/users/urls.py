from django.urls import path
from . import views

urlpatterns = [
    path('bulk_upload/',views.BulkUploadView.as_view()),
    path('feedback', views.FeedbackView.as_view({'post': 'post_feedback'})),
    path('product_feedback', views.FeedbackView.as_view({'post':'get_feedback_list'})),
    path('product_list/',views.ProductListView.as_view(),name='product_list'),
    ]

