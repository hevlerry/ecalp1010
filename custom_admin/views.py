from datetime import timezone
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from newsfeed.models import Report, UserReport, Product
from main.models import ContactMessage
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

def is_staff(user):
    return user.is_staff or user.is_superuser

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser and not request.user.is_staff:
        return redirect('newsfeed')
    return render(request, 'admin_dashboard.html')

@login_required
@user_passes_test(is_staff)
def users(request):
    users = User.objects.all()
    return render(request, 'users.html', {'users': users})

@login_required
@user_passes_test(is_staff)
def user_details(request, pk):
        user = get_object_or_404(User, pk=pk)
        posted_listings = Product.objects.filter(user=user)
        return render(request, 'user_details.html', {'user': user, 'posted_listings': posted_listings})

@login_required
@user_passes_test(is_staff)
def delete_user(request, pk):
    user = User.objects.get(pk=pk)
    user.delete()
    return redirect('custom_admin:users')

@login_required
@user_passes_test(is_staff)
def contact_messages(request):
    messages = ContactMessage.objects.all()
    return render(request, 'messages.html', {'messages': messages})

@login_required
@user_passes_test(is_staff)
def products(request):
    products = Product.objects.filter(deleted_at__isnull=True)  # Assuming you have a 'deleted_at' field
    return render(request, 'products.html', {'products': products})

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

@login_required
@user_passes_test(is_staff)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user.has_perm('custom_admin.delete_product', product):
        product.deleted_at = timezone.now()
        product.save()
        messages.success(request, 'Product deleted successfully.')
        return redirect('custom_admin:admin_dashboard')
    else:
        return HttpResponseForbidden()

@login_required
@user_passes_test(is_staff)
def listing_reports(request):
    reports = Report.objects.all()
    return render(request, 'listing_reports.html', {'reports': reports})

@login_required
@user_passes_test(is_staff)
def user_reports(request):
    reports = UserReport.objects.all()
    return render(request, 'user_reports.html', {'reports': reports})

@login_required
@user_passes_test(lambda user: user.is_staff or user.is_superuser)
def delete_listing_report(request, pk):
    report = Report.objects.get(pk=pk)
    report.delete()
    return redirect('custom_admin:listing_reports')

@login_required
@user_passes_test(lambda user: user.is_staff or user.is_superuser)
def delete_message(request, pk):
    message = ContactMessage.objects.get(pk=pk)
    message.delete()
    return redirect('custom_admin:messages')

@login_required
@user_passes_test(lambda user: user.is_staff or user.is_superuser)
def delete_user_report(request, pk):
    report = UserReport.objects.get(pk=pk)
    report.delete()
    return redirect('custom_admin:user_reports')