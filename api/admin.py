from django.contrib import admin
import models


admin.site.register(models.User)
admin.site.register(models.Trip)
admin.site.register(models.TripExtra)
admin.site.register(models.BillingAddress)
admin.site.register(models.BookedTrips)