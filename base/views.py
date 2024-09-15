from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from buydenniscoffee.secrets import STRIPE_KEY

import stripe

stripe.api_key = STRIPE_KEY

def index(request):
	return render(request, 'base/index.html')


def charge(request):
	amount = 5
	if request.method == 'POST':
		print('Data:', request.POST)
	
	# reverse => dynamically generate a URL from a named URL pattern
	# (i.e. we don't hardcode the URL -- we ask django to make it from the urlpattern called success)
	return redirect(reverse('success', args=[amount]))


def successMsg(request, args):
	amount = args
	return render(request, 'base/success.html', {'amount':amount})

def calculate_order_amount(items):
    # Implement your order amount calculation logic here
    return 1400 

@api_view(["POST"])
def addPayment(request):
	try:
		data = request.data
        # Create a PaymentIntent with the order amount and currency
		intent = stripe.PaymentIntent.create(
            amount=calculate_order_amount(data['items']),
            currency='cad',
            automatic_payment_methods={
                'enabled': True,
            },
        )
		return Response({
            'clientSecret': intent['client_secret'],
            # [DEV]: For demo purposes only, you should avoid exposing the PaymentIntent ID in the client-side code.
            'dpmCheckerLink': 'https://dashboard.stripe.com/settings/payment_methods/review?transaction_id={}'.format(intent['id']),
        })
	except Exception as e:
		return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)