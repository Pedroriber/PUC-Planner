from django import forms
from .models import Course


class CourseForm(forms.ModelForm):    
    class Meta:
        model = Course
        fields = ['code', 'name', 'credits']
        labels = {
            'code': 'Código',
            'name': 'Nome',
            'credits': 'Créditos',
        }
