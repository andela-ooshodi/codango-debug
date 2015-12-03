from django.conf.urls import url
from userprofile import views


urlpatterns = [
    url(r'^(?P<username>\w+)$',
        views.UserProfileDetailView.as_view(), name='user_profile'),
    url(r'^(?P<username>\w+)/edit$',
        views.UserProfileEditView.as_view(), name='edit_user_profile'),
    url(r'^(?P<username>\w+)/follow$',
        views.FollowUserView.as_view(), name='follow_user'),
    url(r'^(?P<username>\w+)/(?P<direction>following|followers)',
        views.FollowListView.as_view(), name='following'),
]
