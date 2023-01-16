from datetime import datetime, timezone

from django.shortcuts import reverse

from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from streaming.forms import TracksForm, AlbumsForm, UserCreationForm, UserForm, ArtistForm, PlaylistForm, \
    PlaylistTrackForm, ArtistInstrumentForm, ArtistLabelForm, ArtistGenreForm
from streaming.models import Albums, Tracks, Artists, Playlists, Labels, Instruments, Genres, AbstractUsers, Users, \
    PlaylistTrack
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.contrib.auth import logout, login
from django.contrib.auth.hashers import make_password
from django.db import connections

from streaming.utils import DataMixin
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin


class Home(DataMixin, TemplateView):
    template_name = 'streaming/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        print(kwargs)
        context = super().get_context_data(**kwargs)
        additional_context = self.get_user_context(title='home', request=self.request)

        return dict(list(context.items()) + list(additional_context.items()))


class AlbumsListView(DataMixin, TemplateView):
    template_name = 'streaming/albums.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['albums'] = Albums.objects.raw('SELECT * FROM albums')
        additional_context = self.get_user_context(title='albums', request=self.request)

        return dict(list(context.items()) + list(additional_context.items()))


class TracksListView(DataMixin, TemplateView):
    template_name = 'streaming/tracks.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tracks'] = Tracks.objects.raw('SELECT * FROM tracks')
        additional_context = self.get_user_context(title='tracks', request=self.request)
        print(context)
        print(additional_context)

        return dict(list(context.items()) + list(additional_context.items()))


class ArtistsListView(DataMixin, TemplateView):
    template_name = 'streaming/artists.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['artists'] = list(Artists.objects.raw(
            " select A.id, A.name, A.website, A.tour_dates, C.title as country_title, C.id, A.country_id "
            "from artists A "
            "INNER JOIN countries C ON A.country_id=C.id "))

        for i in range(len(context['artists'])):
            print(context['artists'][i].pk)
            query = "SELECT L.id, L.name as label_title, L.website as label_website, L.foundation_year as label_year FROM artist_label AL " \
                    "INNER JOIN labels L ON AL.label_id=L.id  WHERE %s=AL.artist_id " % context['artists'][i].pk
            query_instr = "SELECT I.id, I.title as instrument_title FROM artist_instrument AI " \
                          "INNER JOIN instruments I ON AI.instrument_id=I.id  WHERE %s=AI.artist_id " % \
                          context['artists'][i].pk
            query_genres = "SELECT G.id, G.name as genre_name FROM artist_genre AG " \
                           "INNER JOIN genres G ON AG.genre_id=G.id  WHERE %s=AG.artist_id " % \
                           context['artists'][i].pk
            context['artists'][i] = {'name': context['artists'][i].name,
                                     'website': context['artists'][i].website,
                                     'tour_dates': context['artists'][i].tour_dates,
                                     'country_title': context['artists'][i].country_title,
                                     'labels': Labels.objects.raw(query),
                                     'instruments': Instruments.objects.raw(query_instr),
                                     'genres': Genres.objects.raw(query_genres)}

        additional_context = self.get_user_context(title='artists', request=self.request)

        return dict(list(context.items()) + list(additional_context.items()))


class PlaylistsListView(DataMixin, TemplateView):
    template_name = 'streaming/playlists.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['playlists'] = list(Playlists.objects.raw("SELECT P.id, P.name FROM playlists AS P "))
        for i in range(len(context['playlists'])):
            query = "SELECT T.id, T.name from tracks as T " \
                    "INNER JOIN playlist_track as PT ON PT.track_id=T.id " \
                    "WHERE %s=PT.playlist_id" % context['playlists'][i].id
            context['playlists'][i] = {'id': context['playlists'][i].id,
                                       'name': context['playlists'][i].name,
                                       'tracks': Tracks.objects.raw(query)}
        additional_context = self.get_user_context(title='playlists', request=self.request)

        return dict(list(context.items()) + list(additional_context.items()))


class TrackCreateView(DataMixin, LoginRequiredMixin, FormView):
    login_url = '/login/'
    template_name = 'streaming/create.html'
    form_class = TracksForm

    def get_context_data(self, **kwargs):
        print(kwargs)
        context = super().get_context_data(**kwargs)
        additional_context = self.get_user_context(title='tracks', request=self.request)

        return dict(list(context.items()) + list(additional_context.items()))

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tracks')


class TrackDetailView(DataMixin, LoginRequiredMixin, DetailView):
    model = Tracks
    template_name = 'streaming/detail_track.html'
    pk_url_kwarg = 'track_id'
    login_url = '/login/'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        print(kwargs)
        context = super().get_context_data(**kwargs)
        additional_context = self.get_user_context(title='tracks', request=self.request)

        cursor = connections['default'].cursor()
        cursor.execute('SELECT A.id FROM tracks T '
                       'INNER JOIN albums Al ON Al.id=T.album_id '
                       'INNER JOIN artist_album AA ON AA.album_id=Al.id '
                       'INNER JOIN artists A ON AA.artist_id=A.id '
                       'WHERE T.id=%s',
                       [self.kwargs['track_id']])
        res = cursor.fetchone()

        if (res and res[0] == self.request.user.id) or self.request.user.role.id == 1:
            context['permission'] = True
        else:
            context['permission'] = False

        return dict(list(context.items()) + list(additional_context.items()))


class TrackUpdateView(DataMixin, LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Tracks
    pk_url_kwarg = 'track_id'
    fields = ['name', 'timing', 'storage_path', 'track', 'photo', 'album']
    template_name = 'streaming/create.html'
    success_url = reverse_lazy('tracks')

    def get_context_data(self, **kwargs):
        print(kwargs)
        context = super().get_context_data(**kwargs)
        additional_context = self.get_user_context(title='tracks', request=self.request)

        return dict(list(context.items()) + list(additional_context.items()))


class TrackDeleteView(DataMixin, LoginRequiredMixin, DeleteView):
    model = Tracks
    login_url = '/login/'
    pk_url_kwarg = 'track_id'
    template_name = 'streaming/delete.html'
    success_url = reverse_lazy('tracks')

    def get_context_data(self, **kwargs):
        print(kwargs)
        context = super().get_context_data(**kwargs)
        additional_context = self.get_user_context(title='tracks', request=self.request)

        return dict(list(context.items()) + list(additional_context.items()))


class AlbumCreateView(DataMixin, LoginRequiredMixin, FormView):
    login_url = '/login/'
    template_name = 'streaming/create.html'
    form_class = AlbumsForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(title='album', request=self.request)

        return self.render_to_response(context=context)

    def form_valid(self, form):
        if int(form.data['release_date']) < 0 or datetime.now().year > int(form.data['release_date']):
            context = self.get_context_data(title='album', request=self.request)
            context['form'] = form
            context['error_messages'] = []
            context['error_messages'].append('Year doesn''t validate year constraints')
            return self.render_to_response(context=context)

        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('albums')


class AlbumDetailView(DataMixin, LoginRequiredMixin, DetailView):
    model = Albums
    template_name = 'streaming/detail_album.html'
    pk_url_kwarg = 'album_id'
    context_object_name = 'item'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        additional_context = self.get_user_context(title='album', request=self.request)

        context['tracks'] = Tracks.objects.raw('SELECT T.id, T.name as track_name, T.timing, T.likes, T.streaming,'
                                               'T.track, T.photo, T.album_id FROM tracks T WHERE T.album_id=%s',
                                               [kwargs['object'].pk])
        cursor = connections['default'].cursor()
        cursor.execute('SELECT A.id FROM artist_album AA '
                       'INNER JOIN artists A ON A.id=AA.artist_id WHERE AA.album_id=%s',
                       [self.kwargs['album_id']])
        res = cursor.fetchone()
        print(res, self.request.user.id)

        if (res and res[0] == self.request.user.id) or self.request.user.role.id == 1:
            context['permission'] = True
        else:
            context['permission'] = False

        return dict(list(context.items()) + list(additional_context.items()))


class AlbumUpdateView(DataMixin, LoginRequiredMixin, UpdateView):
    model = Albums
    login_url = '/login/'
    pk_url_kwarg = 'album_id'
    fields = ['name', 'release_date', 'icon']
    template_name = 'streaming/create.html'
    success_url = reverse_lazy('albums', )

    def get_context_data(self, **kwargs):
        print(kwargs)
        context = super().get_context_data(**kwargs)
        additional_context = self.get_user_context(title='album', request=self.request)

        return dict(list(context.items()) + list(additional_context.items()))

    def form_valid(self, form):
        if int(form.data['release_date']) < 0 or int(form.data['release_date']) > datetime.now().year:
            context = self.get_context_data(title='album', request=self.request)
            context['form'] = form
            context['error_messages'] = []
            context['error_messages'].append('Year doesn''t validate year constraints')
            return self.render_to_response(context=context)
        form.save()
        return super().form_valid(form)


class AlbumDeleteView(DataMixin, LoginRequiredMixin, DeleteView):
    model = Albums
    login_url = '/login/'
    pk_url_kwarg = 'album_id'
    template_name = 'streaming/delete.html'
    success_url = reverse_lazy('albums')

    def get_context_data(self, **kwargs):
        print(kwargs)
        context = super().get_context_data(**kwargs)
        additional_context = self.get_user_context(title='tracks', request=self.request)

        return dict(list(context.items()) + list(additional_context.items()))


class PlaylistListView(DataMixin, LoginRequiredMixin, DetailView):
    model = Playlists
    login_url = '/login/'
    template_name = 'streaming/tracks.html'
    pk_url_kwarg = 'playlist_id'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        additional_context = self.get_user_context(title='playlist', request=self.request)

        print(kwargs['object'].id)
        context['tracks'] = Tracks.objects.raw('SELECT T.id, T.name, T.timing, T.likes, T.streaming,'
                                               'T.track, T.photo, T.album_id FROM tracks AS T '
                                               'INNER JOIN playlist_track AS PT ON PT.track_id=T.id '
                                               'WHERE PT.playlist_id=%s', [kwargs['object'].id])
        print(context['tracks'])
        return dict(list(context.items()) + list(additional_context.items()))


def _get_form(request, formcls, prefix):
    data = request.POST if prefix in request.POST else None
    return formcls(data, prefix=prefix)


class RegisterAbstractUser(DataMixin, TemplateView):
    template_name = 'streaming/register.html'
    my_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        additional_context = self.get_user_context(title='register', request=self.request)

        return dict(list(context.items()) + list(additional_context.items()))

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        context['aform'] = UserCreationForm(prefix='aform_pre')
        context['cform'] = UserForm(prefix='cform_pre')
        context['bform'] = ArtistForm(prefix='bform_pre')

        self.my_context = context

        return self.render_to_response(context=self.my_context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        aform = _get_form(request, UserCreationForm, 'aform_pre')
        cform = _get_form(request, UserForm, 'cform_pre')
        bform = _get_form(request, ArtistForm, 'bform_pre')
        context['aform'] = aform
        context['error_messages'] = []

        if aform.is_valid():
            role = aform.instance.role_id
            if aform.cleaned_data['password1'] == aform.cleaned_data['password2']:
                cursor = connections['default'].cursor()
                cursor.execute('INSERT INTO abstract_users(last_login, is_superuser, username, '
                               'login, email, password,'
                               ' is_active, is_staff, role_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                               [datetime.now(timezone.utc), False, aform.instance.login, aform.instance.login,
                                aform.instance.email,
                                make_password(aform.cleaned_data['password1']), True, False, aform.instance.role_id])
                cursor.execute('select id, login from abstract_users WHERE login=%s',
                               [aform.instance.login])
                row = cursor.fetchone()
            else:
                context['error_messages'].append('Passwords are different')
                aform.instance.role_id = None
                return self.render_to_response(context=context)

            if role == 3:
                context['cform'] = cform
                if cform.is_valid():
                    cursor.execute('INSERT INTO users(abstr_user_id, subscription_id) VALUES (%s,%s)',
                                   [row[0], cform.instance.subscription.id])
                    login(self.request, AbstractUsers.object.get(pk=row[0]))
                    return HttpResponseRedirect(reverse('home'))
                else:
                    aform.instance.role_id = None
            if role == 2:
                context['bform'] = bform
                if bform.is_valid():
                    cursor.execute(
                        'INSERT INTO artists(id, name, website, tour_dates, country_id) VALUES (%s, %s, %s, %s, %s)',
                        [row[0], bform.instance.name, bform.instance.website,
                         bform.instance.tour_dates, bform.instance.country.id])
                    login(AbstractUsers.object.get(self.request, pk=row[0]))
                    return HttpResponseRedirect(reverse('home'))
                else:
                    aform.instance.role_id = None

        return self.render_to_response(context=context)


class LoginUser(DataMixin, LoginView):
    form_template = AuthenticationForm
    template_name = 'streaming/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        additional_context = self.get_user_context(title='login', request=self.request)

        return dict(list(context.items()) + list(additional_context.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class SubscriptionUpdateView(DataMixin, LoginRequiredMixin, UpdateView):
    model = Users
    pk_url_kwarg = 'abstr_user_id'
    fields = ['subscription']
    template_name = 'streaming/create.html'
    success_url = reverse_lazy('home',)
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        additional_context = self.get_user_context(title='album', request=self.request)

        return dict(list(context.items()) + list(additional_context.items()))


class PlaylistCreateView(DataMixin, LoginRequiredMixin, FormView):
    login_url = '/login/'
    template_name = 'streaming/create.html'
    form_class = PlaylistForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        additional_context = self.get_user_context(title='playlist', request=self.request)

        return dict(list(context.items()) + list(additional_context.items()))

    def form_valid(self, form):
        cursor = connections['default'].cursor()
        cursor.execute('INSERT INTO playlists(name) VALUES (%s)', [form.instance.name])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('playlists')


class PlaylistAddTrackView(DataMixin, LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'streaming/create.html'
    pk_url_kwarg = 'playlist_id'
    fields = ['track']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        additional_context = self.get_user_context(title='playlist', request=self.request)
        print(self.kwargs)
        return dict(list(context.items()) + list(additional_context.items()))

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        context['form'] = PlaylistTrackForm(prefix='form_pre')

        self.my_context = context

        return self.render_to_response(context=self.my_context)

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        additional_context = self.get_user_context(request=self.request)
        context['form'] = PlaylistTrackForm(prefix='form_pre')
        context = dict(list(context.items()) + list(additional_context.items()))

        cursor = connections['default'].cursor()
        cursor.execute('SELECT playlist_id, track_id FROM playlist_track WHERE playlist_id=%s AND track_id=%s', [self.kwargs['playlist_id'],request.POST['form_pre-track']])

        if cursor.fetchone():
            context['error_messages'] = ['Current track already exists',]
            print("error", context)
            return self.render_to_response(context=context)
        cursor.execute('INSERT INTO playlist_track(playlist_id, track_id) VALUES (%s, %s)', [self.kwargs['playlist_id'],
                                                                                              request.POST['form_pre-track']])
        return HttpResponseRedirect(reverse('playlists'))


class PlaylistRemoveTrackView(DataMixin, LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'streaming/delete.html'
    pk_url_kwarg = ('playlist_id', 'track_id')
    model = PlaylistTrack
    success_url = reverse_lazy('playlists')

    def get_context_data(self, *args, **kwargs):
        print(self.kwargs)
        context = super().get_context_data(**kwargs)
        additional_context = self.get_user_context(title='playlist', request=self.request)
        cursor = connections['default'].cursor()
        cursor.execute('SELECT id, name FROM tracks WHERE id=%s',
                       [self.kwargs['track_id']])
        row = cursor.fetchone()
        context['object'] = row[1]
        return dict(list(context.items()) + list(additional_context.items()))

    def post(self, request, *args, **kwargs):
        cursor = connections['default'].cursor()
        cursor.execute('DELETE FROM playlist_track WHERE playlist_id=%s AND track_id=%s',
                       [self.kwargs['playlist_id'], self.kwargs['track_id']])
        return HttpResponseRedirect(reverse('playlists'))


class ArtistsAddInstrumentView(DataMixin, LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'streaming/create.html'
    pk_url_kwarg = 'abstr_user_id'
    model = PlaylistTrack
    success_url = reverse_lazy('artists')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        additional_context = self.get_user_context(title='instrument', request=self.request)
        print(self.kwargs)
        return dict(list(context.items()) + list(additional_context.items()))

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        context['form'] = ArtistInstrumentForm(prefix='form_pre')

        self.my_context = context

        return self.render_to_response(context=self.my_context)

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        additional_context = self.get_user_context(request=self.request)
        context['form'] = PlaylistTrackForm(prefix='form_pre')
        context = dict(list(context.items()) + list(additional_context.items()))

        cursor = connections['default'].cursor()
        cursor.execute('SELECT artist_id, instrument_id FROM artist_instrument WHERE artist_id=%s AND instrument_id=%s',
                       [self.kwargs['abstr_user_id'], request.POST['form_pre-instrument']])

        if cursor.fetchone():
            context['error_messages'] = ['Current instrument already exists', ]
            print("error", context)
            return self.render_to_response(context=context)
        cursor.execute('INSERT INTO artist_instrument(artist_id, instrument_id) VALUES (%s, %s)', [self.kwargs['abstr_user_id'],
                                                                                             request.POST[
                                                                                                 'form_pre-instrument']])
        return HttpResponseRedirect(reverse('artists'))


class ArtistsAddLabelView(DataMixin, LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'streaming/create.html'
    pk_url_kwarg = 'abstr_user_id'
    model = PlaylistTrack
    success_url = reverse_lazy('artists')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        additional_context = self.get_user_context(title='label', request=self.request)
        print(self.kwargs)
        return dict(list(context.items()) + list(additional_context.items()))

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        context['form'] = ArtistLabelForm(prefix='form_pre')

        self.my_context = context

        return self.render_to_response(context=self.my_context)

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        additional_context = self.get_user_context(request=self.request)
        context['form'] = ArtistLabelForm(prefix='form_pre')
        context = dict(list(context.items()) + list(additional_context.items()))

        cursor = connections['default'].cursor()
        cursor.execute('SELECT artist_id, label_id FROM artist_label WHERE artist_id=%s AND label_id=%s',
                       [self.kwargs['abstr_user_id'], request.POST['form_pre-label']])

        if cursor.fetchone():
            context['error_messages'] = ['Current label already exists', ]
            print("error", context)
            return self.render_to_response(context=context)
        cursor.execute('INSERT INTO artist_label(artist_id, label_id) VALUES (%s, %s)',
                       [self.kwargs['abstr_user_id'],
                        request.POST[
                            'form_pre-label']])
        return HttpResponseRedirect(reverse('artists'))


class ArtistsAddGenreView(DataMixin, LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'streaming/create.html'
    pk_url_kwarg = 'abstr_user_id'
    model = PlaylistTrack
    success_url = reverse_lazy('artists')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        additional_context = self.get_user_context(title='genre', request=self.request)
        print(self.kwargs)
        return dict(list(context.items()) + list(additional_context.items()))

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        context['form'] = ArtistGenreForm(prefix='form_pre')

        self.my_context = context

        return self.render_to_response(context=self.my_context)

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        additional_context = self.get_user_context(request=self.request)
        context['form'] = ArtistGenreForm(prefix='form_pre')
        context = dict(list(context.items()) + list(additional_context.items()))

        cursor = connections['default'].cursor()
        cursor.execute('SELECT artist_id, genre_id FROM artist_genre WHERE artist_id=%s AND genre_id=%s',
                       [self.kwargs['abstr_user_id'], request.POST['form_pre-genre']])

        if cursor.fetchone():
            context['error_messages'] = ['Current genre already exists', ]
            print("error", context)
            return self.render_to_response(context=context)
        cursor.execute('INSERT INTO artist_genre(artist_id, genre_id) VALUES (%s, %s)',
                       [self.kwargs['abstr_user_id'],
                        request.POST[
                            'form_pre-genre']])
        return HttpResponseRedirect(reverse('artists'))

