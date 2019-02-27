from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Event(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
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

    # def __str__(self):
    #     return "%s booked %s"%(self.user.username, self.event.Title)



