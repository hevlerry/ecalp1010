from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model


User = get_user_model()



from django.db import models
from django.utils import timezone

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    mobile_number = models.CharField(max_length=20)
    location = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50, choices=[('Electronics', 'Electronics'), ('Fashion and Beauty', 'Fashion and Beauty'), ('Home and Garden', 'Home and Garden'), ('Sports and Leisure', 'Sports and Leisure'), ('Others', 'Others')], default='Others')
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images')

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)

    def __str__(self):
        return self.user.username

def profile_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'profile.html', {'user': user})

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

from django.db import models
from django.contrib.auth.models import User

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rated_user')
    rating = models.IntegerField()
    comment = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.username} rated {self.rated_user.username} {self.rating}/5'

class Report(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Listing Report'
        verbose_name_plural = 'Listing Reports'

    def __str__(self):
        return f"{self.product.title} listing reported by {self.user.username}"

class UserReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_user')
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reporter')
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} reported by {self.reported_by.username}"