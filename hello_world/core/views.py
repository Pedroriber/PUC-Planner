from django.shortcuts import render, redirect, get_object_or_404
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

from appPUC_Planner.models import Course
from appPUC_Planner.forms import CourseForm

User = get_user_model()


def index(request):
    context = {
        "title": "Django example",
    }
    return render(request, "index.html", context)


@login_required
def home(request):
    return render(request, "home.html")

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        matricula = request.POST.get("matricula", "").strip()
        password = request.POST.get("password", "")
        
        if not matricula or not password:
            messages.error(request, "Matrícula e senha são obrigatórios!")
            return render(request, "login.html")
        
        user = authenticate(request, username=matricula, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Bem-vindo(a), {user.nome_completo}!")
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, "Matrícula ou senha incorretos!")
            return render(request, "login.html")
    
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "Você saiu da sua conta com sucesso!")
    return redirect("login")

def cadastro(request):
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
        
        if not email.endswith('@puc-rio.br') and not email.endswith('@aluno.puc-rio.br'):
            messages.warning(request, "Aviso: Recomendamos usar seu e-mail institucional PUC.")
        
        try:
            user = User.objects.create_user(
                matricula=matricula,
                email=email,
                password=senha,
                nome_completo=nome
            )
            
            messages.success(request, "Cadastro realizado com sucesso! Faça login para continuar.")
            return redirect("login")
            
        except IntegrityError as e:
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
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        
        if not email:
            messages.error(request, "Por favor, insira um e-mail válido!")
            return render(request, "esqueci_senha.html")
        
        try:
            user = User.objects.get(email=email)
            
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            reset_link = request.build_absolute_uri(
                f'/redefinir-senha/{uid}/{token}/'
            )
            
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
            
            send_mail(
                subject,
                message,
                'noreply@pucplanner.com',
                [user.email],
                fail_silently=False,
            )
            
            messages.success(request, "Email de recuperação enviado! Verifique sua caixa de entrada.")
            
        except User.DoesNotExist:
            messages.success(request, "Se o e-mail estiver cadastrado, você receberá instruções de recuperação!")
        except Exception as e:
            messages.error(request, f"Erro ao enviar email: {str(e)}")
        
        return redirect("login")
    
    return render(request, "esqueci_senha.html")


def redefinir_senha(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
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
    return render(request, "consulta_disciplina.html")


@login_required
def fluxograma(request):
    return render(request, "fluxograma.html")


@login_required
def fluxograma1(request):
    return render(request, "fluxograma1.html")


@login_required
def fluxograma2(request):
    return render(request, "fluxograma2.html")


@login_required
def fluxograma3(request):
    return render(request, "fluxograma3.html")


@login_required
def grade_horaria(request):
    return render(request, "grade_horaria.html")


# ============ CRUD de Disciplinas ============

@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, "courses/course_list.html", {"courses": courses})


@login_required
def course_create(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Disciplina criada com sucesso!")
            return redirect("course_list")
    else:
        form = CourseForm()
    
    return render(request, "courses/course_form.html", {"form": form})


@login_required
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Disciplina atualizada com sucesso!")
            return redirect("course_list")
    else:
        form = CourseForm(instance=course)
    
    return render(request, "courses/course_form.html", {"form": form, "course": course})


@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    
    if request.method == "POST":
        course.delete()
        messages.success(request, "Disciplina deletada com sucesso!")
        return redirect("course_list")
    
    return render(request, "courses/course_confirm_delete.html", {"course": course})
