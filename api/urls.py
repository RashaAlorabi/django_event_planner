from django.urls import path
from .views import (
    UpcomingEventList,
    # OrganizerEventList,
    EventCreate,
    EventUpdate,
    EventDelete)
from events import views 

urlpatterns = [
	#path('', views.home, name='home'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),

 
    path('upcoming/api/', UpcomingEventList.as_view(), name='upcoming-api-list'),
    # path('organizer/api/', OrganizerEventList.as_view(), name='organizer-api-detail'),
    path('api/add/', EventCreate.as_view(), name='api-create'),
    path('api/<int:event_id>/update/', EventUpdate.as_view(), name='api-update'),
    path('api/<int:event_id>/delete/', EventDelete.as_view(), name='api-delete'),

]