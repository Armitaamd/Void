from django.db import models
from django.contrib.auth.models import User


class Artist(models.Model):
    name = models.CharField(max_length=150)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='artists/', blank=True, null=True)

    class Meta:
        verbose_name = 'خواننده'
        verbose_name_plural = 'خواننده‌ها'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'سبک موسیقی'
        verbose_name_plural = 'سبک‌های موسیقی'

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    cover = models.ImageField(upload_to='albums/', blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'آلبوم'
        verbose_name_plural = 'آلبوم‌ها'

    def __str__(self):
        return self.title


class Song(models.Model):
    title = models.CharField(max_length=200)

    LANGUAGE_CHOICES = [
        ('persian', 'فارسی'),
        ('english', 'انگلیسی'),
        ('other', 'سایر زبان‌ها'),
    ]

    language = models.CharField(
        max_length=20,
        choices=LANGUAGE_CHOICES,
        default='other'
    )

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='songs')
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, blank=True, null=True, related_name='songs')
    genres = models.ManyToManyField(Genre, blank=True, related_name='songs')
    audio_file = models.FileField(upload_to='songs/')
    cover = models.ImageField(upload_to='songs/covers/', blank=True, null=True)
    duration = models.PositiveIntegerField(default=0)
    release_date = models.DateField(blank=True, null=True)
    is_void_pick = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'آهنگ'
        verbose_name_plural = 'آهنگ‌ها'

    def __str__(self):
        return self.title


class Playlist(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='playlists',
        blank=True,
        null=True
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to='playlists/', blank=True, null=True)
    songs = models.ManyToManyField(Song, blank=True, related_name='playlists')
    likes = models.ManyToManyField(
        User,
        blank=True,
        related_name='liked_playlists'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'پلی‌لیست'
        verbose_name_plural = 'پلی‌لیست‌ها'

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='profiles/', blank=True, null=True)

    class Meta:
        verbose_name = 'پروفایل کاربر'
        verbose_name_plural = 'پروفایل‌های کاربران'

    def __str__(self):
        return self.user.username


class SongPlay(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='plays')
    played_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'تاریخچه پخش'
        verbose_name_plural = 'تاریخچه پخش آهنگ‌ها'

    def __str__(self):
        return self.song.title


class SoundEffect(models.Model):
    title = models.CharField(max_length=200)
    audio_file = models.FileField(upload_to='sound_effects/')
    cover = models.ImageField(
        upload_to='sound_effects/covers/',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'افکت صوتی'
        verbose_name_plural = 'افکت‌های صوتی'

    def __str__(self):
        return self.title
