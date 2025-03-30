# EMT
App predicció boletaire

Saber, per una data donada, els llocs on serà més probable trobar bolets. 

Ens basem en cuatre factors determinants. 

- 11 La pluja: 16 - 18 dies abans de la data ha d'haver plogut
- 33 La temperatura desde els 15 dies abans ha de estar entre 08 i 15
- 35 La humitat ha de estar entre el 70 i 80 
- 46 Velocitat del vent < 5,5 m/s 

Si no ha hagut pluja es descarta el lloc. 

Exemple: Per la data 16/03/2025.

11 Pluja: ha d'haver plogut 16-18 dies abans, sumariem les dates 26,27 i 28/02.

33 La mitja de la temperatura des de 14/03 (agafem 1 dia menys de la data perque molt probablament el dia abans de la data no tindrem dades, ja que aquesta serà a futur). Per tant les dades són de 14/03 al 01/03

35 Humitat per les mateixes dates de temperatura la mitjana de la humitat 

46 Vent. Per les mateixes dates anteriors la mitjana del vent. 


Variables de entorno del sistema
setx EMT_API_KEY
setx EMT_URLBASE


Estadistiques diaris. 
- 1000 Temperatura
- 1300 Precipitació acumulada diaria
- 1505 Velocitat mitjana diària del vent 2 m (esc.)
- 1100 Humitat relativa mitjana diària
{{baseurlEMT}}/variables/estadistics/diaris/1000?any=2025&mes=02



 
