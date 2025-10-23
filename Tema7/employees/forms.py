from django import forms
from django.contrib.auth.models import User
from .models import EmployeeProfile, EmployeeSkill, Skill

class EmployeeProfileCreateForm(forms.ModelForm):
    username = forms.CharField(label="Логин пользователя")
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput, required=False)

    class Meta:
        model = EmployeeProfile
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Для уже существующего объекта подставляем user-данные в поля формы
        if self.instance.pk and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
            self.fields['password'].help_text = "Чтобы изменить пароль, введите новый. Если не менять — оставьте пустым."
            self.fields['password'].required = False
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['first_name'].initial = self.instance.user.first_name

    def clean_username(self):
        username = self.cleaned_data['username']
        qs = User.objects.exclude(pk=(self.instance.user.pk if self.instance.pk and self.instance.user else None))
        if qs.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует.')
        return username

    def save(self, commit=True):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        last_name = self.cleaned_data.get('last_name')
        first_name = self.cleaned_data.get('first_name')

        if self.instance.pk and self.instance.user:
            # --- ОБНОВЛЕНИЕ ---
            user = self.instance.user
            user.username = username
            user.email = email
            user.last_name = last_name
            user.first_name = first_name
            if password:  # Меняем пароль только если введён новый
                user.set_password(password)
            if commit:
                user.save()
        else:
            # --- СОЗДАНИЕ ---
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

        instance = super().save(commit=False)
        instance.user = user
        if commit:
            instance.save()
        return instance

class EmployeeSkillForm(forms.ModelForm):
    class Meta:
        model = EmployeeSkill
        fields = ['skill', 'level']

EmployeeSkillFormSet = forms.inlineformset_factory(
    EmployeeProfile,
    EmployeeSkill,
    form=EmployeeSkillForm,
    extra=5,
    can_delete=True
)

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name']