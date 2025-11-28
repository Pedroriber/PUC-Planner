from django import forms
from .models import Course


class CourseForm(forms.ModelForm):    
    class Meta:
        model = Course
        fields = ['code', 'name', 'credits', 'program', 'pos_top_px', 'pos_left_pct', 'prerequisites']
        labels = {
            'code': 'Código',
            'name': 'Nome',
            'credits': 'Créditos',
            'program': 'Curso / Programa',
            'pos_top_px': 'Posição top (px)',
            'pos_left_pct': 'Posição left (%)',
            'prerequisites': 'Pré-requisitos (códigos, separados por vírgula)',
        }
