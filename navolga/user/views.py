from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import GroupMembership, Transaction, UserProfile  # Import the UserProfile model
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

def register_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")
        address = request.POST.get("address")

        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
        else:
            user = User.objects.create_user(
                username=name,
                email=email,
                password=password
            )
            # Create UserProfile with phone number
            UserProfile.objects.create(user=user, phone_number=phone_number, address = address)
            
            messages.success(request, "Registration successful. Please log in.")
            return redirect("login_view")
    return render(request, "register.html")



def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # Custom authentication with email
        user = authenticate(request, username=username, password=password)
        print(user)
        
        if user is not None:
            login(request, user)
            remember_me = request.POST.get("remember_me")  # None if unchecked
            if not remember_me:
                request.session.set_expiry(0)  # Session expires on browser close
            messages.success(request, "Logged in successfully.")
            return redirect("home")  # Redirect to home or desired page
        else:
            messages.error(request, "Invalid email or password.")
    
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login_view')


@login_required
@csrf_protect
def account_view(request):
    try:
        user_profile = request.user.profile  # Use related_name 'profile'
    except UserProfile.DoesNotExist:
        user_profile = None  # Handle missing profile

    group_membership = GroupMembership.objects.filter(user=request.user).first()
    transactions = Transaction.objects.filter(user_profile=user_profile).order_by('-timestamp') if user_profile else []

    context = {
        "user_profile": user_profile,
        "account_balance": group_membership.account_balance if group_membership else 0,
        "transactions": transactions
    }

    return render(request, "account_home.html", context)