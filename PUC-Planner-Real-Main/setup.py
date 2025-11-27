#!/usr/bin/env python
"""
Script de setup para o PUC Planner
Execute este script após clonar o repositório para configurar o projeto.
"""

import os
import sys
import shutil
import subprocess


def print_step(message):
    """Imprime uma mensagem de etapa formatada"""
    print(f"\n{'='*60}")
    print(f"  {message}")
    print(f"{'='*60}\n")


def run_command(command, description):
    """Executa um comando e trata erros"""
    print(f"➤ {description}...")
    try:
        subprocess.run(command, check=True, shell=True)
        print(f"✓ {description} - Concluído!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Erro ao {description.lower()}: {e}")
        return False


def setup_project():
    """Configura o projeto completo"""
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║            PUC PLANNER - SETUP AUTOMÁTICO             ║
    ╚════════════════════════════════════════════════════════╝
    """)

    # 1. Verificar arquivo .env
    print_step("1. Configurando variáveis de ambiente")
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            shutil.copy('.env.example', '.env')
            print("✓ Arquivo .env criado a partir de .env.example")
        else:
            print("⚠ Arquivo .env.example não encontrado!")
    else:
        print("✓ Arquivo .env já existe")

    # 2. Instalar dependências
    print_step("2. Instalando dependências")
    if not run_command("pip install -r requirements.txt", "Instalando pacotes Python"):
        print("⚠ Falha ao instalar dependências. Continue manualmente.")

    # 3. Executar migrações
    print_step("3. Configurando banco de dados")
    if not run_command("python manage.py migrate", "Executando migrações"):
        print("⚠ Falha nas migrações. Execute 'python manage.py migrate' manualmente.")

    # 4. Perguntar sobre superusuário
    print_step("4. Criando superusuário (opcional)")
    criar_super = input("Deseja criar um superusuário agora? (s/N): ").strip().lower()
    if criar_super == 's':
        print("\n➤ Execute o seguinte comando após este script:")
        print("  python manage.py createsuperuser --matricula <sua_matricula> --email <seu_email>")
    else:
        print("✓ Você pode criar um superusuário depois com:")
        print("  python manage.py createsuperuser --matricula <matricula> --email <email>")

    # 5. Instruções finais
    print_step("5. Setup concluído!")
    print("""
    ✅ O projeto está configurado e pronto para uso!
    
    Para iniciar o servidor de desenvolvimento:
        python manage.py runserver
    
    Acesse em seu navegador:
        http://127.0.0.1:8000/
    
    Primeira vez usando?
        1. Acesse http://127.0.0.1:8000/cadastro/
        2. Crie sua conta
        3. Faça login com sua matrícula e senha
    
    Documentação completa: README.md
    """)


if __name__ == "__main__":
    try:
        setup_project()
    except KeyboardInterrupt:
        print("\n\n⚠ Setup interrompido pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Erro durante setup: {e}")
        sys.exit(1)
