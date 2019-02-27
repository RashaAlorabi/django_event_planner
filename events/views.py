from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserSignup, UserLogin , EventForm ,BookingForm
from .models import Event, Booking
from django.contrib import messages
from django.http import Http404, JsonResponse
from django.db.models import Q
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
import datetime
from django.core.mail import EmailMessage
def home(request):
    events = Event.objects.all()
    context = {
        'events': events,
    }    
    return render(request, 'home.html',context)

class Signup(View):
    form_class = UserSignup
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, "You have successfully signed up.")
            login(request, user)
            return redirect("home")
        messages.warning(request, form.errors)
        return redirect("signup")

class Login(View):
    form_class = UserLogin
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, "Welcome Back!")
                return redirect('dashboard')
            messages.warning(request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")

def dashboard(request):
    if request.user.is_anonymous:
        return redirect('event-list')
    #events = Event.objects.filter(organizer=request.user)
    #events = request.user.events.all()
    current_date = datetime.date.today()
    events_1 = Event.objects.filter(date__lte=current_date)
    events = events_1.filter(organizer=request.user)

    booking_objs = Booking.objects.filter(guest=request.user)
    context = {
        'booking_objs': booking_objs,
        'current_date': current_date,
        'events': events
    }

    return render(request, 'dashboard.html', context)


def event_list(request):
    current_date = datetime.date.today()
    events = Event.objects.filter(date__gte=current_date)
    query = request.GET.get('search')
    if query:
        events = events.filter(
                Q(title__icontains=query)|
                Q(description__icontains=query)|
                Q(organizer__username__icontains=query)
            ).distinct()
    context = {
        'events': events,
        'current_date':current_date,
    }
    return render(request, 'event_list.html', context)


def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)    
    left_ticket = event.get_left_seats()
    guest_list =  event.booked.all()

    print(guest_list)
    context = {
        'event': event,
        'left_ticket' : left_ticket,
        'guest_list': guest_list,
   }
    return render(request, 'event_detail.html', context)

def add_event(request):
    if request.user.is_anonymous:
        return redirect('event-list')
    events = Event.objects.all()
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect(event)
    context = {
        'form': form,
    }
    return render(request, 'add_event.html', context)

def event_update(request, event_id):
    event = Event.objects.get(id=event_id)

    form = EventForm(instance=event)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect(event)
    context = {
        'form': form,
        "event": event,
    }
    return render(request, 'event_update.html', context)

def event_delete(request, event_id):
    if request.user.is_anonymous:
        return redirect('dashboard')

    if not request.user.is_staff:
        raise Http404
    
    Event.objects.get(id=event_id).delete()
    return redirect('dashboard')

def book_event(request, event_id):
    if request.user.is_anonymous:
        return redirect('login')
    event = Event.objects.get(id=event_id)    
    form = BookingForm()
    if request.method == "POST":
        left_ticket = event.get_left_seats()
        if int(request.POST['seats']) <= left_ticket:
            form = BookingForm(request.POST)
            if form.is_valid():
                book = form.save(commit=False)
                book.guest = request.user
                book.event = event
                book.save()
                messages.success(request, "Congratulations your booking is confirm")
                # email = EmailMessage('Subject', 'Body', to=['def@domain.com'])
                # email.send()
                return redirect('event-detail',event_id)
        messages.warning(request, "The number of seats you are trying to book is greater than the avalible seate")        
        return redirect('event-detail',event_id) 
               
    context = {
        "form":form,
        'event':event,
    }
    return render(request, 'book_event.html', context)