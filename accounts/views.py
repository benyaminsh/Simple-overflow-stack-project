from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserRegisterionForm, LoginForm, EditUserForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .models import Relation


class RegisterView(View):
    form_class = UserRegisterionForm
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(
                username=cd['username'],
                email=cd['email'],
                password=cd['password']
            )
            messages.success(request, 'User Register Successfully', 'success')
            return redirect('home:home')

        else:
            return render(request, self.template_name, {'form': form})


class LoginView(View):
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get("next", None)
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'Login Successfully', 'success')
                if self.next:
                    return redirect(self.next)
                else:
                    return redirect('home:home')

            else:
                messages.error(request, 'username or password is wrong', 'warning')

        return render(request, self.template_name, {'form': form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Logout Successfully', 'success')
        return redirect('home:home')


class ProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'

    def get(self, request, user_id):
        is_following = False
        user = get_object_or_404(User, id=user_id)
        posts = user.post_set.all()
        relation = Relation.objects.filter(from_user=request.user, to_user_id=user_id)
        if relation.exists():
            is_following = True

        context = {
            'user': user,
            'posts': posts,
            'is_following': is_following,
        }
        return render(request, self.template_name, context)


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy('accounts:password_reset_complete')


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"


class FollowView(LoginRequiredMixin, View):

    def get(self, request, user_id):
        if request.user != user_id:
            user = User.objects.get(id=user_id)
            relation = Relation.objects.filter(from_user=request.user, to_user=user)
            if relation.exists():
                messages.error(request, "you are already following this user", "danger")

            else:
                Relation.objects.create(from_user=request.user, to_user=user)
                messages.success(request, "you followed this user", "success")

        else:
            messages.error(request, "you cannot follow yourself", "danger")

        return redirect('accounts:user_profile', user_id)


class UnfollowView(LoginRequiredMixin, View):

    def get(self, request, user_id):
        if request.user != user_id:
            user = User.objects.get(id=user_id)
            relation = Relation.objects.filter(from_user=request.user, to_user=user)
            if relation.exists():
                relation.delete()
                messages.success(request, "you unfollowed this user", "success")

            else:
                messages.error(request, "you do not follow the user", "danger")

        else:
            messages.error(request, "you cannot unfollow yourself", "danger")

        return redirect('accounts:user_profile', user_id)


class EditUserView(LoginRequiredMixin, View):
    form_class = EditUserForm
    template_name = 'accounts/edit_user.html'

    def get(self, request):
        form = self.form_class(instance=request.user.profile, initial={'email': request.user.email})
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user.profile, initial={'email': request.user.email})
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, "profile edited successfully", "success")
            return redirect('accounts:user_profile', request.user.id)
