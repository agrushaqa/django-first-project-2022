from django.contrib.auth import authenticate, login
from django.views.generic.base import TemplateView
from .forms import (AvatarForm, SettingsForm, SignUpForm)
from django.shortcuts import render
from common.library import storage_file
from user.models import Avatar
from django.http.response import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import ListView


# Create your views here.
class SignupListView(TemplateView):
    template_name = "user/registration.html"
    default_user_logo = "profile-icon-empty.png"

    def post(self, request, *args, **kwargs):
        user_form = SignUpForm(request.POST)
        avatar_form = AvatarForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            user.save()
            if avatar_form.is_valid() and 'image' in request.FILES:
                storage_file(request.FILES['image'])
                new_image = Avatar(image=str(request.FILES['image']),
                                   user=user)
                new_image.save()
            else:
                new_image = Avatar(image=self.default_user_logo, user=user)
                new_image.save()
            raw_password = user_form.cleaned_data.get('password1')

            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
        if avatar_form.is_valid():
            return HttpResponseRedirect('/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SignUpForm()
        context['avatar_form'] = AvatarForm()
        return context


class SettingsView(LoginRequiredMixin, SingleObjectMixin, ListView):
    login_url = '/login'
    redirect_field_name = 'settings'

    def get(self, request):
        if "searchField" in request.GET and request.GET['searchField']:
            return HttpResponseRedirect("/query")
        else:
            try:
                avatar = Avatar.objects.get(user_id=request.user)
                if request.FILES:
                    storage_file(request.FILES['image'])
                    avatar.image = str(request.FILES['image'])
                    avatar.save()
            except Exception:
                pass
            user_form = SettingsForm(data=request.POST or None,
                                     instance=request.user)
            if user_form.is_valid():
                user = user_form.save()
                user.refresh_from_db()
                user.save()

            avatar_form = AvatarForm(request)

            return render(request, "user/settings.html",
                          {"user_form": user_form, 'avatar_form': avatar_form,
                           "avatar": avatar})
