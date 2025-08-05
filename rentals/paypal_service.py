import os
import json
import requests
from django.conf import settings
from django.urls import reverse
from decimal import Decimal
from .models import Payment, Rental

class PayPalService:
    """
    PayPal integration service for payment processing
    """
    
    def __init__(self):
        self.client_id = getattr(settings, 'PAYPAL_CLIENT_ID', '')
        self.client_secret = getattr(settings, 'PAYPAL_CLIENT_SECRET', '')
        self.mode = getattr(settings, 'PAYPAL_MODE', 'sandbox')  # sandbox or live
        
        if self.mode == 'sandbox':
            self.base_url = 'https://api-m.sandbox.paypal.com'
        else:
            self.base_url = 'https://api-m.paypal.com'
    
    def get_access_token(self):
        """Get PayPal access token"""
        url = f"{self.base_url}/v1/oauth2/token"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {self._get_basic_auth()}'
        }
        data = {'grant_type': 'client_credentials'}
        
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            raise Exception(f"Failed to get access token: {response.text}")
    
    def _get_basic_auth(self):
        """Get basic auth header for PayPal"""
        import base64
        auth_string = f"{self.client_id}:{self.client_secret}"
        return base64.b64encode(auth_string.encode()).decode()
    
    def create_order(self, rental, return_url, cancel_url):
        """Create a PayPal order"""
        access_token = self.get_access_token()
        
        url = f"{self.base_url}/v2/checkout/orders"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        
        # Calculate amounts
        total_amount = rental.total_amount
        subtotal = rental.subtotal
        service_fee = rental.service_fee
        delivery_fee = rental.delivery_fee
        
        payload = {
            "intent": "CAPTURE",
            "purchase_units": [{
                "reference_id": str(rental.id),
                "description": f"Rental: {rental.equipment.title}",
                "amount": {
                    "currency_code": "USD",
                    "value": str(total_amount),
                    "breakdown": {
                        "item_total": {
                            "currency_code": "USD",
                            "value": str(subtotal)
                        },
                        "shipping": {
                            "currency_code": "USD",
                            "value": str(delivery_fee)
                        },
                        "handling": {
                            "currency_code": "USD",
                            "value": str(service_fee)
                        }
                    }
                },
                "items": [{
                    "name": rental.equipment.title,
                    "description": f"Rental from {rental.start_date} to {rental.end_date}",
                    "quantity": "1",
                    "unit_amount": {
                        "currency_code": "USD",
                        "value": str(rental.daily_rate)
                    }
                }]
            }],
            "application_context": {
                "return_url": return_url,
                "cancel_url": cancel_url,
                "brand_name": "GameZone",
                "landing_page": "LOGIN",
                "user_action": "PAY_NOW"
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to create order: {response.text}")
    
    def capture_order(self, order_id):
        """Capture a PayPal order"""
        access_token = self.get_access_token()
        
        url = f"{self.base_url}/v2/checkout/orders/{order_id}/capture"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        
        response = requests.post(url, headers=headers)
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to capture order: {response.text}")
    
    def get_order_details(self, order_id):
        """Get PayPal order details"""
        access_token = self.get_access_token()
        
        url = f"{self.base_url}/v2/checkout/orders/{order_id}"
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get order details: {response.text}")
    
    def create_payment_record(self, rental, paypal_order_id, payment_type='rental_payment'):
        """Create a payment record in the database"""
        order_details = self.get_order_details(paypal_order_id)
        
        # Extract payment information
        purchase_unit = order_details['purchase_units'][0]
        amount = Decimal(purchase_unit['amount']['value'])
        
        payment = Payment.objects.create(
            rental=rental,
            payer=rental.renter,
            payment_type=payment_type,
            payment_method='paypal',
            amount=amount,
            status='pending',
            paypal_order_id=paypal_order_id,
            paypal_payer_id=order_details.get('payer', {}).get('payer_id'),
            paypal_email=order_details.get('payer', {}).get('email_address')
        )
        
        return payment
    
    def process_payment_capture(self, payment, capture_data):
        """Process payment capture and update payment record"""
        capture = capture_data['purchase_units'][0]['payments']['captures'][0]
        
        payment.status = 'completed'
        payment.paypal_capture_id = capture['id']
        payment.paypal_payment_id = capture['id']
        payment.processed_at = capture.get('create_time')
        payment.save()
        
        # Update rental status
        rental = payment.rental
        if payment.payment_type == 'rental_payment':
            rental.status = 'confirmed'
            rental.confirmed_at = payment.processed_at
            rental.save()
        
        return payment

def initiate_payment(rental, request):
    """Initiate a PayPal payment for a rental"""
    paypal_service = PayPalService()
    
    # Create return and cancel URLs
    return_url = request.build_absolute_uri(
        reverse('paypal_payment_success', kwargs={'rental_id': rental.id})
    )
    cancel_url = request.build_absolute_uri(
        reverse('paypal_payment_cancel', kwargs={'rental_id': rental.id})
    )
    
    try:
        # Create PayPal order
        order_data = paypal_service.create_order(rental, return_url, cancel_url)
        
        # Create payment record
        payment = paypal_service.create_payment_record(rental, order_data['id'])
        
        return {
            'success': True,
            'order_id': order_data['id'],
            'approval_url': order_data['links'][1]['href'],  # PayPal approval URL
            'payment_id': payment.id
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def capture_payment(order_id, payment_id):
    """Capture a PayPal payment"""
    paypal_service = PayPalService()
    
    try:
        # Capture the order
        capture_data = paypal_service.capture_order(order_id)
        
        # Get payment record
        payment = Payment.objects.get(id=payment_id)
        
        # Process the capture
        updated_payment = paypal_service.process_payment_capture(payment, capture_data)
        
        return {
            'success': True,
            'payment': updated_payment
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        } 