from django import forms
from .models import Course


class CourseForm(forms.ModelForm):    
    class Meta:
        model = Course
        fields = ['code', 'name', 'credits', 'syllabus_url', 'prerequisites']
        labels = {
            'code': 'Código',
            'name': 'Nome',
            'credits': 'Créditos',
            'syllabus_url': 'Link da ementa',
            'prerequisites': 'Pré-requisitos (códigos, separados por vírgula)',
        }
