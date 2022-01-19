from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from app.models import Profile

from app.models import Question, Tag, Answer, LikeQuestion

from django.db.models import F


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class RegistrationForm(UserCreationForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'avatar']

    def save(self, commit=False):
        user = super(RegistrationForm, self).save()
        Profile.objects.create(user_id=user.id)

        if self.files.get('avatar'):
            profile = Profile.objects.get(user_id=user.id)
            profile.avatar = self.files.get('avatar')
            profile.save()

        return user

    def clean_username(self):
        cleaned_data = super().clean()
        if User.objects.filter(username=cleaned_data.get('username')).exists():
            self.add_error('username', "Такой пользователь уже существует")
        else:
            return cleaned_data


class QuestionForm(forms.ModelForm):
    tags = forms.CharField(required=True)

    class Meta:
        model = Question
        fields = ['title', 'text']

    def __init__(self, data, profile):
        self.profile = profile
        super(QuestionForm, self).__init__(data)

    def save(self, commit=False):
        question = super(QuestionForm, self).save(commit=False)
        question.author = self.profile
        question.like = 0
        question.dislike = 0

        question.save()
        for tag in self.cleaned_data['tags'].split(' '):
            try:
                tag_id = Tag.objects.get(name=tag).id
            except Tag.DoesNotExist:
                tag_id = Tag.objects.create(name=tag).id
            question.tags.add(tag_id)
        return question


class SettingsForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'avatar']

    def save(self, commit=False):
        user = super(SettingsForm, self).save(commit=True)

        if self.files.get('avatar'):
            profile = Profile.objects.get(user_id=user.id)
            profile.avatar = self.files.get('avatar')
            profile.save()

        return user


class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ['text']

    def __init__(self, data, profile, question):
        self.profile = profile
        self.question = question
        super(AnswerForm, self).__init__(data)

    def save(self, commit=False):
        answer = super(AnswerForm, self).save(False)
        answer.question = self.question
        answer.author = self.profile
        answer.checked = False
        answer.dislike_counter = 0
        answer.like_counter = 0
        answer.save()
        return answer
