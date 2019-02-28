from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django_countries.fields import CountryField

class Event(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organizer')
    date = models.DateField()
    time = models.TimeField()
    location = models.TextField()  
    capacity = models.IntegerField()
    poster = models.ImageField(upload_to='event_posters')

    class Meta:
        ordering = ['date','time','title',]

    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'event_id': self.id})

    def update_url(self):
        return reverse('update-event', kwargs={'event_id': self.id})

    def delete_url(self):
        return reverse('delete-event', kwargs={'event_id': self.id})

    def get_left_seats(self):
        return self.capacity - sum(self.booked.all().values_list('seats', flat=True))


class Booking(models.Model):
    guest = models.ForeignKey(User, on_delete=models.CASCADE,related_name='booked')
    event = models.ForeignKey(Event,on_delete=models.CASCADE,related_name='booked')
    seats = models.IntegerField()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    phone = models.CharField(max_length=12,blank=True,)
    birth_date = models.DateField(null=True, blank=True)
    country = CountryField()
    picture =models.ImageField(upload_to='user_profile_img',null=True, blank=True)
    # following = models.ManyToManyField(User, related_name='followers')

    def __unicode__(self):
        return self.user.username

    def update_url(self):
        return reverse('update-profile', kwargs={'profile_id': self.id})
        
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
