from django.shortcuts import render

# Create your views here.


def signupview(request):
    return render(request, 'signup.html', {'somedata':100})
