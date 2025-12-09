from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Curso, Course, CursoDisciplina


MAX_COLUMNS = 8


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
	"""Admin customizado para o modelo de usuário."""
	model = CustomUser
	list_display = ['matricula', 'nome_completo', 'email', 'curso', 'periodo', 'is_active', 'data_criacao']
	list_filter = ['is_active', 'is_staff', 'curso', 'periodo']
	search_fields = ['matricula', 'nome_completo', 'email']
	ordering = ['-data_criacao']
	
	fieldsets = (
		('Informações de Login', {'fields': ('matricula', 'password')}),
		('Informações Pessoais', {'fields': ('nome_completo', 'email', 'curso', 'periodo')}),
		('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
		('Datas Importantes', {'fields': ('last_login', 'data_criacao', 'data_atualizacao')}),
	)
	
	add_fieldsets = (
		('Criar Novo Usuário', {
			'classes': ('wide',),
			'fields': ('matricula', 'email', 'nome_completo', 'password1', 'password2', 'curso', 'periodo'),
		}),
	)
	
	readonly_fields = ['data_criacao', 'data_atualizacao', 'last_login']


class CursoDisciplinaInlineForCourse(admin.TabularInline):
	model = CursoDisciplina
	fk_name = 'disciplina'
	extra = 1
	autocomplete_fields = ['curso']
	fields = ['curso', 'periodo', 'posicao']

	def formfield_for_dbfield(self, db_field, request, **kwargs):
		field = super().formfield_for_dbfield(db_field, request, **kwargs)
		if db_field.name == 'posicao' and field is not None:
			field.widget.attrs.update({'min': 1, 'max': MAX_COLUMNS, 'placeholder': '1 a 8'})
		return field


class CursoDisciplinaInlineForCurso(admin.TabularInline):
	model = CursoDisciplina
	fk_name = 'curso'
	extra = 1
	autocomplete_fields = ['disciplina']
	fields = ['disciplina', 'periodo', 'posicao']

	def formfield_for_dbfield(self, db_field, request, **kwargs):
		field = super().formfield_for_dbfield(db_field, request, **kwargs)
		if db_field.name == 'posicao' and field is not None:
			field.widget.attrs.update({'min': 1, 'max': MAX_COLUMNS, 'placeholder': '1 a 8'})
		return field


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
	"""Admin para disciplinas."""
	list_display = ['code', 'name', 'credits', 'lista_cursos']
	search_fields = ['code', 'name', 'relacoes__curso__nome']
	list_filter = ['credits', 'relacoes__periodo', 'relacoes__posicao', 'relacoes__curso']
	fieldsets = (
		(None, {'fields': ('code', 'name', 'credits', 'syllabus_url')}),
		('Fluxograma e Pré/co-requisitos', {'fields': ('prerequisites', 'corequisites')}),
	)
	inlines = [CursoDisciplinaInlineForCourse]

	def lista_cursos(self, obj):
		relacoes = obj.relacoes.select_related('curso').all()
		if not relacoes:
			return "-"
		rotulos = []
		for rel in relacoes:
			info_parts = []
			if rel.periodo:
				info_parts.append(f"P{rel.periodo}")
			if rel.posicao:
				info_parts.append(f"Pos {rel.posicao}")
			info = f" ({', '.join(info_parts)})" if info_parts else ""
			rotulos.append(f"{rel.curso.nome}{info}")
		return ", ".join(rotulos)

	lista_cursos.short_description = 'Cursos'


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
	list_display = ['nome', 'periodos']
	search_fields = ['nome']
	inlines = [CursoDisciplinaInlineForCurso]


