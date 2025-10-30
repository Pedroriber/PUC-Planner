from django.shortcuts import render, redirect
from django.contrib import messages

def index(request):
    """Página inicial antiga (exemplo Django)"""
    context = {
        "title": "Django example",
    }
    return render(request, "index.html", context)

def home(request):
    """Página inicial do PUC Planner"""
    return render(request, "home.html")

def login_view(request):
    """Tela de login"""
    if request.method == "POST":
        matricula = request.POST.get("matricula")
        password = request.POST.get("password")
        # TODO: Implementar autenticação real
        messages.success(request, "Login realizado com sucesso!")
        return redirect("home")
    return render(request, "login.html")

def cadastro(request):
    """Tela de cadastro"""
    if request.method == "POST":
        nome = request.POST.get("nome")
        matricula = request.POST.get("matricula")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        # TODO: Implementar cadastro real no banco de dados
        messages.success(request, "Cadastro realizado com sucesso!")
        return redirect("login")
    return render(request, "cadastro.html")

def esqueci_senha(request):
    """Tela de recuperação de senha"""
    if request.method == "POST":
        email = request.POST.get("email")
        # TODO: Implementar envio de email de recuperação
        messages.success(request, "Link de recuperação enviado para seu e-mail!")
        return redirect("login")
    return render(request, "esqueci_senha.html")

def consulta_disciplina(request):
    """Tela de consulta de disciplinas"""
    # TODO: Buscar disciplinas do banco de dados
    return render(request, "consulta_disciplina.html")

def fluxograma(request):
    """Tela de fluxograma"""
    # TODO: Implementar lógica de fluxograma por curso
    return render(request, "fluxograma.html")

def grade_horaria(request):
    """Tela de grade horária"""
    # TODO: Implementar lógica de montagem de grade
    return render(request, "grade_horaria.html")
