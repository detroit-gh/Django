from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import SignUpForm
from .tasks import send_activation_email
from .token import account_activation_token


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            token = account_activation_token.make_token(user)
            user_id = urlsafe_base64_encode(force_bytes(user.pk))
            message = render_to_string('users/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'user_id': user_id,
                'token': token
            })
            data = {
                'to_email': form.cleaned_data['email'],
                'subject': subject,
                'message': message
            }
            send_activation_email.delay(data)
            return render(request, 'users/account_activation_sent.html')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


def activate(request, user_id, token):
    try:
        user_id = force_text(urlsafe_base64_decode(user_id))
        user = User.objects.get(pk=user_id)
    except (TypeError, ValueError, ObjectDoesNotExist):
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('/')

    return render(request, 'users/account_activation_invalid.html')
