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
        
        # Validações básicas
        if not matricula or not password:
            messages.error(request, "Matrícula e senha são obrigatórios!")
            return render(request, "login.html")
        
        # TODO: Implementar autenticação real
        # Por enquanto, apenas simula sucesso
        messages.success(request, "Login simulado com sucesso! (Autenticação será implementada)")
        return redirect("home")
    return render(request, "login.html")

def cadastro(request):
    """Tela de cadastro"""
    if request.method == "POST":
        nome = request.POST.get("nome")
        matricula = request.POST.get("matricula")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        confirmar_senha = request.POST.get("confirmar_senha")
        
        # Validações
        if not all([nome, matricula, email, senha, confirmar_senha]):
            messages.error(request, "Todos os campos são obrigatórios!")
            return render(request, "cadastro.html")
        
        if senha != confirmar_senha:
            messages.error(request, "As senhas não coincidem!")
            return render(request, "cadastro.html")
        
        if len(senha) < 6:
            messages.error(request, "A senha deve ter no mínimo 6 caracteres!")
            return render(request, "cadastro.html")
        
        # TODO: Verificar se matrícula ou email já existem
        # TODO: Implementar cadastro real no banco de dados
        messages.success(request, "Cadastro realizado com sucesso! Faça login para continuar.")
        return redirect("login")
    return render(request, "cadastro.html")

def esqueci_senha(request):
    """Tela de recuperação de senha"""
    if request.method == "POST":
        email = request.POST.get("email")
        
        if not email:
            messages.error(request, "Por favor, insira um e-mail válido!")
            return render(request, "esqueci_senha.html")
        
        # TODO: Verificar se o email existe no banco de dados
        # TODO: Implementar envio de email de recuperação
        messages.success(request, "Se o e-mail estiver cadastrado, você receberá um link de recuperação!")
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
