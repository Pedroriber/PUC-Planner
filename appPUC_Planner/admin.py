from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Course


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


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
	"""Admin para disciplinas."""
	list_display = ['code', 'name', 'credits']
	search_fields = ['code', 'name']
	list_filter = ['credits']

