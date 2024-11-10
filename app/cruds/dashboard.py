from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.ocorrencia import Ocorrencia
from app.models.curtida import Curtida
from app.schemas.dashboard import CardResponse, TipoCount, MonthlyTipoCount, PieChartResponse, MonthlyPieChartResponse

def get_ocorrencia_data(db: Session) -> CardResponse:
    # Define date ranges
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    last_week_start = today - timedelta(days=7)
    week_before_start = today - timedelta(days=14)

    # Query total occurrences
    total = db.query(func.count(Ocorrencia.id)).scalar()

    # Query occurrences for today
    today_count = db.query(func.count(Ocorrencia.id)).filter(func.date(Ocorrencia.data_registro) == today).scalar()

    # Query occurrences for yesterday
    yesterday_count = db.query(func.count(Ocorrencia.id)).filter(func.date(Ocorrencia.data_registro) == yesterday).scalar()

    # Query occurrences for the last week
    last_week_count = db.query(func.count(Ocorrencia.id)).filter(Ocorrencia.data_registro >= last_week_start).scalar()

    # Query occurrences for the week before last
    week_before_count = db.query(func.count(Ocorrencia.id)).filter(Ocorrencia.data_registro >= week_before_start, Ocorrencia.data_registro < last_week_start).scalar()

    # Calculate percentage difference for yesterday
    if yesterday_count > 0:
        yesterday_percent = ((today_count - yesterday_count) / yesterday_count) * 100
    else:
        yesterday_percent = 0

    # Calculate percentage difference for last week
    if week_before_count > 0:
        last_week_percent = ((last_week_count - week_before_count) / week_before_count) * 100
    else:
        last_week_percent = 0

    # Create Card instance with the counts and percentage differences
    return CardResponse(total=total, today=today_count, yesterdayPercent=yesterday_percent, lastWeekPercent=last_week_percent)

def get_curtida_data(db: Session) -> CardResponse:
    # Define date ranges
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    last_week_start = today - timedelta(days=7)
    week_before_start = today - timedelta(days=14)

    # Query total occurrences
    total = db.query(func.count(Curtida.id)).scalar()

    # Query occurrences for today
    today_count = db.query(func.count(Curtida.id)).filter(func.date(Curtida.data_registro) == today).scalar()

    # Query occurrences for yesterday
    yesterday_count = db.query(func.count(Curtida.id)).filter(func.date(Curtida.data_registro) == yesterday).scalar()

    # Query occurrences for the last week
    last_week_count = db.query(func.count(Curtida.id)).filter(Curtida.data_registro >= last_week_start).scalar()

    # Query occurrences for the week before last
    week_before_count = db.query(func.count(Curtida.id)).filter(Curtida.data_registro >= week_before_start, Curtida.data_registro < last_week_start).scalar()

    # Calculate percentage difference for yesterday
    if yesterday_count > 0:
        yesterday_percent = ((today_count - yesterday_count) / yesterday_count) * 100
    else:
        yesterday_percent = 0

    # Calculate percentage difference for last week
    if week_before_count > 0:
        last_week_percent = ((last_week_count - week_before_count) / week_before_count) * 100
    else:
        last_week_percent = 0

    # Create Card instance with the counts and percentage differences
    return CardResponse(total=total, today=today_count, yesterdayPercent=yesterday_percent, lastWeekPercent=last_week_percent)

def count_ocorrencias_by_tipo(db: Session) -> PieChartResponse:
    # Query to count occurrences for each unique tipo
    result = db.query(Ocorrencia.tipo, func.count(Ocorrencia.id).label('count'))\
               .group_by(Ocorrencia.tipo)\
               .all()

    # If no results, return an empty list
    tipo_counts = [TipoCount(tipo=tipo, count=count) for tipo, count in result]

    # Return PieChartResponse with the data
    return PieChartResponse(data=tipo_counts)

def count_ocorrencias_by_tipo_per_month(db: Session) -> MonthlyPieChartResponse:
    # Get current year
    current_year = datetime.now().year

    # Query to count occurrences for each unique tipo, grouped by year and month
    result = db.query(
                Ocorrencia.tipo,
                func.extract('year', Ocorrencia.data_registro).label('year'),
                func.extract('month', Ocorrencia.data_registro).label('month'),
                func.count(Ocorrencia.id).label('count')
            )\
            .filter(func.extract('year', Ocorrencia.data_registro) == current_year).group_by(Ocorrencia.tipo, 'year', 'month')\
            .order_by('year', 'month')\
            .all()

    # Convert result to a list of MonthlyTipoCount objects
    monthly_counts = [MonthlyTipoCount(tipo=tipo, year=int(year), month=int(month), count=int(count)) for tipo, year, month, count in result]

    return MonthlyPieChartResponse(data=monthly_counts)