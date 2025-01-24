from django.shortcuts import render

from Logins.models import Logins


# Create your views here.
def create_login(request):
    if request.method == "POST":
        login = request.POST.get("login")
        password = request.POST.get("password")
        login_instance, created = Logins.objects.get_or_create(login=login, password=password)
        login_instance.save()
