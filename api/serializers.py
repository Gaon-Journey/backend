from rest_framework import serializers
from .models import Trip, TripExtra, BillingAddress, BookedTrips, User, MailingList


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = "__all__"


class TripExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripExtra
        fields = "__all__"


class BillingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingAddress
        fields = "__all__"


class BookedTripsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookedTrips
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class MailingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailingList
        fields = "__all__"