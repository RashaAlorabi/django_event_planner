from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib.auth.models import User
from .forms import UserSignup, UserLogin , EventForm ,BookingForm ,ProfileForm ,ProfileUpdateForm
from .models import Event, Booking , Profile, Follow
from django.contrib import messages
from django.http import Http404, JsonResponse
from django.db.models import Q
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
import datetime
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.mail import send_mail


def home(request):
    current_date = datetime.date.today()
    events = Event.objects.filter(date__gte=current_date)[:10]
    context = {
        'events': events,
    }    
    return render(request, 'home.html',context)


def profile(request):
    user_profile = Profile.objects.get(user=request.user)  
    events = Event.objects.filter(organizer=request.user)
    
    
    context = {
        'user_profile': user_profile,
        'events':events,
        
   }
    return render(request, 'profile.html', context)

def update_profile(request,profile_id):
    user_profile =Profile.objects.get(id=profile_id)
    # user_siginup =User.objects.get(id=profile_id)
    siginup_form = ProfileUpdateForm(instance=user_profile)
    profile_form = ProfileForm(instance=user_profile)
    if request.method == "POST":
        siginup_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)
        profile_form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if siginup_form.is_valid() and profile_form.is_valid():
            siginup_form.save()
            profile_form.save()
            return redirect('profile')
    context = {
        'siginup_form': siginup_form,
        "profile_form": profile_form,
        'user_profile': user_profile,
        # 'user_siginup':user_siginup,
        }
    return render(request, 'update_profile.html', context)


# def following(request, profile_id):
#     if request.user.is_anonymous:
#         return redirect('signin')

#     Profile_followers = Profile.followers.all()
#     user_profile = Profile.objects.get(id=profile_id)
#     print(Profile_followers)



#     if user_profile in Profile_followers:
#         Profile_followers.remove(user_profile)
#     else:
#        Profile_followers.add(user_profile)
#        Profile_followers.save()
#     response = {
#         # "followed": followed,
        
#     }
#     return JsonResponse(response)

def follow(request, user_id):
    follow_obj = User.objects.get(id=user_id)

    if request.user.is_anonymous:
        return redirent('login')
    
    follow, created = Follow.objects.get_or_create(follower=request.user, following=follow_obj)
    if created:
        follow_btn = True
    else:

        follow_btn = False
        follow_obj.delete()
    response = {
        "follow_btn": follow_btn,
    }
    return JsonResponse(response, safe=False)


class Signup(View):
    form_class = UserSignup
    profile_form_class = ProfileForm
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        profile_form = self.profile_form_class()
        return render(request, self.template_name, {'form': form, 'profile_form': profile_form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        profile_form = self.profile_form_class(request.POST,request.FILES)
        if form.is_valid() and profile_form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user=user
            profile.save()
            messages.success(request, "You have successfully signed up.")
            login(request, user)
            return redirect("event-list")
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
                if request.user.organizer.all().exists():
                    return redirect('dashboard')
                else :
                    return redirect('event-list')

                messages.success(request, "Welcome Back! %s") %(request.username)
                
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
    #events = request.user.organizer.all()
    current_date = datetime.date.today()
    # events_1 = Event.objects.filter(date__lte=current_date)
    events = Event.objects.filter(organizer=request.user)
    # events = request.user.organizer.filter(date__lte=current_date)
    #booking_objs = Booking.objects.filter(guest=request.user)
    booking_objs = request.user.booked.all()

    context = {
        'booking_objs': booking_objs,
        'current_date': current_date,
        'events': events
    }

    return render(request, 'dashboard.html', context)



def event_org(request):
    if request.user.is_anonymous:
        return redirect('login')
    events = Event.objects.filter(organizer=request.user)

    context = {
        'events': events
    }

    return render(request, 'events_I_org.html', context)


def event_list(request):
    current_date = datetime.date.today()
    events = Event.objects.filter(date__gte=current_date)
    query = request.GET.get('search')
    user_id = request.user.id
    if query:
        events = events.filter(
                Q(title__icontains=query)|
                Q(description__icontains=query)|
                Q(organizer__username__icontains=query)
            ).distinct()
    user_profile = Profile.objects.get(user=request.user)  
    follow_list = []
    if request.user.is_authenticated:
        follow_list = user_profile.user.followers.all().values_list('follower', flat=True)
      
    context = {
        'events': events,
        'current_date':current_date,
        'follow_list':follow_list,
        'user_id' : user_id,
    }
    return render(request, 'event_list.html', context)


def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)    
    left_ticket = event.get_left_seats()
    guest_list =  event.booked.all()
    
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
                send_mail(
                    'Congratulations',
                    'Congratulations your booking is confirm',
                    'event5345345@gmail.com',
                    [request.user.email+'@gmail.com'],
                    fail_silently=False,
                )
                return redirect('event-detail',event_id)
        messages.warning(request, "The number of seats you are trying to book is greater than the avalible seate")        
        return redirect('event-detail',event_id) 
               
    context = {
        "form":form,
        'event':event,
    }
    return render(request, 'book_event.html', context)