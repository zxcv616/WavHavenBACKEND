from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Beat, Genre, User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .forms import RegisterForm, BeatForm

# No decorator here - should be accessible to everyone
def beat_list(request):
    query = request.GET.get('q', '')
    beats = Beat.objects.all().order_by('-created_at')
    
    if query:
        beats = beats.filter(
            Q(title__icontains=query) |
            Q(producer__username__icontains=query) |
            Q(genre__name__icontains=query) |
            Q(tags__icontains=query)
        ).distinct()
    
    return render(request, 'store/beat_list.html', {'beats': beats})

# No decorator here - should be accessible to everyone
def beat_detail(request, pk):
    beat = get_object_or_404(Beat, pk=pk)
    return render(request, 'store/beat_detail.html', {'beat': beat})

def genres(request):
    genres = Genre.objects.all()
    return render(request, 'store/genres.html', {'genres': genres})

# Only this view requires login
@login_required
def beat_upload(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        audio_file = request.FILES.get('audio_file')
        price = request.POST.get('price')
        bpm = request.POST.get('bpm')
        key = request.POST.get('key')
        tags = request.POST.get('tags')
        genre_id = request.POST.get('genre')
        
        if title and audio_file and price:
            beat = Beat(
                title=title,
                audio_file=audio_file,
                price=price,
                producer=request.user,
                bpm=bpm,
                key=key,
                tags=tags,
                genre_id=genre_id
            )
            if 'cover_image' in request.FILES:
                beat.cover_image = request.FILES['cover_image']
            beat.save()
            messages.success(request, 'Beat uploaded successfully!')
            return redirect('beat_detail', pk=beat.pk)
        
    genres = Genre.objects.all()
    return render(request, 'store/beat_upload.html', {'genres': genres})

@login_required
def manage_genres(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to manage genres.')
        return redirect('beat_list')
        
    if request.method == 'POST':
        genre_name = request.POST.get('genre_name')
        if genre_name:
            Genre.objects.create(name=genre_name)
            messages.success(request, f'Genre "{genre_name}" created successfully!')
        return redirect('manage_genres')
        
    genres = Genre.objects.all().order_by('name')
    return render(request, 'store/manage_genres.html', {'genres': genres})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('beat_list')
    else:
        form = RegisterForm()
    return render(request, 'store/register.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    beats = Beat.objects.filter(producer=user)
    
    context = {
        'beats': beats,
        'beats_count': beats.count(),
        'total_sales': 0,  # Placeholder until sales system is implemented
        'total_plays': 0,  # Placeholder until play tracking is implemented
        'recent_activities': []  # Placeholder for activity tracking
    }
    
    return render(request, 'store/dashboard.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        # Update profile
        profile = request.user.userprofile
        profile.bio = request.POST.get('bio', '')
        profile.website = request.POST.get('website', '')
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        profile.save()
        
        # Update user
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('dashboard')
        
    return render(request, 'store/edit_profile.html')

@login_required
def delete_beat(request, pk):
    beat = get_object_or_404(Beat, pk=pk, producer=request.user)
    if request.method == 'POST':
        beat.delete()
        messages.success(request, 'Beat deleted successfully!')
        return redirect('dashboard')
    return render(request, 'store/delete_beat_confirm.html', {'beat': beat})

def logout_view(request):
    logout(request)
    return redirect('beat_list')

@login_required
def beat_edit(request, pk):
    beat = get_object_or_404(Beat, pk=pk, producer=request.user)
    
    if request.method == 'POST':
        form = BeatForm(request.POST, request.FILES, instance=beat)
        if form.is_valid():
            form.save()
            messages.success(request, 'Beat updated successfully!')
            return redirect('dashboard')
    else:
        form = BeatForm(instance=beat)
    
    return render(request, 'store/beat_edit.html', {'form': form, 'beat': beat})

@login_required
def beat_delete(request, pk):
    beat = get_object_or_404(Beat, pk=pk, producer=request.user)
    
    if request.method == 'POST':
        beat.delete()
        messages.success(request, 'Beat deleted successfully!')
        return redirect('dashboard')
    
    return render(request, 'store/beat_delete.html', {'beat': beat})



