from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser,
    Course,
    CourseRelation,
    Schedule,
    ScheduleItem,
	Period
)

# ============================================================
# CUSTOM USER ADMIN (igual ao seu – não alterei nada)
# ============================================================

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


# ============================================================
# COURSE ADMIN (idêntico ao seu – só deixei organizado)
# ============================================================

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Admin para disciplinas."""
    list_display = ['code', 'name', 'credits', 'degree', 'flow_row', 'flow_col_percent']
    search_fields = ['code', 'name']
    list_filter = ['degree']
    ordering = ['code']


# ============================================================
# COURSE RELATION (pré/co requisitos)
# ============================================================

@admin.register(CourseRelation)
class CourseRelationAdmin(admin.ModelAdmin):
    list_display = ['source', 'relation_type', 'target']
    list_filter = ['relation_type']
    search_fields = ['source__code', 'target__code']


# ============================================================
# SCHEDULE (grade horária)
# ============================================================

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'year', 'semester', 'created_at']
    list_filter = ['semester', 'year']
    search_fields = ['user__matricula', 'name']


# ============================================================
# SCHEDULE ITEM (blocos da grade)
# ============================================================

@admin.register(ScheduleItem)
class ScheduleItemAdmin(admin.ModelAdmin):
    list_display = ['schedule', 'course', 'day', 'start_hour', 'duration_hours']
    list_filter = ['day']
    search_fields = ['schedule__user__matricula', 'course__code']

@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ["order", "name", "flow_row", "flow_col_percent"]
    ordering = ["order"]