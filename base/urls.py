from django.urls import path
from .views import (home, song_detail, artist_detail,
notes, trends, singers, sound_effects,
playlist, search, profile, record_song_play,
register, user_login, user_logout, create_playlist , 
playlist_detail , add_song_to_playlist , remove_song_from_playlist ,
toggle_playlist_like )



urlpatterns = [
    path('', home, name='home'),
    path('song/<int:song_id>/', song_detail, name='song_detail'),
    path('artist/<int:artist_id>/', artist_detail, name='artist_detail'),
    path('notes/', notes, name='notes'),
    path('trends/', trends, name='trends'),
    path('singers/', singers, name='singers'),
    path('sound-effects/', sound_effects, name='sound_effects'),
    path('playlist/', playlist, name='playlist'),
    path('search/', search, name='search'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('song/<int:song_id>/play/', record_song_play, name='record_song_play'),
    path('create-playlist/', create_playlist, name='create_playlist'),
    path('playlist/<int:playlist_id>/', playlist_detail, name='playlist_detail'),
    path('song/<int:song_id>/add-to-playlist/',add_song_to_playlist,name='add_song_to_playlist'),
    path('playlist/<int:playlist_id>/remove-song/<int:song_id>/',remove_song_from_playlist,name='remove_song_from_playlist'),
    path('playlist/<int:playlist_id>/like/',toggle_playlist_like,name='toggle_playlist_like'),
]