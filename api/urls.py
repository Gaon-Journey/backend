from django.http import HttpResponse
from django.urls import path
from .views import (
    AllTrips,
    TripDetails,
    TripCategoryWise,
    TripSizeWise,
    AllTripExtras,
    TripSpecificExtras,
    Profile,
    UpdateProfile,
    DeleteUser,
    BookedTripsView,
    BillingAddressView,
    AddBillingAddressView, UpdateBillingAddressView,
)

from . import views

urlpatterns = [
    path("", lambda request: HttpResponse("Hello, World!")),
    # trip end points
    path("all_trips/", AllTrips.as_view(), name="all_trips"),
    path("trip/<int:trip_id>/", TripDetails.as_view(), name="trip_details"),
    path(
        "trips/<str:trip_type>/", TripCategoryWise.as_view(), name="trip_category_wise"
    ),
    path("trips/<str:trip_type_2>/", TripSizeWise.as_view(), name="trip_size_wise"),
    # trip extra end points
    path("all_trip_extras/", AllTripExtras.as_view(), name="all_trip_extras"),
    path(
        "trip_extras/<int:trip_id>/",
        TripSpecificExtras.as_view(),
        name="trip_specific_extras",
    ),
    # profile end points
    path("profile/<int:user_id>/", Profile.as_view(), name="profile"),
    path(
        "profile/update/<int:user_id>/", UpdateProfile.as_view(), name="update_profile"
    ),
    path("profile/delete/<int:user_id>/", DeleteUser.as_view(), name="delete_user"),
    # booked trips end points
    path("booked_trips/", BookedTripsView.as_view(), name="booked_trips"),
    # billing address
    path("billing_address/", BillingAddressView.as_view(), name="billing_address"),
    path("billing_address/add/", AddBillingAddressView.as_view(), name="add_billing_address"),
    path("billing_address/update/", UpdateBillingAddressView.as_view(), name="update_billing_address"),
    
    
    # Paypal urls
    path("payment/create/", views.CreatePaymentView.as_view(), name="create_payment"),
    path("payment/execute/", views.ExecutePaymentView.as_view(), name="execute_payment"),
]
