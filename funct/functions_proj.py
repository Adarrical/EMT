import requests
import os
from dotenv import load_dotenv
from fastapi import APIRouter,status,HTTPException
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime

def get_months(start_date, end_date):
    months = []
    current_date = start_date
    while current_date <= end_date:
        month_year = current_date.strftime("%Y-%m")
        if month_year not in months:
            months.append(month_year)

        next_month = current_date.month + 1 if current_date.month < 12 else 1
        next_year = current_date.year if current_date.month < 12 else current_date.year + 1
        current_date = datetime(next_year, next_month, 1)  # Primer día del siguiente mes

    return months


async def get_api_data(variable, year, month):
    load_dotenv()

    EMT_API_KEY = os.getenv('EMT_API_KEY')
    EMT_URLBASE = os.getenv('EMT_URLBASE')

    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": EMT_API_KEY,
    }

    url = f"{EMT_URLBASE}/variables/estadistics/diaris/{variable}?any={year}&mes={month}"

    response = requests.get(url, headers=headers)

    status_code = response.status_code

    return JSONResponse(status_code=status_code, content=jsonable_encoder(response.content))