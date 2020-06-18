"""defines urls pattern for learning_logs"""

from django.conf.urls import url
from . import views

urlpatterns = [
    # home page
    url(r'^$', views.index, name='index'),
    url(r'^topics/$', views.topics, name='topics'),
    # Details for single topic
    url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),
    # page for adding a new topic
    url(r'^new_topic/$', views.new_topic, name='new_topic'),
    # page ofr adding new entry
    url(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry'),
    url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry'),
    url(r'^delete_topic/(?P<topic_id>\d+)/$', views.delete_topic, name='delete_topic'),
    url(r'^delete_entry/(?P<entry_id>\d+)/$', views.delete_entry, name='delete_entry'),

]
