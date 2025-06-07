# views.py
import paynships.views.razorpay_views as razorpay_views
from django.conf import settings
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from orders.models import Order, OrderItem
from carts.models import Cart, CartItem
from paynships.models import Payment
from users.models import UserAddresses


class RazorpayOrderCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        amount = request.data.get("amount") 
        amount_in_paise = int(float(amount) * 100)

        client = razorpay_views.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        order_data = {
            "amount": amount_in_paise,
            "currency": "INR",
            "payment_capture": 1,
            "method": "upi",
        }
        razorpay_order = client.order.create(order_data)

        return Response({
            "order_id": razorpay_order['id'],
            "amount": razorpay_order['amount'],
            "currency": razorpay_order['currency'],
            "key": settings.RAZORPAY_KEY_ID
        }, status=status.HTTP_201_CREATED)
        

class RazorpayPaymentVerifyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        total_amount = request.data.get('total_amount')
        data = request.data

        try:
            client = razorpay_views.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            client.utility.verify_payment_signature({
                'razorpay_order_id': data['razorpay_order_id'],
                'razorpay_payment_id': data['razorpay_payment_id'],
                'razorpay_signature': data['razorpay_signature']
            })
        except razorpay_views.errors.SignatureVerificationError:
            return Response({"error": "Invalid signature"}, status=400)

        # Now create Order, OrderItems, Payment
        user = request.user
        cart = Cart.objects.filter(user_id=user).first()
        cart_items = CartItem.objects.filter(cart_id=cart)
        user_shipping_address = UserAddresses.objects.filter(user_id=user, is_shipping_address=True)
        user_billing_address = UserAddresses.objects.filter(user_id=user, is_billing_address=True)

        order = Order.objects.create(
            user_id=user,
            total_amount=total_amount,
            shipping_address=user_shipping_address,
            billing_address=user_billing_address,
            payment_status='paid',
            status='processing'
        )

        for item in cart_items:
            OrderItem.objects.create(
                order_id=order,
                product_id=item.product_id,
                quantity=item.quantity,
                price_at_purchase=item.product_id.sale_price
            )

        Payment.objects.create(
            order_id=order,
            payment_method="UPI",
            payment_id=data['razorpay_payment_id'],
            amount_paid=order.total_amount,
            status='success'
        )

        cart_items.delete()

        return Response({"message": "Payment verified and order placed."})
