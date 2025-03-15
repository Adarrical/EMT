from datetime import datetime, timedelta

from fastapi import APIRouter,status
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

route_date = APIRouter(prefix='/date')

@route_date.get('/validate{date}',tags=['Date'])
def validate_date(date:datetime):
    if date.date() < datetime.now().date():
        status_code = status.HTTP_406_NOT_ACCEPTABLE
        result = { "message": "La fecha debe estar a futuro"}
    else:
        status_code = status.HTTP_200_OK
        result = date
    return JSONResponse(status_code=status_code, content=jsonable_encoder(result))

@route_date.get('/get_periods{date}',tags=['Date'])
def get_periods(date:datetime):
    date_from_rain = date.date() - timedelta(days=18)
    date_to_rain = date.date() - timedelta(days=16)

    date_from_rest_variables = date.date() - timedelta(days=15)
    date_to_rest_variables = date.date() - timedelta(days=1)

    status_code = status.HTTP_200_OK
    result = { 'date_from_rain': date_from_rain,
               'date_to_rain': date_to_rain,
               'date_from_rest_variables': date_from_rest_variables,
               'date_to_rest_variables': date_to_rest_variables
             }
    return JSONResponse(status_code=status_code, content=jsonable_encoder(result))
