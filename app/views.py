from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.


questions = [
    {
        "number": i,
        "title": f"Что такое TI?",
        "text": f"The International 2021 - заключительный турнир Dota Pro Circuit и десятый ежегодный турнир The International, который возвращается в Европу впервые с 2011 года. Формат приглашения аналогичен формату, используемому для предыдущего International..."
    } for i in range(30)
]


def paginate(questions, request):
    per_page = request.GET.get('limit', 3)
    paginator = Paginator(questions, per_page)
    page = request.GET.get('page')
    content = paginator.get_page(page)
    return content


def index(request):
    return render(request, "index.html", {"questions": paginate(questions, request)})


def question(request, number):
    return render(request, "question.html", {'number': questions[number]})


def hot(request):
    return render(request, "hot.html", {"questions": paginate(questions, request)})


def tag(request):
    return render(request, "tag.html", {"questions": paginate(questions, request)})


def setting(request):
    return render(request, "setting.html", {})


def login(request):
    return render(request, "login.html", {})


def registration(request):
    return render(request, "registration.html", {})


def ask(request):
    return render(request, "ask.html", {})
