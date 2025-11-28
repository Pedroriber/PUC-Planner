from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
	
	def create_user(self, matricula, email, password=None, **extra_fields):
		if not matricula:
			raise ValueError('A matrícula é obrigatória')
		if not email:
			raise ValueError('O email é obrigatório')
		
		email = self.normalize_email(email)
		user = self.model(matricula=matricula, email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user
	
	def create_superuser(self, matricula, email, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('is_active', True)
		
		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser deve ter is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser deve ter is_superuser=True.')
		
		return self.create_user(matricula, email, password, **extra_fields)


class CustomUser(AbstractUser):
	username = None
	matricula = models.CharField('Matrícula', max_length=20, unique=True)
	email = models.EmailField('Email', unique=True)
	nome_completo = models.CharField('Nome Completo', max_length=200)
	curso = models.CharField('Curso', max_length=100, blank=True)
	periodo = models.PositiveSmallIntegerField('Período', null=True, blank=True)
	data_criacao = models.DateTimeField(auto_now_add=True)
	data_atualizacao = models.DateTimeField(auto_now=True)
	
	USERNAME_FIELD = 'matricula'
	REQUIRED_FIELDS = ['email', 'nome_completo']
	
	objects = CustomUserManager()
	
	class Meta:
		verbose_name = 'Usuário'
		verbose_name_plural = 'Usuários'
		ordering = ['-data_criacao']
	
	def __str__(self):
		return f"{self.matricula} - {self.nome_completo}"
	
	def get_full_name(self):
		return self.nome_completo
	
	def get_short_name(self):
		return self.first_name or self.nome_completo.split()[0]


# Versão simplificada dos modelos para PUC-Planner

class Course(models.Model):
    """Disciplina do PUC Planner."""
    code = models.CharField("código", max_length=20, unique=True)
    name = models.CharField("nome", max_length=200)
    credits = models.PositiveSmallIntegerField("créditos", default=0)

    # NOVOS CAMPOS (todos opcionais)
    degree = models.CharField(
        "curso / habilitação",
        max_length=100,
        blank=True,
        help_text="Ex.: Engenharia de Computação, Engenharia de Produção..."
    )
    syllabus_url = models.URLField(
        "URL da ementa",
        max_length=300,
        blank=True
    )

    # posição no fluxograma (praquelas <div style='top: X; left: Y%'>)
    flow_row = models.IntegerField(
        "linha do fluxograma",
        null=True,
        blank=True,
        help_text="Coordenada vertical (px) do bloco no fluxograma"
    )
    flow_col_percent = models.IntegerField(
        "coluna do fluxograma (%)",
        null=True,
        blank=True,
        help_text="Posição horizontal em porcentagem (2, 34, 50, 75, ...)"
    )

    class Meta:
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.name}"

class CourseRelation(models.Model):
    """Relação entre disciplinas: pré-requisito ou co-requisito."""
    TYPE_CHOICES = [
        ("PRE", "Pré-requisito"),
        ("CO", "Co-requisito"),
    ]

    source = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="relations_from",
        help_text="Disciplina que é o pré/co-requisito."
    )
    target = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="relations_to",
        help_text="Disciplina que depende da outra."
    )
    relation_type = models.CharField(
        "tipo",
        max_length=3,
        choices=TYPE_CHOICES,
        default="PRE"
    )

    class Meta:
        verbose_name = "Relação de disciplina"
        verbose_name_plural = "Relações de disciplinas"

    def __str__(self):
        seta = "→" if self.relation_type == "PRE" else "↔"
        return f"{self.get_relation_type_display()}: {self.source.code} {seta} {self.target.code}"
class Schedule(models.Model):
    """Grade horária de um usuário (um semestre, por exemplo)."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="schedules"
    )
    name = models.CharField(
        "nome da grade",
        max_length=100,
        default="Minha grade"
    )
    year = models.PositiveIntegerField("ano", null=True, blank=True)
    semester = models.PositiveSmallIntegerField(
        "semestre",
        null=True,
        blank=True,
        choices=[(1, "1º"), (2, "2º")]
    )
    created_at = models.DateTimeField("criada em", auto_now_add=True)

    class Meta:
        verbose_name = "Grade horária"
        verbose_name_plural = "Grades horárias"
        ordering = ["-year", "-semester", "-created_at"]

    def __str__(self):
        if self.year and self.semester:
            return f"{self.user} - {self.year}.{self.semester} ({self.name})"
        return f"{self.user} - {self.name}"


class ScheduleItem(models.Model):
    """Cada bloquinho de disciplina arrastado para a grade."""
    DAYS = [
        (1, "Segunda"),
        (2, "Terça"),
        (3, "Quarta"),
        (4, "Quinta"),
        (5, "Sexta"),
    ]

    schedule = models.ForeignKey(
        Schedule,
        on_delete=models.CASCADE,
        related_name="items"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="schedule_items"
    )

    day = models.PositiveSmallIntegerField("dia da semana", choices=DAYS)
    start_hour = models.PositiveSmallIntegerField("hora de início")  # 7, 8, 9...
    duration_hours = models.PositiveSmallIntegerField(
        "duração (horas)",
        default=2
    )

    class Meta:
        verbose_name = "Bloco na grade"
        verbose_name_plural = "Blocos na grade"
        unique_together = ("schedule", "day", "start_hour", "course")

    def __str__(self):
        return f"{self.course.code} - {self.get_day_display()} às {self.start_hour}h"
class Period(models.Model):
    """Rótulo de período no fluxograma (1º, 2º, 3º...)."""

    name = models.CharField(
        "nome do período",
        max_length=50,
        help_text="Ex.: 1º período, 2º período..."
    )

    order = models.PositiveSmallIntegerField(
        "ordem",
        help_text="Ordem do período (1, 2, 3...)."
    )

    flow_row = models.IntegerField(
        "linha do fluxograma",
        null=True,
        blank=True,
        help_text="Coordenada vertical (px) onde o rótulo aparecerá"
    )

    flow_col_percent = models.IntegerField(
        "coluna do fluxograma (%)",
        default=0,
        help_text="Posição horizontal em porcentagem (0 = bem à esquerda)"
    )

    class Meta:
        verbose_name = "Período"
        verbose_name_plural = "Períodos"
        ordering = ["order"]

    def __str__(self):
        return f"{self.order}º - {self.name}"