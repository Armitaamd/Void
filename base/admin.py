
from django.contrib import admin
from .models import Artist, Genre, Album, Song, Playlist, UserProfile, SongPlay , SoundEffect

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'release_date')
    list_filter = ('artist',)
    search_fields = ('title', 'artist__name')


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album', 'language', 'release_date', 'is_void_pick')
    list_filter = ('artist', 'genres', 'language', 'is_void_pick')
    search_fields = ('title', 'artist__name', 'album__title')


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'likes_count')
    search_fields = ('title', 'user__username')

    def likes_count(self, obj):
        return obj.likes.count()

    likes_count.short_description = 'تعداد لایک‌ها'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)


@admin.register(SongPlay)
class SongPlayAdmin(admin.ModelAdmin):
    list_display = ('song', 'played_at')
    list_filter = ('played_at',)
    search_fields = ('song__title', 'song__artist__name')
    ordering = ('-played_at',)





admin.site.register(SoundEffect)    