import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser

files_to_delete = [
    "gamezone_env/rentals/templates/account/verification_sent.html",
    "gamezone_env/rentals/templates/account/email_verification_sent.html",
    "gamezone_env/rentals/templates/account/enter_token.html",
    "gamezone_env/rentals/templates/account/email/email_confirmation_message.txt",
]

for file_path in files_to_delete:
    try:
        os.remove(file_path)
        print(f"Deleted: {file_path}")
    except FileNotFoundError:
        print(f"File not found (already deleted?): {file_path}")
    except Exception as e:
        print(f"Error deleting {file_path}: {e}")
def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None and (user.is_staff or getattr(user, 'role', None) == 'admin'):
            login(request, user)
            request.session['is_admin'] = True
            return redirect('custom_admin_dashboard')
        else:
            messages.error(request, 'Invalid admin credentials or not authorized.')
    return render(request, 'admin/login.html')

def admin_logout(request):
    logout(request)
    request.session.flush()
    return redirect('custom_admin_login')

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.session.get('is_admin', False):
            return redirect('custom_admin_login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@admin_required
def custom_admin_dashboard(request):
    # You can use your existing dashboard logic here, or just render the dashboard template
    return render(request, 'admin/dashboard.html')

def equipment_list(request):
    return render(request, 'equipment/list.html')

def equipment_detail(request, equipment_id):
    return render(request, 'equipment/detail.html', {'equipment_id': equipment_id})

def home(request):
    return render(request, 'index.html')

def create_rental_request(request, equipment_id):
    return render(request, 'rentals/create_rental_request.html', {'equipment_id': equipment_id})

def load_more_equipment(request):
    return render(request, 'rentals/load_more_equipment.html')

def how_it_works(request):
    return render(request, 'how_it_works.html')

def about(request):
    return render(request, 'about.html')

def rental_requests_dashboard(request):
    return render(request, 'rentals/rental_requests_dashboard.html')

def my_rentals(request):
    return render(request, 'rentals/my_rentals.html')

def rental_detail(request, rental_id):
    return render(request, 'rentals/rental_detail.html', {'rental_id': rental_id})

def manage_rental(request, rental_id):
    return render(request, 'rentals/manage_rental.html', {'rental_id': rental_id})

def list_equipment(request):
    return render(request, 'equipment/list.html')

def my_equipment(request):
    return render(request, 'equipment/my_equipment.html')

def edit_equipment(request, equipment_id):
    return render(request, 'equipment/edit.html', {'equipment_id': equipment_id})

def delete_equipment(request, equipment_id):
    return render(request, 'equipment/delete.html', {'equipment_id': equipment_id})

def toggle_equipment_status(request, equipment_id):
    return render(request, 'equipment/toggle_status.html', {'equipment_id': equipment_id})

def paypal_payment_success(request, rental_id):
    """
    Handle PayPal payment success redirect.
    """
    # You may want to capture the payment here using order_id from request.GET
    # order_id = request.GET.get('token')  # PayPal usually returns 'token' as the order ID

    # Optionally, add logic to update payment/rental status here

    # For now, just render a simple success page or redirect
    return render(request, 'rentals/payment_success.html', {'rental_id': rental_id})

def paypal_payment_cancel(request, rental_id):
    """
    Handle PayPal payment cancel redirect.
    """
    return render(request, 'rentals/payment_cancel.html', {'rental_id': rental_id})

