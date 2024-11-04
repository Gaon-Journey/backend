from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser, Group, Permission


# trip extras model
class TripExtra(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    price = models.FloatField()


# trip model
class Trip(models.Model):
    trip_name = models.CharField(max_length=100)
    trip_type = models.CharField(
        max_length=10, choices=(("rural", "Rural"), ("agro", "Agro"))
    )
    trip_type_2 = models.CharField(
        choices=(("group", "Group"), ("solo", "Solo")), max_length=10
    )
    description = models.TextField()
    price = models.FloatField()
    min_people = models.IntegerField()
    max_people = models.IntegerField()
    discount_codes = ArrayField(models.CharField(max_length=50), blank=True, null=True)
    itenary = models.JSONField()
    includes = ArrayField(models.CharField(max_length=100))
    excludes = ArrayField(models.CharField(max_length=100))
    allowed_extras = models.ManyToManyField(TripExtra)


# address model
class BillingAddress(models.Model):
    line_1 = models.CharField(max_length=50)
    line_2 = models.CharField(max_length=50)
    line_3 = models.CharField(max_length=50, blank=True, null=True)
    pin_code = models.IntegerField(
        validators=[MaxValueValidator(000000), MinValueValidator(999999)]
    )
    country = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=20,  # Adjust based on your needs
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",  # Example regex for international phone numbers
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
            )
        ],
    )


# user model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone_number = models.CharField(
        max_length=20,  # Adjust based on your needs
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",  # Example regex for international phone numbers
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
            )
        ],
    )
    auth_provider = models.CharField(
        choices=(("google", "Google"), ("email", "Email")), max_length=10
    )
    billing_address = models.ForeignKey(
        BillingAddress, on_delete=models.CASCADE, blank=True, null=True
    )

    # Add related_name to resolve clashes
    groups = models.ManyToManyField(Group, related_name="custom_user_set", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="custom_user_permissions_set", blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["email", "name"]


# booked trips
class BookedTrips(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    extras_included = ArrayField(models.IntegerField())
    final_cost = models.FloatField()  # after discount price
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)
