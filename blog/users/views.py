
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from main.models import  Plant
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username or not email or not password1 or not password2:
            messages.error(request, "Пожалуйста, заполните все поля")
        elif password1 != password2:
            messages.error(request, "Пароли не совпадают")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Пользователь с таким именем уже существует")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Пользователь с таким email уже существует")
        else:
            try:
                validate_password(password1)
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request, error)
                return render(request, 'users/register.html')  # не продолжаем

            # Всё ок — создаем пользователя
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            messages.success(request, "Регистрация успешна! Войдите в систему.")
            return redirect('login')

    return render(request, 'users/register.html')




login_required()
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')  # чтобы избежать повторной отправки формы
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)





class ProfileView(DetailView):
    model = Profile
    context_object_name = 'author'
    template_name = 'users/profile_author.html'
    slug_url_kwarg='slug'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object
        # Получаем все книги этого автора
        posts = Plant.objects.filter(author=profile)

        # Пагинация: по 6 книг на страницу
        paginator = Paginator(posts, 3)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj  # для шаблона
        return context

    
class ProfileViewAbout(DetailView):
    model = Profile
    template_name = 'users/author_about.html'
    context_object_name = 'author'
    slug_url_kwarg = 'slug'



class MyLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = CustomLoginForm
