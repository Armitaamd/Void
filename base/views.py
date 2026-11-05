from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.db import IntegrityError, transaction
from .models import Song, SongPlay, UserProfile, Playlist, Artist , SoundEffect
from django.http import JsonResponse
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST





def home(request):
    seven_days_ago = timezone.now() - timedelta(days=7)

    trending_songs = Song.objects.filter(
        plays__played_at__gte=seven_days_ago
    ).annotate(
        play_count=Count('plays')
    ).order_by('-play_count')[:15]

    popular_songs = Song.objects.annotate(
        play_count=Count('plays')
    ).order_by('-play_count')[:15] 

    foreign_songs = Song.objects.filter(
        language__in=['english', 'other']
    ).order_by('-created_at')[:15]

    persian_songs = Song.objects.filter(
        language='persian'
    ).order_by('-created_at')[:15]

    popular_artists = Artist.objects.all()[:15]

    sound_effects = SoundEffect.objects.all()[:15] 

    new_songs = Song.objects.filter(
        release_date__isnull=False
    ).order_by('-release_date')[:15]

    return render(request, 'index.html', {
        'new_songs': new_songs,
        'trending_songs': trending_songs,
        'popular_songs': popular_songs,
        'popular_artists': popular_artists,
        'foreign_songs': foreign_songs,
        'persian_songs': persian_songs,
        'sound_effects': sound_effects,
    })



def song_detail(request, song_id):
    song = get_object_or_404(Song, id=song_id)

    artist_songs = Song.objects.filter(
        artist=song.artist
    ).exclude(id=song.id)[:8]

    similar_songs = Song.objects.filter(
        genres__in=song.genres.all()
    ).exclude(id=song.id).distinct()[:8]

    return render(request, 'SongProfile.html', {
        'song': song,
        'artist_songs': artist_songs,
        'similar_songs': similar_songs,
    })


def artist_detail(request, artist_id):
    from .models import Artist

    artist = get_object_or_404(Artist, id=artist_id)

    artist_songs = Song.objects.filter(
        artist=artist
    ).order_by('-release_date')

    return render(request, 'ArtistProfile.html', {
        'artist': artist,
        'artist_songs': artist_songs,
    })


def notes(request):
    return render(request, 'Notes.html')


def trends(request):
    seven_days_ago = timezone.now() - timedelta(days=7)
    thirty_days_ago = timezone.now().date() - timedelta(days=30)

    trending_songs = Song.objects.filter(
        plays__played_at__gte=seven_days_ago
    ).annotate(
        play_count=Count('plays')
    ).order_by('-play_count')[:20]

    new_releases = Song.objects.filter(
        release_date__gte=thirty_days_ago
    ).order_by('-release_date')[:15]

    void_picks = Song.objects.filter(
        is_void_pick=True
    ).order_by('-created_at')[:10]

    return render(request, 'Trends.html', {
        'trending_songs': trending_songs,
        'new_releases': new_releases,
        'void_picks': void_picks,
    })


def singers(request):
    artists = Artist.objects.all().order_by('name')

    return render(request, 'Singers.html', {
        'artists': artists,
    })

def sound_effects(request):
    effects = SoundEffect.objects.all()

    return render(request, 'SoundEffect.html', {
        'effects': effects,
    }) 


def playlist(request):
    playlists = Playlist.objects.all().order_by('-created_at')

    return render(request, 'PlayList.html', {
        'playlists': playlists
    })


def search(request):
    query = request.GET.get('q', '').strip()

    songs = Song.objects.none()
    artists = Artist.objects.none()

    if query:
        songs = Song.objects.filter(
            Q(title__icontains=query) |
            Q(artist__name__icontains=query)
        ).distinct()

        artists = Artist.objects.filter(
            name__icontains=query
        )

    return render(request, 'search.html', {
        'query': query,
        'songs': songs,
        'artists': artists,
    })




@login_required(login_url='login')
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    user_playlists = Playlist.objects.filter(
        user=request.user
    ).order_by('-created_at')

    liked_playlists = request.user.liked_playlists.all().order_by('-created_at')

    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()

        if request.FILES.get('avatar'):
            user_profile.avatar = request.FILES.get('avatar')
            user_profile.save()

        return redirect('profile')

    return render(request, 'Profile.html', {
        'profile': user_profile,
        'user_playlists': user_playlists,
        'liked_playlists': liked_playlists,
    })


@login_required(login_url='login')
def create_playlist(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        cover = request.FILES.get('cover')

        if title:
            Playlist.objects.create(
                user=request.user,
                title=title,
                description=description,
                cover=cover
            )

            return redirect('profile')

    return render(request, 'create_playlist.html')



def playlist_detail(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)

    return render(request, 'PlaylistDetail.html', {
        'playlist': playlist,
        'songs': playlist.songs.all(),
    })



def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            return render(request, 'register.html', {
                'error': 'لطفاً نام کاربری و رمز عبور را وارد کنید.'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'این نام کاربری قبلاً ثبت شده است.'
            })

        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )

            login(request, user)
            return redirect('profile')

        except IntegrityError:
            return render(request, 'register.html', {
                'error': 'این نام کاربری قبلاً ثبت شده است.'
            })

    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('profile')

        return render(request, 'login.html', {
            'error': 'نام کاربری یا رمز عبور اشتباه است.'
        })

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('home')

@require_POST
def record_song_play(request, song_id):
    song = get_object_or_404(Song, id=song_id)

    SongPlay.objects.create(song=song)

    return JsonResponse({'status': 'success'})    



@login_required(login_url='login')
def add_song_to_playlist(request, song_id):
    if request.method == 'POST':
        song = get_object_or_404(Song, id=song_id)
        playlist_id = request.POST.get('playlist_id')

        playlist = get_object_or_404(
            Playlist,
            id=playlist_id,
            user=request.user
        )

        playlist.songs.add(song)

        return redirect('playlist_detail', playlist_id=playlist.id)

    return redirect('song_detail', song_id=song_id)



@login_required(login_url='login')
def remove_song_from_playlist(request, playlist_id, song_id):
    if request.method == 'POST':
        playlist = get_object_or_404(
            Playlist,
            id=playlist_id,
            user=request.user
        )

        song = get_object_or_404(
            Song,
            id=song_id
        )

        playlist.songs.remove(song)

        return redirect('playlist_detail', playlist_id=playlist.id)

    return redirect('profile')


@login_required(login_url='login')
@require_POST
def toggle_playlist_like(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)

    if playlist.likes.filter(id=request.user.id).exists():
        playlist.likes.remove(request.user)
        liked = False
    else:
        playlist.likes.add(request.user)
        liked = True

    return JsonResponse({
        'liked': liked,
        'likes_count': playlist.likes.count()
    })