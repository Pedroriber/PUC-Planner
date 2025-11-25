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
	"""Disciplina mínima: código, nome e créditos."""
	code = models.CharField("código", max_length=20, unique=True)
	name = models.CharField("nome", max_length=200)
	credits = models.PositiveSmallIntegerField("créditos", default=0)

	class Meta:
		verbose_name = "Disciplina"
		verbose_name_plural = "Disciplinas"
		ordering = ["code"]

	def __str__(self):
		return f"{self.code} - {self.name}"


