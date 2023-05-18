from django.shortcuts import render, redirect
from .models import PersonalEmail
from .forms import PersonalInfoForm
from .user import PersonalInfo, User
from django.conf import settings


def register_user(request):
    if request.method == 'POST':
        form = PersonalInfoForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')

            # Create PersonalInfo instance and save email
            PersonalEmail.objects.create(email=email)

            # create PersonalInfo instance
            personal_info = PersonalInfo()
            personal_info.set_personal_info(
                form.cleaned_data.get('gender'),
                form.cleaned_data.get('age'),
                form.cleaned_data.get('marriage'),
                form.cleaned_data.get('income'),
                form.cleaned_data.get('education'),
                form.cleaned_data.get('job'),
                form.cleaned_data.get('phone'),
                form.cleaned_data.get('phone_maker')
            )

            # create User instance with PersonalInfo instance
            user = User(personal_info)

            # Encrypt personal information
            user_id = PersonalEmail.objects.latest('id').id
            network = settings.NETWORK_INSTANCE
            user.encrypt_personal_info(user_id, network)

            return redirect('userapp:success_url')
        else:
            return render(request, 'userapp/user_form.html', {'form': form})

    else:
        form = PersonalInfoForm()
        return render(request, 'userapp/user_form.html', {'form': form})


def success(request):
    return render(request, 'userapp/success.html')
