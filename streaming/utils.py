from django.db import connections
from django.contrib.auth.models import AnonymousUser


menu_items = [
    {'title': 'Playlists', 'url_name': 'playlists'},
    {'title': 'Artists', 'url_name': 'artists'},
    {'title': 'Albums', 'url_name': 'albums'},
    {'title': 'Tracks', 'url_name': 'tracks'},
]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu_items
        if str(context['request'].user) != 'AnonymousUser' and context['request'].user.role.id == 3:
            cursor = connections['default'].cursor()
            cursor.execute('SELECT * FROM users WHERE abstr_user_id=%s', [self.request.user.id])
            context['auth_user'] = cursor.fetchone()[0]
            print(context['auth_user'])

        return context
