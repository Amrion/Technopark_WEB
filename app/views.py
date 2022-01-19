from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.

from django.contrib.auth.models import User
from app.models import Question, Answer, Tag, Profile, LikeQuestion, LikeAnswer, BestTags, BestUsers, QuestionManager
from app.forms import LoginForm, RegistrationForm, QuestionForm, SettingsForm, AnswerForm
from django.urls import reverse
from django.views.decorators.http import require_POST

best = {
    "tags": BestTags.best_tags()[:10],
    "users": BestUsers.best_users()[:10]
}


def paginate(content, request):
    per_page = request.GET.get('limit', 3)
    paginator = Paginator(content, per_page)
    page = request.GET.get('page')
    contents = paginator.get_page(page)
    return contents


def index(request):
    profile = Profile.objects.get(user_id=request.user.id)
    questions = Question.objects.new_questions()
    return render(request, "index.html", {"content": paginate(questions, request), 'best': best, 'profile': profile})


def question(request, number):
    profile = Profile.objects.get(user_id=request.user.id)
    quest = Question.objects.get(pk=number)
    answers = Answer.objects.get_question(quest)

    if request.user.is_authenticated:
        author = Profile.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            form = AnswerForm(data=request.GET, profile=author, question=quest)
        if request.method == 'POST':
            form = AnswerForm(data=request.POST, profile=author, question=quest)
            if form.is_valid():
                form.save()
                return redirect(reverse('question', kwargs={'number': quest.id}))
    else:
        form = LoginForm()
    return render(request, "question.html",
                  {"content": paginate(answers, request), 'question': quest, 'best': best, 'form': form,
                   'profile': profile})


def hot(request):
    profile = Profile.objects.get(user_id=request.user.id)
    questions = Question.objects.hot_question()
    return render(request, "hot.html", {"content": paginate(questions, request), 'best': best, 'profile': profile})


def tag(request, name):
    profile = Profile.objects.get(user_id=request.user.id)
    questions = Question.objects.tags_question(name)
    return render(request, "tag.html",
                  {"content": paginate(questions, request), "name": name, 'best': best, 'profile': profile})


def setting(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            form = SettingsForm()
        if request.method == 'POST':
            form = SettingsForm(data=request.POST, instance=request.user, files=request.FILES)
            print(form)
            if form.is_valid():
                form.save()
                return redirect(reverse('setting'))
            else:
                form.add_error(None, 'Такой пользователь уже существует')
    else:
        return redirect(reverse('home'))
    return render(request, "setting.html", {'best': best, 'profile': profile, 'form': form})


def login(request):
    if request.method == 'GET':
        form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if not user:
                form.add_error(None, "Не верный логин или пароль!")
            else:
                auth.login(request, user)
                return redirect(reverse('home'))
    return render(request, "login.html", {'best': best, 'form': form})


def registration(request):
    if request.method == 'GET':
        form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            user = auth.authenticate(request, username=form.cleaned_data['username'],
                                     password=form.cleaned_data['password1'])
            auth.login(request, user)
            return redirect(reverse('home'))
        else:
            form.clean()
            form.add_error(None, 'Проверьтe!')
            form.add_error(None, 'Пароль должен содержать минимум 8 символов!')
            form.add_error(None, 'Пароль не должен содержать данные, которые будут схожи с вашими личными данными!')
            form.add_error(None, 'Пароль не должен состоять только из чисел!')
            form.add_error(None, 'Пароль должны совпадать!')

    return render(request, "registration.html", {'best': best, 'form': form})


@login_required
def ask(request):
    profile = Profile.objects.get(user_id=request.user.id)
    author = Profile.objects.get(user_id=request.user.id)
    if request.method == 'GET':
        form = QuestionForm(data=request.GET, profile=author)
    if request.method == 'POST':
        form = QuestionForm(data=request.POST, profile=author)
        if form.is_valid():
            q = form.save()
            return redirect(reverse('question', kwargs={'number': q.id}))
    return render(request, "ask.html", {'best': best, 'form': form, 'profile': profile})


def error(request):
    return render(request, "404.html", {})


def logout(request):
    auth.logout(request)
    return redirect(request.META.get('HTTP_REFERER'))


@require_POST
@login_required
def vote(request):
    data = request.POST

    profile = Profile.objects.get(user_id=request.user.id)

    if data['action'] == 'like':
        check = True
    else:
        check = False

    if 'question' == data['class']:
        try:
            like_id = LikeQuestion.objects.get(user_id=profile.id, question_id=data['id'])
        except LikeQuestion.DoesNotExist:
            rate = LikeQuestion.objects.create(user_id=profile.id, check=check,
                                               question_id=data['id'])
            rate.save()

            if check:
                Question.objects.filter(id=data['id']).update(like=F('like') + 1)
            else:
                Question.objects.filter(id=data['id']).update(dislike=F('dislike') + 1)
        like = Question.objects.get(id=data['id']).like
        dislike = Question.objects.get(id=data['id']).dislike
    if 'answer' == data['class']:
        try:
            like_id = LikeAnswer.objects.get(user_id=profile.id, answer_id=data['id'])
        except LikeAnswer.DoesNotExist:
            rate = LikeAnswer.objects.create(user_id=profile.id, check=check,
                                             answer_id=data['id'])
            rate.save()

            if check:
                Answer.objects.filter(id=data['id']).update(like_counter=F('like_counter') + 1)
            else:
                Answer.objects.filter(id=data['id']).update(dislike_counter=F('dislike_counter') + 1)
        like = Answer.objects.get(id=data['id']).like_counter
        dislike = Answer.objects.get(id=data['id']).dislike_counter

    return JsonResponse({'like': like, 'dislike': dislike})


@require_POST
@login_required
def correct(request):
    data = request.POST

    answer = Answer.objects.get(id=data['id'])

    if data['checked']:
        answer.checked = True
        answer.save()
    if not data['checked']:

        answer.checked = False
        answer.save()

    checked = Answer.objects.get(id=data['id']).checked

    return JsonResponse({'checked': checked})
