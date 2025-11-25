from django import forms
from .models import Course, Task


class CourseForm(forms.ModelForm):
    """Formulário para cadastrar/editar disciplinas."""
    
    class Meta:
        model = Course
        fields = ['code', 'name', 'credits']
        labels = {
            'code': 'Código',
            'name': 'Nome',
            'credits': 'Créditos',
        }


class TaskForm(forms.ModelForm):
    """Formulário para cadastrar/editar tarefas."""
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'completed', 'related_course']
        labels = {
            'title': 'Título',
            'description': 'Descrição',
            'due_date': 'Data de Entrega',
            'completed': 'Concluída',
            'related_course': 'Disciplina Relacionada',
        }
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
