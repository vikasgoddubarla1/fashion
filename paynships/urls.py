
from django.urls import path
from paynships.views import razorpay_views

urlpatterns = [
    path('create-razorpay-order/', razorpay_views.RazorpayOrderCreateAPIView.as_view(), name='create_razorpay_order'),
    path('verify-razorpay-payment/', razorpay_views.RazorpayPaymentVerifyAPIView.as_view(), name='verify_razorpay_payment'),

]
