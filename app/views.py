from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.

from app.models import Question, Answer, Tag, Profile, LikeQuestion, LikeAnswer, BestTags, BestUsers, QuestionManager


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
    questions = Question.objects.new_questions()
    return render(request, "index.html", {"content": paginate(questions, request), 'best': best})


def question(request, number):
    question = Question.objects.get(pk=number)
    answers = Answer.objects.get_question(question)
    return render(request, "question.html", {"content": paginate(answers, request), 'question': question, 'best': best})


def hot(request):
    questions = Question.objects.hot_question()
    return render(request, "hot.html", {"content": paginate(questions, request), 'best': best})


def tag(request, name):
    questions = Question.objects.tags_question(name)
    return render(request, "tag.html", {"content": paginate(questions, request), "name": name, 'best': best})


def setting(request):
    return render(request, "setting.html", {'best': best})


def login(request):
    return render(request, "login.html", {'best': best})


def registration(request):
    return render(request, "registration.html", {'best': best})


def ask(request):
    return render(request, "ask.html", {})


def error(request):
    return render(request, "404.html", {})
