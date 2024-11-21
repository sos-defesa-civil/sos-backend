from fastapi import APIRouter, Depends
from app.database import get_db
from app.schemas.dashboard import CardResponse, PieChartResponse, MonthlyPieChartResponse
from app.repositories.dashboard import get_session_data, get_ocorrencia_data, get_curtida_data, count_ocorrencias_by_tipo, count_ocorrencias_by_tipo_per_month
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

@router.get(
    "/dashboard/sessions-card",
    response_model=CardResponse,
    summary="Obter resumo de sessões para o dashboard",
    description=(
        "Esta rota retorna um resumo de dados de sessões para exibição em um card no dashboard.\n\n"
        "### Processos executados:\n"
        "1. Conta o total de sessões registradas no banco de dados.\n"
        "2. Obtém o número de sessões registradas hoje.\n"
        "3. Calcula o número de sessões de ontem e a porcentagem de variação em relação a hoje.\n"
        "4. Obtém o número de sessões na última semana e calcula a variação percentual em relação à semana anterior.\n"
        "5. Retorna os dados processados no formato esperado pelo dashboard."
    ),
)
def ocorrencias_card(db: Session = Depends(get_db)):
    return get_session_data(db)

@router.get("/dashboard/ocorrencias-card",
    response_model=CardResponse,
    summary="Obter resumo de ocorrências para o dashboard",
    description=(
        "Esta rota retorna um resumo de dados de ocorrências para exibição em um card no dashboard.\n\n"
        "### Processos executados:\n"
        "1. Conta o total de ocorrências registradas no banco de dados.\n"
        "2. Obtém o número de ocorrências registradas hoje.\n"
        "3. Calcula o número de ocorrências de ontem e a porcentagem de variação em relação a hoje.\n"
        "4. Obtém o número de ocorrências na última semana e calcula a variação percentual em relação à semana anterior.\n"
        "5. Retorna os dados processados no formato esperado pelo dashboard."
    )
)
def ocorrencias_card(db: Session = Depends(get_db)):
    return get_ocorrencia_data(db)

@router.get("/dashboard/curtidas-card",
    response_model=CardResponse,
    summary="Obter resumo de curtidas para o dashboard",
    description=(
        "Esta rota retorna um resumo de dados de curtidas para exibição em um card no dashboard.\n\n"
        "### Processos executados:\n"
        "1. Conta o total de curtidas registradas no banco de dados.\n"
        "2. Obtém o número de curtidas registradas hoje.\n"
        "3. Calcula o número de curtidas de ontem e a porcentagem de variação em relação a hoje.\n"
        "4. Obtém o número de curtidas na última semana e calcula a variação percentual em relação à semana anterior.\n"
        "5. Retorna os dados processados no formato esperado pelo dashboard."
    )
)
def curtidas_card(db: Session = Depends(get_db)):
    return get_curtida_data(db)

@router.get("/dashboard/pie-chart",
    response_model=PieChartResponse,
    summary="Obter dados de gráfico de pizza para tipos de ocorrências",
    description=(
        "Esta rota retorna os dados necessários para gerar um gráfico de pizza, representando a distribuição "
        "das ocorrências por tipo.\n\n"
        "### Processos executados:\n"
        "1. Conta o número de ocorrências para cada tipo registrado no banco de dados.\n"
        "2. Agrupa os resultados pelo campo `tipo`.\n"
        "3. Retorna os dados formatados em uma lista contendo cada tipo e sua contagem."
    )
)
def pie_chart(db: Session = Depends(get_db)):
    return count_ocorrencias_by_tipo(db)

@router.get("/dashboard/monthly-chart",
    response_model=MonthlyPieChartResponse,
    summary="Obter dados de gráfico mensal por tipo de ocorrência",
    description=(
        "Esta rota retorna os dados necessários para gerar um gráfico mensal agrupado por tipo de ocorrência, "
        "para o ano atual.\n\n"
        "### Processos executados:\n"
        "1. Conta o número de ocorrências para cada tipo, agrupadas por ano e mês.\n"
        "2. Filtra os resultados para incluir apenas as ocorrências do ano atual.\n"
        "3. Ordena os dados pelos campos de ano e mês.\n"
        "4. Retorna os dados formatados em uma lista contendo tipo, ano, mês e a contagem correspondente."
    )
)
def monthly_chart(db: Session = Depends(get_db)):
    return count_ocorrencias_by_tipo_per_month(db);