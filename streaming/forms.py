from django.forms import ModelForm
from django import forms

from streaming.models import Tracks, Albums, AbstractUsers, Users, Artists, Playlists, PlaylistTrack, ArtistInstrument, \
    ArtistLabel, ArtistGenre

from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    """
    A form that creats a custom user with no privilages
    form a provided email and password.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = AbstractUsers
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    """
    A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = AbstractUsers
        fields = '__all__'


class TracksForm(ModelForm):
    class Meta:
        model = Tracks
        fields = ['name', 'timing', 'storage_path', 'track', 'photo', 'album']


class AlbumsForm(ModelForm):
    class Meta:
        model = Albums
        fields = ['name', 'release_date', 'icon']


class UserCreationForm(ModelForm):
    email = forms.CharField(widget=forms.EmailInput)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = AbstractUsers
        fields = ['login', 'email', 'role', 'password1', 'password2']


class UserForm(ModelForm):
    class Meta:
        model = Users
        fields = ['subscription']


class PlaylistForm(ModelForm):
    class Meta:
        model = Playlists
        fields = ['name']


class PlaylistTrackForm(ModelForm):
    class Meta:
        model = PlaylistTrack
        fields = ['track']


class ArtistForm(ModelForm):
    class Meta:
        model = Artists
        fields = ['name', 'website', 'tour_dates', 'country']


class ArtistInstrumentForm(ModelForm):
    class Meta:
        model = ArtistInstrument
        fields = ['instrument']


class ArtistLabelForm(ModelForm):
    class Meta:
        model = ArtistLabel
        fields = ['label']


class ArtistGenreForm(ModelForm):
    class Meta:
        model = ArtistGenre
        fields = ['genre']
