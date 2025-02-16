from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class Genre(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Beat(models.Model):
    producer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    audio_file = models.FileField(
        upload_to='beats/',
        validators=[
            FileExtensionValidator(allowed_extensions=['mp3', 'wav'])
        ]
    )
    price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bpm = models.IntegerField(null=True, blank=True)
    key = models.CharField(max_length=50, null=True, blank=True)
    tags = models.CharField(max_length=500, null=True, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    cover_image = models.ImageField(upload_to='beat_covers/', null=True, blank=True)
    sales_count = models.IntegerField(default=0)
    play_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_cover_image_url(self):
        if self.cover_image:
            return self.cover_image.url
        return '/static/store/images/default_cover.png'  # We'll create this default image

class Cart(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    beat = models.ForeignKey(Beat, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    website = models.URLField(blank=True)
    purchased_beats = models.ManyToManyField(Beat, related_name='buyers')
    
    def __str__(self):
        return self.user.username

# Signal to create UserProfile automatically
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'userprofile'):
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()

class License(models.Model):
    name = models.CharField(max_length=100)  # e.g., "Basic", "Premium", "Exclusive"
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    
class BeatLicense(models.Model):
    beat = models.ForeignKey(Beat, on_delete=models.CASCADE)
    license = models.ForeignKey(License, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
