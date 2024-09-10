from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from .models import Song
from .forms import SongForm, UserRegisterForm  # Import the UserRegisterForm
from django.contrib import messages

@login_required
def song_list(request):
    songs = Song.objects.filter(user=request.user)
    return render(request, 'songs/song_list.html', {'songs': songs})

@login_required
def song_add(request):
    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            song = form.save(commit=False)
            song.user = request.user
            song.save()
            return redirect('song_list')
    else:
        form = SongForm()
    return render(request, 'songs/song_form.html', {'form': form})

@login_required
def song_edit(request, song_id):
    song = get_object_or_404(Song, id=song_id, user=request.user)
    if request.method == 'POST':
        form = SongForm(request.POST, instance=song)
        if form.is_valid():
            form.save()
            return redirect('song_list')
    else:
        form = SongForm(instance=song)
    return render(request, 'songs/song_form.html', {'form': form})

@login_required
def song_delete(request, song_id):
    song = get_object_or_404(Song, id=song_id, user=request.user)
    if request.method == 'POST':
        song.delete()
        return redirect('song_list')
    return render(request, 'songs/song_confirm_delete.html', {'song': song})

@login_required
def user_logout(request):
    logout(request)
    return render(request, 'registration/logout.html', {})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            messages.success(request, f'Your account has been created! You are now logged in.')
            return redirect('song_list')  # Redirect to the song list after successful registration
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def homepage(request):
    return render(request, 'songs/homepage.html')