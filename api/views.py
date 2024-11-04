from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

# from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    GenericAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from .models import Trip, TripExtra, BookedTrips, User
from .serializers import (
    TripSerializer,
    TripExtraSerializer,
    BillingAddressSerializer,
    BookedTripsSerializer,
    UserSerializer,
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
