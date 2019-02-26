from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Hall(models.Model):
    seats = models.IntegerField()

    def __str__(self):
        return self.title

class Event(models.Model):
    Title = models.CharField(max_length=50)
    Description = models.TextField()
    Organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    Date = models.DateField()
    Time = models.TimeField()
    Location = models.TextField()  
    Seats = models.IntegerField()
    Poster = models.ImageField(upload_to='event_posters')

    class Meta:
        ordering = ['Date','Time','Title',]

    def __str__(self):
        return self.Title
        
    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'event_id': self.id})

    def update_url(self):
        return reverse('update-event', kwargs={'event_id': self.id})

    def delete_url(self):
        return reverse('delete-event', kwargs={'event_id': self.id})
    def get_left_seats(self, ticket_count):
        return self.Seats - ticket_count 

class Booking(models.Model):
    guest = models.ForeignKey(User, on_delete=models.CASCADE,related_name='booked')
    event = models.ForeignKey(Event, on_delete=models.CASCADE,related_name='booked')
    seats = models.ForeignKey(Hall, on_delete=models.CASCADE,related_name='booked')

    def __str__(self):
        return "%s booked %s"%(self.user.username, self.event.Title)



