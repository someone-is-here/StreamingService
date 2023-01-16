from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from streaming.models import Tracks, Albums, Genres, Labels, Roles, Artists, Users, Playlists, Logging, AbstractUsers, \
    Subscriptions, Instruments, Countries, ArtistAlbum, ArtistGenre, ArtistInstrument, ArtistLabel, PlaylistAbstrUser, \
    PlaylistTrack, TrackGenre
from django.utils.translation import gettext_lazy as _


class AbstractUsersConfig(UserAdmin):
    fieldsets = (
        (None, {'fields': ('login','username', 'email', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_filedsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2')}
         ),
    )
    list_display = ('email', 'is_staff')
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(Tracks)
admin.site.register(AbstractUsers, AbstractUsersConfig)
admin.site.register(Albums)
admin.site.register(Genres)
admin.site.register(Labels)
admin.site.register(Instruments)
admin.site.register(Roles)
admin.site.register(Artists)
admin.site.register(Users)
admin.site.register(Playlists)
admin.site.register(Countries)
admin.site.register(Logging)
admin.site.register(ArtistAlbum)
admin.site.register(ArtistGenre)
admin.site.register(ArtistInstrument)
admin.site.register(ArtistLabel)
admin.site.register(Subscriptions)
admin.site.register(PlaylistAbstrUser)
admin.site.register(PlaylistTrack)
admin.site.register(TrackGenre)

