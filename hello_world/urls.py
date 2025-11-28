"""
URL configuration for hello_world project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from hello_world.core import views as core_views

urlpatterns = [
    path("exemplo/", core_views.index, name="index"),
    path("", core_views.home, name="home"),
    path("login/", core_views.login_view, name="login"),
    path("logout/", core_views.logout_view, name="logout"),
    path("cadastro/", core_views.cadastro, name="cadastro"),
    path("esqueci-senha/", core_views.esqueci_senha, name="esqueci_senha"),
    path("redefinir-senha/<uidb64>/<token>/", core_views.redefinir_senha, name="redefinir_senha"),
    path("consulta-disciplina/", core_views.consulta_disciplina, name="consulta_disciplina"),
    path("fluxograma/", core_views.fluxograma, name="fluxograma"),
    # Generic fluxograma by program (ex: /fluxograma/Engenharia%20de%20Computacao/)
    path("fluxograma/<str:program>/", core_views.fluxograma_course, name="fluxograma_course"),
    path("fluxograma1/", core_views.fluxograma1, name="fluxograma1"),
    path("fluxograma2/", core_views.fluxograma2, name="fluxograma2"),
    path("fluxograma3/", core_views.fluxograma3, name="fluxograma3"),
    path("grade-horaria/", core_views.grade_horaria, name="grade_horaria"),
    
    path("disciplinas/", core_views.course_list, name="course_list"),
    path("disciplinas/nova/", core_views.course_create, name="course_create"),
    path("disciplinas/<int:pk>/editar/", core_views.course_update, name="course_update"),
    path("disciplinas/<int:pk>/deletar/", core_views.course_delete, name="course_delete"),
    
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
