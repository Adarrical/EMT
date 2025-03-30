import json

from fastapi import APIRouter,status,HTTPException
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv
from routers.date import get_periods
import os
import requests
import sqlite3
from datetime import datetime
from funct.functions_proj import get_months
from funct.functions_proj import get_api_data

route_data = APIRouter(prefix='/data')

@route_data.get('/stations',tags=['Data'])
async def get_stations():

    load_dotenv()

    EMT_API_KEY = os.getenv('EMT_API_KEY')
    EMT_URLBASE = os.getenv('EMT_URLBASE')


    headers = {
                "Content-Type": "application/json",
                "X-Api-Key": EMT_API_KEY,
               }

    url = f"{EMT_URLBASE}/estacions/metadades"

    response = requests.get(url, headers=headers)

    data = response.json()
    if response.status_code == 200:
        conn = sqlite3.connect("emt.db")
        cursor = conn.cursor()
        for item in data:
            codiestacio = item["codi"]
            nom = item["nom"]
            latitud = item["coordenades"]["latitud"]
            longitud = item["coordenades"]["longitud"]
            municipi = item["municipi"]["nom"]
            comarca = item["comarca"]["nom"]
            provincia = item["provincia"]["nom"]

            cursor.execute("""
                            insert into 
                                Estacio (CodiEstacio, Nom, Latitud, Longitud, Municipi, Comarca, Provincia) 
                                values (?, ? ,?, ?, ? ,?, ?)
                                on conflict (CodiEstacio) do update set 
                                Nom = excluded.Nom,
                                Latitud = excluded.Latitud,
                                Longitud = excluded.Longitud,
                                Municipi = excluded.Municipi,
                                Comarca = excluded.Comarca,
                                Provincia = excluded.Provincia
                            """,
                           ( codiestacio,
                            nom,
                            latitud,
                            longitud,
                            municipi,
                            comarca,
                            provincia )
                            )
            conn.commit()
        conn.close()

    return response.status_code

@route_data.get('/variables{date}',tags=['Data'])
async def get_variables(date:datetime):

    load_dotenv()

    EMT_API_KEY = os.getenv('EMT_API_KEY')
    EMT_URLBASE = os.getenv('EMT_URLBASE')

    result = get_periods(date)

    content = json.loads(result.body)

    #Dades de precipitació
    start_date = datetime.strptime(content["date_from_rain"],"%Y-%m-%d")
    end_date = datetime.strptime(content["date_to_rain"],"%Y-%m-%d")

    months = get_months(start_date, end_date)


    for month in months:

        year_api, month_api = month.split("-")
        variable = 1300 #read readme

        result = await get_api_data(variable, year_api, month_api)

        if result.status_code == 200:
            body_bytes = result.body  # Obtiene el contenido en bytes
            body_str = body_bytes.decode("utf-8")  # Decodificar a string
            items = json.loads(body_str)  # Convertir a JSON (lista o diccionario)
            for item in items:
                codi_estacio = item["codiEstacio"]
                for valor in item["valors"]:
                    value_date = datetime.strptime(valor["data"],"%Y-%m-%dZ")
                    if value_date >= start_date and value_date <= end_date:
                        print(f'codi estacio: {codi_estacio}, data: {value_date}, valor: {valor["valor"]}')

    # Resta de dades
    start_date = datetime.strptime(content["date_from_rest_variables"], "%Y-%m-%d")
    end_date = datetime.strptime(content["date_to_rest_variables"], "%Y-%m-%d")

    variables = [1100,1300,1505] #read readme

    months = get_months(start_date, end_date)


    for variable in variables:
        for month in months:

            year_api, month_api = month.split("-")
            result = await get_api_data(variable, year_api, month_api )

            if result.status_code == 200:
                body_bytes = result.body  # Obtiene el contenido en bytes
                body_str = body_bytes.decode("utf-8")  # Decodificar a string
                body_json = json.loads(body_str)  # Convertir a JSON (lista o diccionario)

            print(body_json)


