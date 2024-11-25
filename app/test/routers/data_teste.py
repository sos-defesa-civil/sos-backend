from datetime import datetime

def usuario_token_ocorrencia():
    return {
        "nome": "User Token Ocorrencia",
        "data_nascimento": "2000-01-01",
        "cpf": "13345678901",
        "email": "test_ocorrencia@example.com",
        "senha": "password",
        "admin": False,
        "endereco": "123 Test St",
        "num_ocorrencias_registradas": 0,
        "telefone": "1234567890",
        "celular": "0987654321"
    }

def usuario_token_feedback():
    return {
        "nome": "User Token FeedBack",
        "data_nascimento": "2000-01-01",
        "cpf": "12345678901",
        "email": "test_feedback@example.com",
        "senha": "password",
        "admin": False,
        "endereco": "123 Test St",
        "num_ocorrencias_registradas": 0,
        "telefone": "1234567890",
        "celular": "0987654321"
    }

def usuario_token_curtida():
    return {
        "nome": "User Token Curtida",
        "data_nascimento": "2000-01-01",
        "cpf": "14345678901",
        "email": "test_curtida@example.com",
        "senha": "password",
        "admin": False,
        "endereco": "123 Test St",
        "num_ocorrencias_registradas": 0,
        "telefone": "1234567890",
        "celular": "0987654321"
    }


def usuario_cidadao():
    return{
        "nome": "Ana Souza",
        "data_nascimento": datetime(1985, 3, 20).isoformat(),
        "cpf": "98765432100",
        "email": "ana@example.com",
        "senha": "senha_cidadao",
        "admin": False,
        "endereco": "Rua Principal, 123",
        "num_ocorrencias_registradas": 0,
        "telefone": "(11) 2345-6789",
        "celular": "(11) 91234-5678"
    }

def usuario_funcionario():
    return {
        "nome": "Carlos Pereira",
        "data_nascimento": datetime(1970, 8, 10).isoformat(),
        "cpf": "11122233344",
        "email": "carlos@example.com",
        "senha": "senha_funcionario",
        "admin": True,
        "cargo": "Coordenador",
        "nivel_acesso": "Alto"
    }

def usuario_funcionario2():
    return {
        "nome": "José Silva",
        "data_nascimento": datetime(1970, 8, 10).isoformat(),
        "cpf": "11122233377",
        "email": "js@example.com",
        "senha": "senha_funcionario",
        "admin": True,
        "cargo": "Dev",
        "nivel_acesso": "Alto"
    }

def usuario_update():
    return {
        "nome": "João Silva Atualizado",
        "data_nascimento": "1990-05-15",
        "cpf": "12345678900",
        "email": "joao_atualizado@example.com",
        "senha": "nova_senha_segura",
        "admin": True
    }

def ocorrencia_alagamento():
    return {
    "tipo": "alagamentos",
    "bairro": "bairro1",
    "descricao": "Incident description tipo 3",
    "data_registro": "2024-10-01T13:00:00",
    "ultima_atualizacao": "2024-10-24T14:00:00",
    "user_id": 1,
    "latitude": 40.73061,
    "longitude": -73.935242
    }

def curtida_data(id_ocorrencia):
    return {
        'user_id': id,
        'oc_id': id_ocorrencia,
        'data_registro': '2024-10-24T14:00:00'
        }