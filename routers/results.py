

from fastapi import APIRouter, status, HTTPException


from models.avgModels import AvgMunicipio, AvgComarca, AvgProvincia

import sqlite3
route_result = APIRouter(prefix='/results')

@route_result.get('/avgmunicipi', tags=['Results'], response_model=list[AvgMunicipio])
async def get_avg_municipi():
   try:
       # Conectar a la base de datos
       conn = sqlite3.connect("emt.db")
       cursor = conn.cursor()

       # Consulta SQL
       query = """
                 SELECT 
                    e.Provincia,
                    e.Comarca,
                    e.Municipi,
                    v.NomVariable,
                    AVG(d.Valor) AS ValorMedio
                 FROM 
                    DadesEstacio d
                 JOIN 
                    Estacio e ON d.CodiEstacio = e.CodiEstacio
                 JOIN 
                    Variables v ON d.CodiVariable = v.CodiVariable
                 GROUP BY 
                    e.Provincia, e.Comarca, e.Municipi, v.NomVariable
                 ORDER BY 
                    e.Provincia, e.Comarca, e.Municipi, v.NomVariable;
                 """

       cursor.execute(query)
       rows = cursor.fetchall()

       # Cerrar conexión
       conn.close()

       # Crear lista de resultados
       results = [
           AvgMunicipio(
               provincia=row[0],
               comarca=row[1],
               municipi=row[2],
               nom_variable=row[3],
               valor_medio=row[4]
           )
           for row in rows
       ]

       return results
   except Exception as e:
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail=f"Error al consultar la base de datos: {str(e)}")

@route_result.get('/avgcomarca', tags=['Results'], response_model=list[AvgComarca])
async def get_avg_comarca():
   try:
       # Conectar a la base de datos
       conn = sqlite3.connect("emt.db")
       cursor = conn.cursor()

       # Consulta SQL
       query = """
                 SELECT 
                    e.Provincia,
                    e.Comarca,
                    v.NomVariable,
                    AVG(d.Valor) AS ValorMedio
                 FROM 
                    DadesEstacio d
                 JOIN 
                    Estacio e ON d.CodiEstacio = e.CodiEstacio
                 JOIN 
                    Variables v ON d.CodiVariable = v.CodiVariable
                 GROUP BY 
                    e.Provincia, e.Comarca, v.NomVariable
                 ORDER BY 
                    e.Provincia, e.Comarca, v.NomVariable;
                 """

       cursor.execute(query)
       rows = cursor.fetchall()

       # Cerrar conexión
       conn.close()

       # Crear lista de resultados
       results = [
           AvgComarca(
               provincia=row[0],
               comarca=row[1],
               nom_variable=row[2],
               valor_medio=row[3]
           )
           for row in rows
       ]

       return results
   except Exception as e:
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail=f"Error al consultar la base de datos: {str(e)}")

@route_result.get('/avgprovincia', tags=['Results'], response_model=list[AvgProvincia])
async def get_avg_provincia():
   try:
       # Conectar a la base de datos
       conn = sqlite3.connect("emt.db")
       cursor = conn.cursor()

       # Consulta SQL
       query = """
                 SELECT 
                    e.Provincia,
                    v.NomVariable,
                    AVG(d.Valor) AS ValorMedio
                 FROM 
                    DadesEstacio d
                 JOIN 
                    Estacio e ON d.CodiEstacio = e.CodiEstacio
                 JOIN 
                    Variables v ON d.CodiVariable = v.CodiVariable
                 GROUP BY 
                    e.Provincia, v.NomVariable
                 ORDER BY 
                    e.Provincia, v.NomVariable;
                 """

       cursor.execute(query)
       rows = cursor.fetchall()

       # Cerrar conexión
       conn.close()

       # Crear lista de resultados
       results = [
           AvgProvincia(
               provincia=row[0],
               nom_variable=row[1],
               valor_medio=row[2]
           )
           for row in rows
       ]

       return results
   except Exception as e:
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail=f"Error al consultar la base de datos: {str(e)}")