from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
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
    """Tela de recuperação de senha - Envia email com link"""
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        
        print(f"[DEBUG] Email recebido: '{email}'")
        
        if not email:
            messages.error(request, "Por favor, insira um e-mail válido!")
            return render(request, "esqueci_senha.html")
        
        try:
            user = User.objects.get(email=email)
            print(f"[DEBUG] Usuário encontrado: {user.nome_completo} ({user.email})")
            
            # Gera token de recuperação
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            print(f"[DEBUG] Token gerado: {token}")
            print(f"[DEBUG] UID: {uid}")
            
            # Cria o link de recuperação
            reset_link = request.build_absolute_uri(
                f'/redefinir-senha/{uid}/{token}/'
            )
            
            print(f"[DEBUG] Link de recuperação: {reset_link}")
            
            # Prepara o email
            subject = 'Recuperação de Senha - PUC Planner'
            message = f"""
Olá {user.nome_completo},

Você solicitou a recuperação de senha para sua conta no PUC Planner.

Clique no link abaixo para redefinir sua senha:
{reset_link}

Este link é válido por 24 horas.

Se você não solicitou esta recuperação, ignore este email.

Atenciosamente,
Equipe PUC Planner
            """
            
            print(f"[DEBUG] Tentando enviar email para: {user.email}")
            
            # Envia o email
            send_mail(
                subject,
                message,
                'noreply@pucplanner.com',
                [user.email],
                fail_silently=False,
            )
            
            print(f"[DEBUG] Email enviado com sucesso!")
            
            messages.success(request, "Email de recuperação enviado! Verifique sua caixa de entrada (ou o console do terminal).")
            
        except User.DoesNotExist:
            print(f"[DEBUG] Usuário com email '{email}' não encontrado")
            # Não revela se o email existe ou não por segurança
            messages.success(request, "Se o e-mail estiver cadastrado, você receberá instruções de recuperação!")
        except Exception as e:
            print(f"[DEBUG] ERRO ao enviar email: {e}")
            import traceback
            traceback.print_exc()
            messages.error(request, f"Erro ao enviar email: {str(e)}")
        
        return redirect("login")
    
    return render(request, "esqueci_senha.html")


def redefinir_senha(request, uidb64, token):
    """Página para redefinir a senha usando o token do email"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    # Valida o token
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            nova_senha = request.POST.get("nova_senha", "")
            confirmar_senha = request.POST.get("confirmar_senha", "")
            
            if not nova_senha or not confirmar_senha:
                messages.error(request, "Todos os campos são obrigatórios!")
                return render(request, "redefinir_senha.html", {"validlink": True})
            
            if nova_senha != confirmar_senha:
                messages.error(request, "As senhas não coincidem!")
                return render(request, "redefinir_senha.html", {"validlink": True})
            
            if len(nova_senha) < 6:
                messages.error(request, "A senha deve ter no mínimo 6 caracteres!")
                return render(request, "redefinir_senha.html", {"validlink": True})
            
            # Altera a senha
            user.set_password(nova_senha)
            user.save()
            
            messages.success(request, "Senha redefinida com sucesso! Faça login com sua nova senha.")
            return redirect("login")
        
        return render(request, "redefinir_senha.html", {"validlink": True})
    else:
        messages.error(request, "Link de recuperação inválido ou expirado!")
        return render(request, "redefinir_senha.html", {"validlink": False})


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
