from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserSignup, UserLogin , EventForm ,BookingForm
from .models import Event, Booking
from django.contrib import messages
from django.http import Http404, JsonResponse
from django.db.models import Q

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
                return redirect('home')
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
    events = Event.objects.all()
    context = {
        'events': events,
    }
    return render(request, 'dashboard.html', context)


def user_dashboard(request):
    events = Event.objects.all()
    context = {
        'events': events,
    }
    return render(request, 'user_dashboard.html', context)


def event_list(request):
    events = Event.objects.all()
    query = request.GET.get('search')
    if query:
        events = events.filter(
                Q(Title__icontains=query)|
                Q(Description__icontains=query)|
                Q(Organizer__username__icontains=query)
            ).distinct()
    context = {
        'events': events,
    }
    return render(request, 'event_list.html', context)


def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    ticket_count = event.booked.all().values_list('seats', flat=True).count()
    
    left_ticket = event.get_left_seats(ticket_count)
    
    context = {
        'event': event,
        'left_ticket' : left_ticket,
   }
    return render(request, 'event_detail.html', context)


def add_event(request):
    if request.user.is_anonymous:
        return redirect('event-list')
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.Organizer = request.user
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
        form = BookingForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.guest = request.user
            book.event = event
            book.save()
            return redirect('event-detail',event_id)
    context = {
        "form":form,
        'event':event,
    }
    return render(request, 'book_event.html', context)