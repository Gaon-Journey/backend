from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework import status
# import paypalrestsdk
from .paypal import paypalrestsdk 

# from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    GenericAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from .models import Trip, TripExtra, BookedTrips, User, MailingList
from .serializers import (
    TripSerializer,
    TripExtraSerializer,
    BillingAddressSerializer,
    BookedTripsSerializer,
    UserSerializer,
    MailingListSerializer
)


# Authentication views using simplejwt



# trip views
class AllTrips(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Trip.objects.all()
    serializer_class = TripSerializer


class TripDetails(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = TripSerializer

    def get(self, request, trip_id):
        trip = Trip.objects.get(id=trip_id)
        serializer = TripSerializer(trip)
        return Response(serializer.data)


class TripCategoryWise(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = TripSerializer

    def get_queryset(self):
        trip_type = self.kwargs["trip_type"]
        return Trip.objects.filter(trip_type=trip_type)


class TripSizeWise(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = TripSerializer

    def get_queryset(self):
        trip_type_2 = self.kwargs["trip_type_2"]
        return Trip.objects.filter(trip_type_2=trip_type_2)


# trip extra views
class AllTripExtras(ListAPIView):
    permission_classes = [AllowAny]
    queryset = TripExtra.objects.all()
    serializer_class = TripExtraSerializer


class TripSpecificExtras(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = TripExtraSerializer

    def get_queryset(self):
        trip_id = self.kwargs["trip_id"]
        return Trip.objects.get(id=trip_id).allowed_extras.all()


# profile views
class Profile(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UpdateProfile(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def put(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class DeleteUser(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def delete(self, request):
        user = User.objects.get(id=request.user.id)
        user.delete()
        return Response({"message": "User deleted successfully"})


class BookedTripsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookedTripsSerializer

    def get_queryset(self):
        return BookedTrips.objects.filter(user_id=self.request.user.id)


# billing address
class BillingAddressView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BillingAddressSerializer

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        billing_address = user.billing_address
        serializer = BillingAddressSerializer(billing_address)
        return Response(serializer.data)


class AddBillingAddressView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BillingAddressSerializer

    def put(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = BillingAddressSerializer(user.billing_address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class UpdateBillingAddressView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BillingAddressSerializer

    def put(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = BillingAddressSerializer(user.billing_address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


# auth views



# Paypal Views
#@csrf_exempt  # Use CSRF exempt for testing
class CreatePaymentView(APIView):
    """
    View to create a payment and get the PayPal approval URL.
    """

    def post(self, request):
        # Extract amount and currency from request data
        total_amount = request.data.get("amount")
        currency = request.data.get("currency", "USD")  # Default to USD if not specified

        # Check if the amount is provided
        if not total_amount:
            return Response({"error": "Amount is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a PayPal payment
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": "http://localhost:8000/payment/execute",  # Your frontend return URL
                "cancel_url": "http://localhost:8000/payment/cancel"    # Your frontend cancel URL
            },
            "transactions": [{
                "amount": {
                    "total": f"{total_amount:.2f}",  
                    "currency": currency
                },
                "description": "Purchase description"
            }]
        })

        # Create payment and get approval URL
        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    return Response({"approval_url": link.href}, status=status.HTTP_200_OK)
            return Response({"error": "Approval URL not found."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": payment.error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExecutePaymentView(APIView):
    #View to execute the payment after user approval.

    def get(self, request):
        payment_id = request.GET.get("paymentId")
        payer_id = request.GET.get("PayerID")

        # Find the payment and execute
        payment = paypalrestsdk.Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):
            # Payment was successful
            return Response({"status": "Payment completed successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": payment.error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# mailing list views
class AddToMailingList(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = MailingListSerializer

    def post(self, request):
        serializer = MailingListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    

class MailingListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = MailingList.objects.all()
    serializer_class = MailingListSerializer