from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator


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


class Curso(models.Model):
	"""Representa um curso/graduação ao qual disciplinas podem pertencer."""
	nome = models.CharField("nome", max_length=200, unique=True)
	periodos = models.PositiveSmallIntegerField(
		"número de períodos",
		default=8,
		help_text="Quantidade total de períodos/semestres do curso.",
	)

	class Meta:
		verbose_name = "Curso"
		verbose_name_plural = "Cursos"
		ordering = ["nome"]

	def __str__(self):
		return self.nome


class Course(models.Model):
	"""Disciplina mínima: código, nome e créditos."""
	code = models.CharField("código", max_length=20, unique=True)
	name = models.CharField("nome", max_length=200)
	# Cursos/graduações aos quais esta disciplina pertence
	cursos = models.ManyToManyField(
		Curso,
		through="CursoDisciplina",
		related_name="disciplinas",
		blank=True,
		help_text="Selecione todos os cursos que incluem esta disciplina."
	)
	# Pré-requisitos: lista de códigos separados por vírgula (ex: 'MAT 4162, ENG 4010')
	prerequisites = models.CharField("pré-requisitos", max_length=500, blank=True,
									 help_text="Códigos separados por vírgula, ex: 'MAT 4162, ENG 4010'")
	credits = models.PositiveSmallIntegerField("créditos", default=0)
	syllabus_url = models.URLField(
		"link da ementa",
		blank=True,
		help_text="URL para a ementa oficial da disciplina.",
	)

	class Meta:
		verbose_name = "Disciplina"
		verbose_name_plural = "Disciplinas"
		ordering = ["code"]

	def __str__(self):
		return f"{self.code} - {self.name}"


class CursoDisciplina(models.Model):
	curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="relacoes")
	disciplina = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="relacoes")
	periodo = models.PositiveSmallIntegerField(
		"período",
		null=True,
		blank=True,
		help_text="Período em que a disciplina é ofertada neste curso."
	)
	posicao = models.PositiveSmallIntegerField(
		"posição na linha",
		null=True,
		blank=True,
		validators=[MinValueValidator(1), MaxValueValidator(8)],
		help_text="Coluna em que a disciplina deve aparecer no período (1 = primeira coluna)."
	)

	class Meta:
		verbose_name = "Disciplina de Curso"
		verbose_name_plural = "Disciplinas por Curso"
		unique_together = ("curso", "disciplina")
		ordering = ["curso__nome", "periodo", "posicao", "disciplina__code"]

	def __str__(self):
		parts = []
		if self.periodo:
			parts.append(f"período {self.periodo}")
		if self.posicao:
			parts.append(f"pos {self.posicao}")
		info = f" ({', '.join(parts)})" if parts else ""
		return f"{self.disciplina.code} em {self.curso.nome}{info}"


