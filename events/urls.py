from django.urls import path
from events import views


urlpatterns = [
path('', views.home, name='home'),




    path('signup/', views.Signup.as_view(), name='signup'),

    path('profile/', views.profile, name='profile'),
    path('profile/<int:profile_id>/update/', views.update_profile, name='update-profile'),


    #path('follow/<int:user_id>/', views.follow, name='follow'),

    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('events/', views.event_list, name='event-list'),
    path('event_org/', views.event_org, name='event-org'),
    path('event/<int:event_id>/', views.event_detail, name='event-detail'),

    path('event/create', views.add_event, name='add-event'),
    path('<int:event_id>/update/', views.event_update, name='update-event'),
    path('<int:event_id>/delete/', views.event_delete, name='delete-event'),

    path('<int:event_id>/booking/', views.book_event, name='book-event'),

]