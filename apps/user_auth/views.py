from django.shortcuts import render

def hello(request):
    return render(request, 'user_auth/index.html')
