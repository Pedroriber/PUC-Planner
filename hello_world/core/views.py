from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

User = get_user_model()


def index(request):
    """Página inicial antiga (exemplo Django)"""
    context = {
        "title": "Django example",
    }
    return render(request, "index.html", context)


@login_required
def home(request):
    """Página inicial do PUC Planner - Requer autenticação"""
    return render(request, "home.html")

def login_view(request):
    """Tela de login"""
    # Se o usuário já está autenticado, redireciona para home
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        matricula = request.POST.get("matricula", "").strip()
        password = request.POST.get("password", "")
        
        # Validações básicas
        if not matricula or not password:
            messages.error(request, "Matrícula e senha são obrigatórios!")
            return render(request, "login.html")
        
        # Tenta autenticar o usuário
        user = authenticate(request, username=matricula, password=password)
        
        if user is not None:
            # Usuário autenticado com sucesso
            login(request, user)
            messages.success(request, f"Bem-vindo(a), {user.nome_completo}!")
            
            # Redireciona para a página solicitada ou para home
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            # Credenciais inválidas
            messages.error(request, "Matrícula ou senha incorretos!")
            return render(request, "login.html")
    
    return render(request, "login.html")


def logout_view(request):
    """Logout do usuário"""
    logout(request)
    messages.success(request, "Você saiu da sua conta com sucesso!")
    return redirect("login")

def cadastro(request):
    """Tela de cadastro"""
    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        matricula = request.POST.get("matricula", "").strip()
        email = request.POST.get("email", "").strip()
        senha = request.POST.get("senha", "")
        confirmar_senha = request.POST.get("confirmar_senha", "")
        
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
        
        # Validação de email institucional (opcional)
        if not email.endswith('@puc-rio.br') and not email.endswith('@aluno.puc-rio.br'):
            messages.warning(request, "Aviso: Recomendamos usar seu e-mail institucional PUC.")
        
        try:
            # Cria o usuário
            user = User.objects.create_user(
                matricula=matricula,
                email=email,
                password=senha,
                nome_completo=nome
            )
            
            messages.success(request, "Cadastro realizado com sucesso! Faça login para continuar.")
            return redirect("login")
            
        except IntegrityError as e:
            # Verifica qual campo causou o erro de duplicação
            if 'matricula' in str(e).lower():
                messages.error(request, "Esta matrícula já está cadastrada!")
            elif 'email' in str(e).lower():
                messages.error(request, "Este e-mail já está cadastrado!")
            else:
                messages.error(request, "Erro ao criar cadastro. Tente novamente.")
            return render(request, "cadastro.html")
        
        except Exception as e:
            messages.error(request, f"Erro ao criar cadastro: {str(e)}")
            return render(request, "cadastro.html")
    
    return render(request, "cadastro.html")

def esqueci_senha(request):
    """Tela de recuperação de senha - versão simplificada"""
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        
        if not email:
            messages.error(request, "Por favor, insira um e-mail válido!")
            return render(request, "esqueci_senha.html")
        
        # Verifica se o email existe
        try:
            user = User.objects.get(email=email)
            # TODO: Implementar envio de email com link de recuperação
            # Por enquanto, apenas informa sucesso
            messages.success(request, "Se o e-mail estiver cadastrado, você receberá instruções de recuperação!")
        except User.DoesNotExist:
            # Não revela se o email existe ou não por segurança
            messages.success(request, "Se o e-mail estiver cadastrado, você receberá instruções de recuperação!")
        
        return redirect("login")
    
    return render(request, "esqueci_senha.html")


@login_required
def consulta_disciplina(request):
    """Tela de consulta de disciplinas"""
    # TODO: Buscar disciplinas do banco de dados
    return render(request, "consulta_disciplina.html")


@login_required
def fluxograma(request):
    """Tela de fluxograma"""
    # TODO: Implementar lógica de fluxograma por curso
    return render(request, "fluxograma.html")


@login_required
def grade_horaria(request):
    """Tela de grade horária"""
    # TODO: Implementar lógica de montagem de grade
    return render(request, "grade_horaria.html")
