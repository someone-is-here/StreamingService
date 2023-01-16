# Generated by Django 4.1.3 on 2022-12-06 10:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractUsers',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=255)),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('login', models.CharField(max_length=100, unique=True)),
                ('email', models.CharField(max_length=256, unique=True)),
                ('password', models.TextField()),
                ('is_active', models.BooleanField(default=True, null=True)),
                ('is_staff', models.BooleanField(default=False, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
            ],
            options={
                'db_table': 'abstract_users',
            },
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Albums',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('release_date', models.SmallIntegerField()),
                ('icon', models.ImageField(blank=True, null=True, upload_to='photos/%Y/%m/%d/')),
            ],
            options={
                'db_table': 'albums',
            },
        ),
        migrations.CreateModel(
            name='Countries',
            fields=[
                ('id', models.SmallAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=56, unique=True)),
                ('iso', models.CharField(max_length=2, unique=True)),
            ],
            options={
                'db_table': 'countries',
            },
        ),
        migrations.CreateModel(
            name='Genres',
            fields=[
                ('id', models.SmallAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'genres',
            },
        ),
        migrations.CreateModel(
            name='Instruments',
            fields=[
                ('id', models.SmallAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'db_table': 'instruments',
            },
        ),
        migrations.CreateModel(
            name='Labels',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150, unique=True)),
                ('website', models.CharField(blank=True, max_length=256, null=True)),
                ('foundation_year', models.SmallIntegerField()),
            ],
            options={
                'db_table': 'labels',
            },
        ),
        migrations.CreateModel(
            name='Logging',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation', models.CharField(max_length=1)),
                ('time', models.DateTimeField()),
                ('message', models.CharField(max_length=100)),
                ('abstr_user_id', models.IntegerField()),
                ('login', models.CharField(max_length=100)),
                ('role_id', models.CharField(max_length=100)),
                ('additional_info', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'db_table': 'logging',
            },
        ),
        migrations.CreateModel(
            name='Playlists',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'playlists',
            },
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.SmallAutoField(primary_key=True, serialize=False)),
                ('role', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'roles',
            },
        ),
        migrations.CreateModel(
            name='Subscriptions',
            fields=[
                ('id', models.SmallAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=150, unique=True)),
                ('cost', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'subscriptions',
            },
        ),
        migrations.CreateModel(
            name='Artists',
            fields=[
                ('id', models.OneToOneField(db_column='id', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=747, unique=True)),
                ('website', models.CharField(max_length=256, unique=True)),
                ('tour_dates', models.SmallIntegerField()),
            ],
            options={
                'db_table': 'artists',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abstr_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='streaming.subscriptions')),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Tracks',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('timing', models.TimeField()),
                ('likes', models.BigIntegerField(default=0)),
                ('streaming', models.BigIntegerField(default=0)),
                ('storage_path', models.CharField(default='', max_length=100)),
                ('track', models.FileField(upload_to='tracks/%Y/%m/%d/')),
                ('photo', models.ImageField(upload_to='tracks/%Y/%m/%d/')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='streaming.albums')),
            ],
            options={
                'db_table': 'tracks',
            },
        ),
        migrations.CreateModel(
            name='TrackGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='streaming.genres')),
                ('track', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='streaming.tracks')),
            ],
            options={
                'db_table': 'track_genre',
            },
        ),
        migrations.CreateModel(
            name='PlaylistTrack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='streaming.playlists')),
                ('track', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='streaming.tracks')),
            ],
            options={
                'db_table': 'playlist_track',
            },
        ),
        migrations.CreateModel(
            name='PlaylistAbstrUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abstr_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('playlist', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='streaming.playlists')),
            ],
            options={
                'db_table': 'playlist_abstr_user',
            },
        ),
        migrations.CreateModel(
            name='ArtistLabel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='streaming.labels')),
            ],
            options={
                'db_table': 'artist_label',
            },
        ),
        migrations.CreateModel(
            name='ArtistInstrument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instrument', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='streaming.instruments')),
            ],
            options={
                'db_table': 'artist_instrument',
            },
        ),
        migrations.CreateModel(
            name='ArtistGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='streaming.genres')),
            ],
            options={
                'db_table': 'artist_genre',
            },
        ),
        migrations.CreateModel(
            name='ArtistAlbum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='streaming.albums')),
            ],
            options={
                'db_table': 'artist_album',
            },
        ),
        migrations.AddField(
            model_name='abstractusers',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='streaming.roles'),
        ),
        migrations.AddField(
            model_name='abstractusers',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AddConstraint(
            model_name='trackgenre',
            constraint=models.UniqueConstraint(fields=('track', 'genre'), name='unique_track_genre'),
        ),
        migrations.AddConstraint(
            model_name='playlisttrack',
            constraint=models.UniqueConstraint(fields=('track', 'playlist'), name='unique_track_playlist'),
        ),
        migrations.AddConstraint(
            model_name='playlistabstruser',
            constraint=models.UniqueConstraint(fields=('playlist', 'abstr_user'), name='unique_playlist_abstr_user'),
        ),
        migrations.AddField(
            model_name='artists',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='streaming.countries'),
        ),
        migrations.AddField(
            model_name='artistlabel',
            name='artist',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='streaming.artists'),
        ),
        migrations.AddField(
            model_name='artistinstrument',
            name='artist',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='streaming.artists'),
        ),
        migrations.AddField(
            model_name='artistgenre',
            name='artist',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='streaming.artists'),
        ),
        migrations.AddField(
            model_name='artistalbum',
            name='artist',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='streaming.artists'),
        ),
        migrations.AddConstraint(
            model_name='artistlabel',
            constraint=models.UniqueConstraint(fields=('artist', 'label'), name='unique_artist_label'),
        ),
        migrations.AddConstraint(
            model_name='artistinstrument',
            constraint=models.UniqueConstraint(fields=('artist', 'instrument'), name='unique_artist_instrument'),
        ),
        migrations.AddConstraint(
            model_name='artistgenre',
            constraint=models.UniqueConstraint(fields=('artist', 'genre'), name='unique_artist_genre'),
        ),
        migrations.AddConstraint(
            model_name='artistalbum',
            constraint=models.UniqueConstraint(fields=('artist', 'album'), name='unique_artist_album'),
        ),
    ]
