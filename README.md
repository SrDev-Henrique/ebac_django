# ebac_django

Projeto Django do curso EBAC — Backend.

## Requisitos

- Python 3.13+
- pip

## Configuração

1. Clone o repositório e entre na pasta do projeto:

```bash
cd django
```

2. Crie e ative o ambiente virtual:

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Rodando o servidor

```bash
python manage.py runserver
```

Acesse: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

Com `DEBUG=True` e sem URLs configuradas, o Django exibe a página padrão de instalação bem-sucedida.

## Estrutura do projeto

```
django/
├── ebac_django/          # Configurações do projeto
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
└── README.md
```

## Comandos úteis

```bash
# Criar uma app
python manage.py startapp nome_da_app

# Aplicar migrações
python manage.py migrate

# Criar superusuário (admin)
python manage.py createsuperuser

# Abrir shell do Django
python manage.py shell
```

## Dependências

| Pacote | Versão  |
|--------|---------|
| Django | 6.0.7   |
