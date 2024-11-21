# SOS Backend

Este é o repositório para o backend do projeto SOS defesa civil. Feito com FastAPI, SQLAlchemy, e Alembic.


## Estrutura do Projeto

Abaixo está a estrutura principal do projeto e uma breve descrição de cada diretório/arquivo:

```
sos-backend/
├── alembic/              # Diretório de configuração e gerenciamento de migrações de banco de dados.
├── app/
│   ├── auth/             # Módulo para lógica de autenticação e autorização.
│   ├── models/           # Definição dos modelos do SQLAlchemy que representam as tabelas do banco de dados.
│   ├── repositories/     # Camada de acesso ao banco de dados (CRUD e consultas específicas).
│   ├── routers/          # Rotas da aplicação, organizadas por funcionalidade.
│   ├── schemas/          # Esquemas Pydantic para validação e serialização de dados.
│   ├── test/             # Testes automatizados para validar as funcionalidades da aplicação.
│   ├── database.py       # Configuração da conexão com o banco de dados e inicialização do SQLAlchemy.
│   └── main.py           # Arquivo principal para inicializar a aplicação FastAPI.
├── requirements.txt      # Lista de dependências Python necessárias para o projeto.
└── README.md             # Documentação do projeto.
```

Esta estrutura organiza o projeto de forma simples e modular, facilitando a manutenção, o crescimento e a integração do código ao longo do tempo

## Uso dos enpoints

O backend do projeto fornece diversos endpoints para gerenciar e acessar os recursos da aplicação. Estes endpoints foram projetados para atender as necessidades da aplicação, como autenticação, gerenciamento de ocorrências, envio de ocorrências e feedbacks, entre outros.

Cada endpoint está documentado detalhadamente no Swagger UI, permitindo que você explore, teste e entenda as funcionalidades oferecidas pela API.

### Documentação com Swagger

O projeto utiliza o Swagger UI integrado ao FastAPI para fornecer uma documentação interativa e fácil de usar para as APIs.

#### Acessando o Swagger UI
Após iniciar o servidor, a documentação estará disponível em:

- Swagger UI: http://127.0.0.1:8000/docs

    Interface interativa para testar as rotas e visualizar os detalhes de cada endpoint.

- ReDoc: http://127.0.0.1:8000/redoc
    
    Documentação detalhada em um formato alternativo, ideal para leitura técnica.

#### Testando as APIs no Swagger UI

Ao acessar http://127.0.0.1:8000/docs no navegador.
Escolha uma rota na lista de endpoints disponíveis.
Clique em "Try it out" para testar a rota diretamente da interface.
Insira os parâmetros necessários e clique em "Execute" para enviar a requisição.
Veja a resposta no painel exibido, incluindo o status HTTP e os dados retornados.


## Instalação

### 1. Clone o repositório

```
git clone https://github.com/sos-defesa-civil/sos-backend.git

cd sos-backend
```

### 2. Crie e ative o ambiente virtual

Linux/macOS:

```
python3 -m venv venv

source venv/bin/activate
```
Windows:

```
python -m venv venv

venv\Scripts\activate
```

### 3. Instalar dependências


```
pip install -r requirements.txt
```

### 4. Configurando a database

Usando o alembic para criar as migrations e as tabelas da database.

```
alembic upgrade head
```

### 5. Rodando a aplicação

Para iniciar o servidor FastAPI, rode o comando:

```
uvicorn app.main:app --reload
```

O API estará disponível em ``http://127.0.0.1:8000``.

## Database Migrations

Quando fizer alterações nos modelos do SQLAlchemy, crie as novas migrações usando o Alembic:  

```
alembic revision --autogenerate -m "Your migration message"

alembic upgrade head
```
