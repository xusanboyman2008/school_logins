from django.shortcuts import render

from School.Logins.models import Logins



# Create your views here.
def all(request):
    logins = Logins.objects.all()
    return render(request, '', {'logins': logins,'page':'home'})


def create_login(request):
    if request.method == "POST":
        login = request.POST.get("login")
        password = request.POST.get("password")
        login_1 = Logins.objects.get(login=login)
        if login_1:
            return render(request, "Logins/login.html", {"login": login_1.login,'page':'create'})
        login_instance = Logins.objects.create(login=login, password=password)
        login_instance.save()

def delete_login(request,pk):
    if request.method == "PUT":
        login_instance = Logins.objects.get(id=pk)
        login_instance.login = request.POST.get("login", login_instance.login)
        login_instance.password = request.POST.get("password", login_instance.password)
        login_instance.save()
        return render(request, "Logins/login.html", {"login": login_instance.login,'page':'update'})

    if request.method == "DELETE":
        login_instance = Logins.objects.get(id=pk)
        login_instance.delete()
        return render(request, "Logins/login.html", {"login": login_instance.login,'page':'delete'})
