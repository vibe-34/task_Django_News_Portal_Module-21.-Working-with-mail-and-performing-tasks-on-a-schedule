from django import forms
from django.contrib.auth.forms import UserCreationForm  # базовая форма (реализованы все валидации и проверки)
from django.contrib.auth.models import User

from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class SignUpForm(UserCreationForm):
    # Расширяем базовую форму, добавляем значимые поля (которые есть в модели User)
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class CustomSignupForm(SignupForm):
    """
    Добавляет нового пользователя в группу common, при успешном заполнении
    формы регистрации.
    """
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)  # вызываем это же метод у родителя
        common_group = Group.objects.get(name='common')      # получаем объект модели группы common
        common_group.user_set.add(user)                     # возвращаем пользователей группы и добавляем нового
        return user                                        # возвращаем объект модели User
