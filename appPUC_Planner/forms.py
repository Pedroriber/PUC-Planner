from django import forms

from .models import Course


class CourseForm(forms.ModelForm):
    """Formulário básico para cadastrar/editar disciplinas.

    Os relacionamentos com `Curso` (via `CursoDisciplina`) são gerenciados
    separadamente, então o formulário cuida apenas dos campos diretos.
    """

    prerequisites = forms.CharField(
        label="Pré-requisitos",
        required=False,
        widget=forms.Textarea(attrs={"rows": 2}),
        help_text="Informe códigos separados por vírgula, ex.: MAT 4162, ENG 4010",
    )

    corequisites = forms.CharField(
        label="Co-requisitos",
        required=False,
        widget=forms.Textarea(attrs={"rows": 2}),
        help_text="Códigos cursados em conjunto, ex.: CTC 4001, CTC 4002",
    )

    class Meta:
        model = Course
        fields = ["code", "name", "credits", "syllabus_url", "prerequisites", "corequisites"]
        labels = {
            "code": "Código",
            "name": "Nome",
            "credits": "Créditos",
            "syllabus_url": "Link da ementa",
            "prerequisites": "Pré-requisitos",
            "corequisites": "Co-requisitos",
        }
        widgets = {
            "syllabus_url": forms.URLInput(attrs={"placeholder": "https://..."}),
        }
