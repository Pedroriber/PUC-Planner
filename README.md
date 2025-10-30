# PUC Planner

Sistema de planejamento acadêmico para estudantes da PUC-Rio. Oferece visualização dinâmica das relações entre disciplinas, incluindo pré-requisitos, co-requisitos e grade horária personalizada.

## Instalação

### 1. Clone o repositório e instale as dependências

```bash
pip install -r requirements.txt
```

### 2. Configure o ambiente (opcional)

Copie `.env.example` para `.env` se desejar customizar configurações:

```bash
cp .env.example .env
```

### 3. Configure o banco de dados

```bash
python manage.py migrate
```

### 4. Execute a aplicação

```bash
python manage.py runserver
```

Acesse: **http://127.0.0.1:8000/**

## Primeiro Acesso

Cadastre-se em: **http://127.0.0.1:8000/cadastro/**

## Funcionalidades

- Sistema de autenticação por matrícula
- Consulta de disciplinas
- Visualização de fluxograma interativo
- Grade horária personalizada
- Recuperação de senha via email

## Tecnologias

- Django 5.2.7
- Python 3.8+
- SQLite
