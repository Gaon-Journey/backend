import paypalrestsdk
from django.conf import settings

paypalrestsdk.configure({
 
    "mode": settings.PAYPAL_MODE,  
    "client_id": settings.PAYPAL_CLIENT_ID, #client id
    "client_secret": settings.PAYPAL_CLIENT_SECRET, #client secret
})
