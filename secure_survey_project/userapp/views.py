from django.shortcuts import render, redirect
from .models import User
from .forms import UserForm


def user_create_view(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'userapp/user_form.html', {'form': form})


def user_list_view(request):
    users = User.objects.all()
    return render(request, 'userapp/user_list.html', {'users': users})
