from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class MatriculaBackend(ModelBackend):
    """Backend de autenticação que permite login por matrícula."""
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Autentica o usuário usando matrícula e senha.
        O parâmetro 'username' na verdade contém a matrícula.
        """
        try:
            # Tenta buscar o usuário pela matrícula
            user = User.objects.get(matricula=username)
        except User.DoesNotExist:
            # Retorna None se o usuário não existir
            return None
        
        # Verifica a senha
        if user.check_password(password):
            return user
        
        return None
    
    def get_user(self, user_id):
        """Retorna o usuário pelo ID."""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
