from flask_admin.contrib.sqla import ModelView
from flask import session, redirect, url_for, request

class AdminView(ModelView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_folder = 'static'

    def is_accessible(self):
        return session.get('user') == 'Administrator'

    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('home', next=request.url))

class TopicView(AdminView):
    def __init__(self, *args, **kwargs):
        super(TopicView, self).__init__(*args, **kwargs)

    column_list = ('title', 'date_created', 'date_modified', 'total_vote_count','status')
    column_searchable_list = ('title',) 
    column_default_sort = ('date_created', True)
    column_filters = ('status',)
    column_sortable_list = ('total_vote_count',)    