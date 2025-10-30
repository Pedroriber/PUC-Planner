from django.conf import settings
from django.db import models


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


class SemesterPlan(models.Model):
	"""Plano simples que agrupa disciplinas para um usuário."""
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='semester_plans')
	name = models.CharField("nome", max_length=100, blank=True)
	courses = models.ManyToManyField(Course, blank=True, related_name='plans')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = "Plano Semestral"
		verbose_name_plural = "Planos Semestrais"

	def __str__(self):
		return self.name or f"Plano de {self.user}"


class Task(models.Model):
	"""Tarefa mínima: título, prazo e completo."""
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	due_date = models.DateTimeField(blank=True, null=True)
	completed = models.BooleanField(default=False)
	related_course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')

	class Meta:
		verbose_name = "Tarefa"
		verbose_name_plural = "Tarefas"
		ordering = ["completed", "due_date"]

	def __str__(self):
		return self.title


