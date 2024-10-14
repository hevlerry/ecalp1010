from custom_admin.views import is_staff
from .models import Product, User, UserReport, ProductImage
from .forms import PostProductForm
from django.contrib import messages
from .forms import ProfileForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Profile, Product, Report
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Rating
from .forms import ProfileForm, RatingForm
from django.db.models import Avg, Count
from django.utils import timezone


def logout_view(request):
    logout(request)
    return redirect('index', logout=True)


from django.utils import timezone
from django.contrib.auth.decorators import login_required


@login_required
def newsfeed(request):
    # Filter out products that are inactive or have been deleted
    products = Product.objects.filter(is_active=True, deleted_at__isnull=True).order_by('-created_at')

    # Convert created_at to local time for each product
    for product in products:
        product.created_at = timezone.localtime(product.created_at)

    return render(request, 'newsfeed.html', {'products': products})

def listing_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'listing_detail.html', {'product': product})

def post_product(request):
    if request.method == 'POST':
        form = PostProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.category = form.cleaned_data['category']
            product.save()
            # Save multiple images
            for file in request.FILES.getlist('image'):
                ProductImage.objects.create(product=product, image=file)
            messages.success(request, 'Your product has been successfully listed!')
            return redirect('newsfeed:newsfeed')
    else:
        form = PostProductForm()
    return render(request, 'post_product.html', {'form': form})


@login_required
def profile(request, pk):
    if pk is None:
        pk = request.user.pk
    user = get_object_or_404(User, pk=pk)
    profile = user.profile
    is_owner = user == request.user

    # Move the ratings query to the top
    ratings = Rating.objects.filter(rated_user=user)

    # Calculate the summary ratings
    average_rating, star_equivalent_average_rating, num_ratings = get_rating_summary(ratings)

    if request.method == 'POST':
        if is_owner:
            edit_form = ProfileForm(request.POST, instance=profile)
            if edit_form.is_valid():
                edit_form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('newsfeed:newsfeed')
        else:
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                rating = rating_form.save(commit=False)
                rating.user = request.user
                rating.rated_user = user
                rating.save()
                messages.success(request, 'Your review has been submitted successfully!')
                # Refresh the ratings query to include the newly submitted rating
                ratings = Rating.objects.filter(rated_user=user)
                # Recalculate the summary ratings
                average_rating, star_equivalent_average_rating, num_ratings = get_rating_summary(ratings)

    if is_owner:
        edit_form = ProfileForm(instance=profile)
        rating_form = None
    else:
        edit_form = None
        rating_form = RatingForm()

    products = Product.objects.filter(user=user, deleted_at__isnull=True)

    # Pass ratings and summary ratings to the template context in all cases
    return render(request, 'profile.html',
                  {'products': products, 'edit_form': edit_form, 'rating_form': rating_form, 'user': user,
                   'is_owner': is_owner, 'ratings': ratings, 'average_rating': average_rating,
                   'star_equivalent_average_rating': star_equivalent_average_rating, 'num_ratings': num_ratings})

def get_rating_summary(ratings):
    if ratings:
        average_rating = sum(rating.rating for rating in ratings) / len(ratings)
        if average_rating is not None:
            star_equivalent_average_rating = round(average_rating, 1)  # assuming 1 decimal place
        else:
            star_equivalent_average_rating = None
        num_ratings = len(ratings)
    else:
        average_rating = None
        star_equivalent_average_rating = None
        num_ratings = 0
    return average_rating, star_equivalent_average_rating, num_ratings

@login_required
def delete_listing(request, pk):
    listing = get_object_or_404(Product, pk=pk)
    if listing.user == request.user:
        listing.deleted_at = timezone.now()
        listing.save()
        messages.success(request, 'Listing deleted successfully!')
        return redirect('newsfeed:profile', pk=request.user.pk)
    else:
        messages.error(request, 'You do not have permission to delete this listing.')
        return redirect('newsfeed:profile', pk=request.user.pk)
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('newsfeed:newsfeed')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def edit_listing(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.user == request.user:
        if request.method == 'POST':
            form = PostProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                messages.success(request, 'Listing updated successfully!')
                return redirect('newsfeed:newsfeed')
        else:
            form = PostProductForm(instance=product)
        return render(request, 'edit_listing.html', {'form': form})
    else:
        messages.error(request, 'You do not have permission to edit this listing.')
        return redirect('newsfeed:newsfeed')

@login_required
def report_listing(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.user == request.user:
        messages.error(request, 'You cannot report your own listing.')
        return redirect('newsfeed:newsfeed')
    if request.method == 'POST':
        reason = request.POST.get('reason')
        report = Report.objects.create(product=product, user=request.user, reason=reason)
        messages.success(request, 'Listing reported successfully!')
        return redirect('newsfeed:newsfeed')
    return render(request, 'report_listing.html')

@login_required
def report_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('reason')
        report = UserReport.objects.create(user=user, reported_by=request.user, reason=reason)
        messages.success(request, 'User  reported successfully!')
        return redirect('newsfeed:newsfeed')
    return render(request, 'report_user.html')

def category_selection(request):
    return render(request, 'category_selection.html')

def search(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            users = User.objects.filter(username__icontains=query, is_superuser=False)  # Exclude superusers
            products = Product.objects.filter(title__icontains=query) | Product.objects.filter(description__icontains=query)
            products = products.filter(is_active=True, deleted_at__isnull=True).order_by('-created_at')
            for product in products:
                product.created_at = timezone.localtime(product.created_at)
            return render(request, 'search_results.html', {'query': query, 'users': users, 'products': products})
    return redirect('newsfeed:newsfeed')

from django.shortcuts import render
from .models import Product

def electronics(request):
    products = Product.objects.filter(category='Electronics', is_active=True, deleted_at__isnull=True)
    for product in products:
        product.created_at = timezone.localtime(product.created_at)
    return render(request, 'electronics.html', {'products': products})

def fashion(request):
    products = Product.objects.filter(category='Fashion and Beauty', is_active=True, deleted_at__isnull=True)
    for product in products:
        product.created_at = timezone.localtime(product.created_at)
    return render(request, 'fashion.html', {'products': products})

def garden(request):
    products = Product.objects.filter(category='Home and Garden', is_active=True, deleted_at__isnull=True)
    for product in products:
        product.created_at = timezone.localtime(product.created_at)
    return render(request, 'garden.html', {'products': products})

def sports(request):
    products = Product.objects.filter(category='Sports and Leisure', is_active=True, deleted_at__isnull=True)
    for product in products:
        product.created_at = timezone.localtime(product.created_at)
    return render(request, 'sports.html', {'products': products})

@login_required
@user_passes_test(is_staff)
def user_reports(request):
    reports = UserReport.objects.all()
    return render(request, 'user_reports.html', {'reports': reports})
