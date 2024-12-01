from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, AuthenticationForm
from .models import Policy
from django.contrib import messages 
from .models import Profile, UserPolicy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta
# from alphabet_sorter.sorting import ascending_sort


# def home(request):
#     default_policies = Policy.objects.filter(default=True)
#     other_policies = Policy.objects.filter(default=False)
#     return render(request, 'insurance/home.html', {
#         'default_policies': default_policies,
#         'other_policies': other_policies,
#     })
def home(request):
    # Query for policies
    default_policies = Policy.objects.filter(default=True)
    other_policies = Policy.objects.filter(default=False)

    # Add the S3 image URL to the context
    s3_image_url = "https://elasticbeanstalk-us-east-1-779777417450.s3.amazonaws.com/bike.jpeg"

    # Pass the S3 URL along with policies to the template
    return render(request, 'insurance/home.html', {
        'default_policies': default_policies,
        'other_policies': other_policies,
        's3_image_url': s3_image_url,  # Add the S3 URL here
    })

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile, created = Profile.objects.get_or_create(user=user)
            profile.phone_number = form.cleaned_data.get('phone_number')
            profile.save()

            # Authenticate and log in the user
            user = authenticate(username=user.username, password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                messages.success(request, "Signup successful! You are now logged in.")
                return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'insurance/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful. Welcome back!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid credentials. Please try again.')
        else:
            messages.error(request, 'Login failed. Please check your credentials.')
    else:
        form = AuthenticationForm()
    return render(request, 'insurance/login.html', {'form': form})


def logout_view(request):
    logout(request)  # Log the user out
    return redirect('home')

from django.shortcuts import render, get_object_or_404
from .models import Policy


@login_required
def policy_details(request, policy_name):
    policy = get_object_or_404(Policy, name = policy_name)
    return render(request, 'insurance/policies_details.html', {'policy': policy})

@login_required
def user_profile(request):
    # Check if the user has a profile; create one if not
    profile, created = Profile.objects.get_or_create(user=request.user)

    # Get the user's purchased policies
    purchased_policies = UserPolicy.objects.filter(user=request.user)

    return render(request, 'insurance/profile.html', {
        'profile': profile,
        'purchased_policies': purchased_policies
    })

# @login_required
# def user_profile(request):
#     # Check if the user has a profile; create one if not
#     profile, created = Profile.objects.get_or_create(user=request.user)

#     # Get the user's purchased policies
#     purchased_policies = UserPolicy.objects.filter(user=request.user)

#     # Sort the policies by policy name using the custom library
#     sorted_policies = ascending_sort(list(purchased_policies), key=lambda p: p.policy.name)

#     return render(request, 'insurance/profile.html', {
#         'profile': profile,
#         'purchased_policies': sorted_policies,
#     })
    
@login_required
def update_profile(request):
    user = request.user
    profile = user.profile  # Access the user's profile

    if request.method == 'POST':
        # Get data from the form
        username = request.POST.get('username', user.username)
        email = request.POST.get('email', user.email)
        phone_number = request.POST.get('phone_number', profile.phone_number)
        address = request.POST.get('address', profile.address)

        # Validate username and email to ensure they are unique
        if User.objects.filter(username=username).exclude(id=user.id).exists():
            messages.error(request, "Username is already taken.")
        elif User.objects.filter(email=email).exclude(id=user.id).exists():
            messages.error(request, "Email is already in use.")
        else:
            # Update user fields
            user.username = username
            user.email = email
            user.save()  # Save user data

            # Update profile fields
            profile.phone_number = phone_number
            profile.address = address
            profile.save()  # Save profile data

            messages.success(request, "Your profile has been updated.")
            return redirect('profile')  # Redirect to the profile page after updating

    # Pre-fill the form with current values for the user and profile
    return render(request, 'insurance/update_profile.html', {
        'user': user,
        'profile': profile,
    })
from django.http import HttpResponseForbidden
@login_required
def update_policy(request, policy_name):
    if not request.user.is_staff:  # Only admins can update policies
        return HttpResponseForbidden("Unauthorized access.")
    
    policy = get_object_or_404(Policy, name=policy_name)
    if request.method == 'POST':
        policy.description = request.POST.get('description', policy.description)
        policy.price = request.POST.get('price', policy.price)
        policy.save()
        messages.success(request, f"Policy '{policy.name}' has been updated.")
        return redirect('home')

    return render(request, 'insurance/update_policy.html', {'policy': policy})


@login_required
def delete_policy(request, policy_name):
    # Filter UserPolicy objects for the logged-in user and the given policy name
    user_policies = UserPolicy.objects.filter(user=request.user, policy__name=policy_name)

    if not user_policies.exists():
        messages.error(request, "You do not have this policy.")
        return redirect('profile')

    if request.method == 'POST':  # Ensure deletion happens via POST to prevent accidental deletes
        user_policies.delete()
        messages.success(request, f"Your policy '{policy_name}' has been deleted.")
        return redirect('profile')

    return render(request, 'insurance/delete_policy.html', {
        'policy_name': policy_name,
        'user_policies': user_policies,
    })
    

@login_required
def buy_policy(request, policy_name):
    policy = get_object_or_404(Policy, name=policy_name)

    # Check if the user already owns this policy (with any plan)
    existing_policy = UserPolicy.objects.filter(user=request.user, policy=policy).first()
    if existing_policy:
        messages.warning(request, f"You have already purchased the policy: {policy.name}.")
        return redirect('profile')

    # Create the new policy purchase
    UserPolicy.objects.create(
        user=request.user,
        policy=policy,
        plan='Basic',  # Default plan
        start_date=now().date(),
        end_date=(now() + timedelta(days=365)).date()
    )
    messages.success(request, f"You have purchased the policy: {policy.name}.")
    return redirect('profile')


@login_required
def add_policy(request):    
    if not request.user.is_staff:  # Restrict to admin users
        return HttpResponseForbidden("Unauthorized access.")

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        # default = request.POST.get("default") == "on"  # Check if the policy is marked as default
        # image = request.FILES.get("image")

        # Save new policy
        Policy.objects.create(
            name=name,
            description=description,
            price=price,
            # default=default,
            # image=image
        )
        messages.success(request, "Policy added successfully!")
        return redirect('home')

    return render(request, 'insurance/add_policy.html')

@login_required
def upgrade_policy(request, policy_name):
    # Fetch the relevant policy
    policy = get_object_or_404(Policy, name=policy_name)
    
    # Fetch the user's policies for this specific policy
    user_policies = UserPolicy.objects.filter(user=request.user, policy=policy)

    # Ensure only one UserPolicy is found for the user
    if user_policies.count() > 1:
        messages.error(request, "You have multiple policies for this plan. Please choose one.")
        return redirect('profile')

    # If exactly one policy is found, proceed
    user_policy = user_policies.first()

    if request.method == 'POST':
        # Get the selected plan from the form
        new_plan = request.POST.get('plan')
        
        if new_plan not in ['Basic', 'Standard', 'Premium']:
            messages.error(request, "Invalid plan selected.")
            return redirect('profile')

        # Update the user's plan and save it
        user_policy.plan = new_plan
        user_policy.save()

        messages.success(request, f"Your policy has been updated to the '{new_plan}' plan.")
        return redirect('profile')

    return render(request, 'insurance/upgrade_policy.html', {
        'user_policy': user_policy,
        'available_plans': ['Basic', 'Standard', 'Premium'],  # List of plans
    })


@login_required
def view_all_users(request):
    # Check if the user is an admin
    if not request.user.is_staff:
        return redirect('home')  # Redirect if the user is not an admin

    # Get all users and their associated policies
    users_with_policies = User.objects.all()  # Get all users
    user_policies = {}
    
    for user in users_with_policies:
        user_policies[user] = UserPolicy.objects.filter(user=user)  # Get policies for each user

    return render(request, 'insurance/view_all_users.html', {
        'user_policies': user_policies
    })
    
@login_required
def delete_user(request, username):
    # Ensure only admin can delete users
    if not request.user.is_staff:
        return redirect('home')  # Redirect if the user is not an admin

    # Get the user object to delete by their username
    user = get_object_or_404(User, username=username)
    
    # Delete all policies associated with this user
    UserPolicy.objects.filter(user=user).delete()

    # Delete the user
    user.delete()

    # Optionally, show a success message
    messages.success(request, f"The user '{user.username}' has been deleted.")

    return redirect('view_all_users')  # Redirect back to the list of users

@login_required
def delete_policy_admin(request, policy_name):
    if not request.user.is_staff:  # Restrict to admin users only
        return HttpResponseForbidden("Unauthorized access.")
    
    # Get the policy object created by the admin
    policy = get_object_or_404(Policy, name=policy_name)
    
    if request.method == 'POST':  # Ensure deletion happens via POST to prevent accidental deletes
        policy.delete()
        messages.success(request, f"Policy '{policy_name}' has been deleted.")
        return redirect('home')  # Redirect to a suitable page after deletion
    
    return render(request, 'insurance/delete_policy_admin.html', {
        'policy_name': policy_name,
    })
    