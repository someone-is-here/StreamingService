from django.urls import path

from streaming.views import Home, AlbumsListView, TracksListView, ArtistsListView, PlaylistsListView, TrackCreateView, \
    AlbumCreateView, TrackDetailView, AlbumDetailView, TrackUpdateView, TrackDeleteView, AlbumUpdateView, \
    AlbumDeleteView, PlaylistListView, RegisterAbstractUser, LoginUser, logout_user, SubscriptionUpdateView, \
    PlaylistCreateView, PlaylistAddTrackView, PlaylistRemoveTrackView, ArtistsAddInstrumentView, ArtistsAddLabelView, \
    ArtistsAddGenreView

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('playlists/', PlaylistsListView.as_view(), name='playlists'),
    path('register/', RegisterAbstractUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('subscription/<int:abstr_user_id>/', SubscriptionUpdateView.as_view(), name='change_subscription'),
    path('user/<int:user_id>/update/', PlaylistsListView.as_view(), name='update_user'),
    path('playlist/<int:playlist_id>/listen/', PlaylistListView.as_view(), name='selected_playlist'),
    path('tracks/', TracksListView.as_view(), name='tracks'),
    path('playlist/create', PlaylistCreateView.as_view(), name='create_playlist'),
    path('playlist/<int:playlist_id>/add/', PlaylistAddTrackView.as_view(), name='add_track_to_playlist'),
    path('playlist/<int:playlist_id>/remove/<int:track_id>/', PlaylistRemoveTrackView.as_view(), name='remove_track_from_playlist'),
    path('tracks/create/', TrackCreateView.as_view(), name='create_track'),
    path('tracks/<int:track_id>/', TrackDetailView.as_view(), name='detail_track'),
    path('tracks/<int:track_id>/update/', TrackUpdateView.as_view(), name='update_track'),
    path('tracks/<int:track_id>/delete/', TrackDeleteView.as_view(), name='delete_track'),
    path('albums/create/', AlbumCreateView.as_view(), name='create_album'),
    path('albums/<int:album_id>/', AlbumDetailView.as_view(), name='detail_album'),
    path('albums/<int:album_id>/update/', AlbumUpdateView.as_view(), name='update_album'),
    path('albums/<int:album_id>/delete/', AlbumDeleteView.as_view(), name='delete_album'),
    path('albums/', AlbumsListView.as_view(), name='albums'),
    path('artists/', ArtistsListView.as_view(), name='artists'),
    path('artists/<int:abstr_user_id>/add_instrument', ArtistsAddInstrumentView.as_view(), name='add_instrument'),
    path('artists/<int:abstr_user_id>/add_genre', ArtistsAddGenreView.as_view(), name='add_genre'),
    path('artists/<int:abstr_user_id>/add_label', ArtistsAddLabelView.as_view(), name='add_label'),
]
