from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import Group


class Roles(models.Model):
    id = models.SmallAutoField(primary_key=True)
    role = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.role

    class Meta:
        db_table = 'roles'


class AbstractUsersManager(BaseUserManager):
    def create_user(self, role, username, login, email, password, is_admin=False, is_staff=False,
                    is_active=True):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not username:
            raise ValueError("User must have a full name")

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        # user.username = username
        user.set_password(password)  # change password to hash
        print("here", role)
        user.role = Roles.objects.get(pk=role)
        user.login = login
        user.is_admin = is_admin
        user.is_staff = is_staff
        user.is_active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, role, username, login, email, password, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not username:
            raise ValueError("User must have a full name")

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        print("here13", role)
        # user.username = username
        user.set_password(password)  # change password to hash
        user.role = Roles.objects.get(pk=role)
        user.login = login
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class AbstractUsers(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    role = models.ForeignKey('Roles', models.DO_NOTHING)
    username = models.CharField(unique=True, max_length=255)
    login = models.CharField(unique=True, max_length=100)
    email = models.CharField(unique=True, max_length=256)
    password = models.TextField()

    is_active = models.BooleanField(default=True, null=True)
    is_staff = models.BooleanField(default=False, null=True)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['login', 'role', 'email']

    object = AbstractUsersManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app ?"
        return True

    def __str__(self):
        return self.login

    class Meta:
        db_table = 'abstract_users'


class Albums(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150)
    release_date = models.SmallIntegerField()
    icon = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True, blank=True)

    class Meta:
        db_table = 'albums'

    def __str__(self):
        return self.name


class ArtistAlbum(models.Model):
    artist = models.OneToOneField('Artists', models.DO_NOTHING)
    album = models.ForeignKey(Albums, models.DO_NOTHING)

    class Meta:
        db_table = 'artist_album'
        constraints = [
            models.UniqueConstraint(
                fields=['artist', 'album'], name='unique_artist_album'
            )
        ]


class ArtistGenre(models.Model):
    artist = models.OneToOneField('Artists', models.DO_NOTHING)
    genre = models.ForeignKey('Genres', models.DO_NOTHING)

    class Meta:
        db_table = 'artist_genre'
        constraints = [
            models.UniqueConstraint(
                fields=['artist', 'genre'], name='unique_artist_genre'
            )
        ]


class ArtistInstrument(models.Model):
    artist = models.OneToOneField('Artists', models.DO_NOTHING)
    instrument = models.ForeignKey('Instruments', models.DO_NOTHING)

    class Meta:
        db_table = 'artist_instrument'
        constraints = [
            models.UniqueConstraint(
                fields=['artist', 'instrument'], name='unique_artist_instrument'
            )
        ]


class ArtistLabel(models.Model):
    artist = models.OneToOneField('Artists', models.DO_NOTHING)
    label = models.ForeignKey('Labels', models.DO_NOTHING)

    class Meta:
        db_table = 'artist_label'
        constraints = [
            models.UniqueConstraint(
                fields=['artist', 'label'], name='unique_artist_label'
            )
        ]


class Artists(models.Model):
    id = models.OneToOneField(AbstractUsers, models.DO_NOTHING, db_column='id', primary_key=True)
    name = models.CharField(unique=True, max_length=747)
    country = models.ForeignKey('Countries', models.DO_NOTHING)
    website = models.CharField(unique=True, max_length=256)
    tour_dates = models.SmallIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'artists'


class Countries(models.Model):
    id = models.SmallAutoField(primary_key=True)
    title = models.CharField(unique=True, max_length=56)
    iso = models.CharField(unique=True, max_length=2)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'countries'


class Genres(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'genres'


class Instruments(models.Model):
    id = models.SmallAutoField(primary_key=True)
    title = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'instruments'


class Labels(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=150)
    website = models.CharField(max_length=256, blank=True, null=True)
    foundation_year = models.SmallIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'labels'


class Logging(models.Model):
    operation = models.CharField(max_length=1)
    time = models.DateTimeField()
    message = models.CharField(max_length=100)
    abstr_user_id = models.IntegerField()
    login = models.CharField(max_length=100)
    role_id = models.CharField(max_length=100)
    additional_info = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'logging'


class PlaylistAbstrUser(models.Model):
    playlist = models.OneToOneField('Playlists', models.DO_NOTHING)
    abstr_user = models.ForeignKey(AbstractUsers, models.DO_NOTHING)

    class Meta:
        db_table = 'playlist_abstr_user'
        constraints = [
            models.UniqueConstraint(
                fields=['playlist', 'abstr_user'], name='unique_playlist_abstr_user'
            )
        ]


class PlaylistTrack(models.Model):
    track = models.OneToOneField('Tracks', models.DO_NOTHING)
    playlist = models.ForeignKey('Playlists', models.DO_NOTHING)

    class Meta:
        db_table = 'playlist_track'
        constraints = [
            models.UniqueConstraint(
                fields=['track', 'playlist'], name='unique_track_playlist'
            )
        ]


class Playlists(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'playlists'


class Subscriptions(models.Model):
    id = models.SmallAutoField(primary_key=True)
    title = models.CharField(unique=True, max_length=150)
    cost = models.TextField(blank=True, null=True)  # This field type is a guess.

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'subscriptions'


class TrackGenre(models.Model):
    track = models.OneToOneField('Tracks', models.DO_NOTHING)
    genre = models.ForeignKey(Genres, models.DO_NOTHING)

    class Meta:
        db_table = 'track_genre'
        constraints = [
            models.UniqueConstraint(
                fields=['track', 'genre'], name='unique_track_genre'
            )
        ]


class Tracks(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150)
    timing = models.TimeField()
    likes = models.BigIntegerField(default=0)
    streaming = models.BigIntegerField(default=0)
    storage_path = models.CharField(max_length=100, default='')
    track = models.FileField(upload_to='tracks/%Y/%m/%d/')
    photo = models.ImageField(upload_to='tracks/%Y/%m/%d/')
    album = models.ForeignKey(Albums, models.DO_NOTHING)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tracks'


class Users(models.Model):
    abstr_user = models.ForeignKey(AbstractUsers, models.DO_NOTHING)
    subscription = models.ForeignKey(Subscriptions, models.DO_NOTHING)

    class Meta:
        db_table = 'users'
