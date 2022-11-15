import time, random
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
#from prometheus_client import Histogram


#h = Histogram('login_to_dashboard_histogram_latency', 'Latency (histogram) to /dashboard in seconds')


def index(request):
    return render(request, 'core/index.html')


def register(request):
  if request.method == 'POST':
    # Get form values
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']

    # Check if passwords match
    if password == password2:
      # Check username
      if User.objects.filter(username=username).exists():
        messages.error(request, 'That username is taken')
        return redirect('core:register')
      else:
        if User.objects.filter(email=email).exists():
          messages.error(request, 'That email is being used')
          return redirect('core:register')
        else:
          # Looks good
          user = User.objects.create_user(username=username, password=password,email=email, first_name=first_name, last_name=last_name)
          user.save()
          messages.success(request, 'You are now registered and can log in')
          return redirect('core:login')
    else:
      messages.error(request, 'Passwords do not match')
      return redirect('core:register')
  else:
    return render(request, 'core/register.html')


def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)

    if user is not None:
      auth.login(request, user)
      ## login_start_time ##
      #request.session['login_start_time'] = time.time()
      return redirect('core:dashboard')
    else:
      messages.error(request, 'Invalid credentials')
      return redirect('core:login')
  elif request.user.is_authenticated:
      return redirect('core:dashboard')
  else:
      return render(request, 'core/login.html')


def logout(request):
  if request.method == 'POST':
    auth.logout(request)
    return redirect('core:index')


def dashboard(request):
    ## Add delay ##
    # time.sleep(3)
    ## total_time ##
    #total_time = time.time() - request.session.get('login_start_time')
    ## Instrument ##
    #h.observe(total_time)      
    return render(request, 'core/dashboard.html') 