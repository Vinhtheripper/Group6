from django.shortcuts import render


def aboutus(request):
    return render(request, 'app/aboutus.html')

def blog(request):
    return render(request, 'app/blog.html')

def wishlist(request):
    return render(request, 'app/wishlist.html')


def policy(request):
    return render(request, 'app/policy.html')

def contact(request):
    return render(request, 'app/contact.html')


def index(request):
    return render(request, 'app/index.html')