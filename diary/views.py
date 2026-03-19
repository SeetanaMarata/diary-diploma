from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from rest_framework import permissions, viewsets

from .models import DiaryEntry
from .serializers import DiaryEntrySerializer


# API ViewSet
class DiaryEntryViewSet(viewsets.ModelViewSet):
    serializer_class = DiaryEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DiaryEntry.objects.filter(author=self.request.user)


# Главная страница
def index(request):
    return render(request, "diary/index.html")


# Страница с записями (только для авторизованных)
@login_required
def dashboard(request):
    # Удаление записи
    if request.method == "POST" and "delete_id" in request.POST:
        entry_id = request.POST["delete_id"]
        try:
            entry = DiaryEntry.objects.get(id=entry_id, author=request.user)
            entry.delete()
        except DiaryEntry.DoesNotExist:
            pass
        return redirect("dashboard")

    # Редактирование записи
    if request.method == "POST" and "edit_id" in request.POST:
        entry_id = request.POST["edit_id"]
        try:
            entry = DiaryEntry.objects.get(id=entry_id, author=request.user)
            entry.title = request.POST["title"]
            entry.content = request.POST["content"]
            entry.mood = request.POST.get("mood", "😐")
            entry.save()
        except DiaryEntry.DoesNotExist:
            pass
        return redirect("dashboard")

    # Создание новой записи
    if request.method == "POST" and "title" in request.POST:
        DiaryEntry.objects.create(
            author=request.user,
            title=request.POST["title"],
            content=request.POST["content"],
            mood=request.POST.get("mood", "😐"),
        )
        return redirect("dashboard")

    entries = DiaryEntry.objects.filter(author=request.user)
    return render(request, "diary/dashboard.html", {"entries": entries})


# Вход
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(
                request, "diary/login.html", {"error": "Неверное имя или пароль"}
            )

    return render(request, "diary/login.html")


# Выход
def logout_view(request):
    logout(request)
    return redirect("index")


# Регистрация
def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST.get("email", "")
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            return render(
                request, "diary/register.html", {"error": "Пароли не совпадают"}
            )

        if User.objects.filter(username=username).exists():
            return render(
                request, "diary/register.html", {"error": "Пользователь уже существует"}
            )

        user = User.objects.create_user(
            username=username, email=email, password=password1
        )
        login(request, user)
        return redirect("dashboard")

    return render(request, "diary/register.html")
