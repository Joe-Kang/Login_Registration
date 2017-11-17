from django.shortcuts import render, redirect
from .models import User

from django.contrib.messages import error
# Create your views here.
def index(request):
    try:
        request.session['user']
    except:
        request.session['user'] = ""

    if request.session['user']:
        return render(request, 'lr_app/success.html')
        
    return render(request, 'lr_app/index.html')

def success(request):
    if not request.session['user']:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user'])
    }
    return render(request, 'lr_app/success.html', context)

def register(request):
    errors = User.objects.validate_registration(request.POST)
    if type(errors) == list:
        for err in errors:
            error(request, err)
        return redirect('/')
    request.session['user'] = User.objects.get(email=request.POST['email']).id
    return redirect('/success')

def login(request):
    errors = User.objects.validate_login(request.POST)
    if type(errors) == list:
        for err in errors:
            error(request, err)
        return redirect('/')
    request.session['user'] = User.objects.get(email=request.POST['email']).id
    return redirect('/success')

def logout(request):
    del request.session['user']
    return redirect('/')
