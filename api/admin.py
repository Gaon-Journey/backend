from django.contrib import admin
from .models import *


admin.site.register(User)
admin.site.register(Trip)
admin.site.register(TripExtra)
admin.site.register(BillingAddress)
admin.site.register(BookedTrips)