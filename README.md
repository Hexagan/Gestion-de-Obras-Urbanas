<img width=100% src="https://capsule-render.vercel.app/api?type=waving&color=e1bbbd&height=120&section=header"/>

# Trabajo práctico integrador
## Materia: Programación Orientada a Objetos

### Grupo:
- Daniel Sosa
- Federico Salvador
- Agustín Braco
- Tatiana Pinzon

### Descripción:
Sistema de gestión de obras urbanas con manejo de POO, importación de datasets desde un archivo CSV y persistencia de objetos con ORM Peewee en una base de datos SQLite.
Se requiere desarrollar un software en Python para gestionar las obras urbanas de la Ciudad de Buenos Aires, tomando como origen de datos un dataset público del gobierno de la ciudad y haciendo uso del modelo ORM de la librería ó módulo “peewee”. Para el manejo y operaciones con el dataset se debe utilizar la librería ó módulo “pandas”. Y para el manejo y operaciones con arrays pueden utilizar la librería ó módulo “numpy”.

### Instalación:
Para poder ejecutar el proyecto, se debe instalar previamente las bibliotecas requeridas:

1. Navegar al directorio raíz:
`cd Sosa-Salvador-Braco-Pinzon`

2. Ejecutar el comando de instalación:
`pip install .`

### Inicialización:
Con las bibliotecas instaladas, podemos ejecutar el proyecto (también desde el directorio raíz):  
`python app.py`

### Tablas:
#### 1. Etapa
  - `id`: Variable identificadora únca. Almacena el identificador de cada fila.
  - `etapa`: Variable de texto única. Almacena el nombre de la etapa.

Algunos valores permitidos:
```
NUEVA
PROYECTO
FINALIZADA
RESCINDIDA
NEUTRALIZADA
EN OBRA
DESESTIMADA
PARALIZADA
ADJUDICADA
ANTEPROYECTO
```

#### 2. Tipo
  - `id`: Variable identificadora únca. Almacena el identificador de cada fila.
  - `tipo`: Variable de texto única. Almacena el nombre del tipo.

Algunos valores permitidos:
```
ESCUELAS
ESPACIO PÚBLICO
VIVIENDA
ARQUITECTURA
TRANSPORTE
SALUD
VIVIENDA NUEVA
INSTALACIONES
INGENIERIA
INFRAESTRUCTURA
```

#### 3. Area
  - `id`: Variable identificadora únca. Almacena el identificador de cada fila.
  - `area`: Variable de texto única. Almacena el nombre del area.

Algunos valores permitidos:
```
MINISTERIO DE EDUCACIÓN
SECRETARÍ­A DE TRANSPORTE Y OBRAS PÚBLICAS
CORPORACIÓN BUENOS AIRES SUR
INSTITUTO DE LA VIVIENDA
MINISTERIO DE SALUD
SUBSECRETARÍ­A DE GESTIÓN COMUNAL
MINISTERIO DE CULTURA
MINISTERIO DE ESPACIO PÚBLICO E HIGIENE URBANA
MINISTERIO DE DESARROLLO HUMANO Y HÁBITAT
SUBSECRETARÍA DE PROYECTOS Y OBRAS
```

#### 4. Barrio
  - `id`: Variable identificadora únca. Almacena el identificador de cada fila.
  - `barrio`: Variable de texto única. Almacena el nombre del barrio.

Algunos valores permitidos:
```
VILLA URQUIZA
MONTSERRAT
SAN NICOLÁS
VILLA LUGANO
VILLA SOLDATI
PUERTO MADERO
RECOLETA
LINIERS
VILLA RIACHUELO
COGHLAN
```

#### 5. Empresa
  - `id`: Variable identificadora únca. Almacena el identificador de cada fila.
  - `licitacion_oferta_empresa`: Variable de texto única. Almacena el nombre de la empresa.

Algunos valores permitidos:
```
CRIBA S.A.
ALTOTE S.A
ROL INGENIERIA S.A
DAL CONSTRUCCIONES S.A
BRICONS S.A.I.C.F.I.
DYCASA S.A.
CUNUMI S.A
CONSTRUCTORA SUDAMERICANA S.A.
VIDOGAR CONSTRUCCIONES S.A
CAVCON S.A.
```

#### 6. Contratacion
  - `id`: Variable identificadora únca. Almacena el identificador de cada fila.
  - `contratacion_tipo`: Variable de texto no única. Almacena el nombre del tipo de contratación.

Algunos valores permitidos:
```
LICITACIÓN PÚBLICA
CONTRATACIÓN DIRECTA
LICITACIÓN PRIVADA
LICITACIÓN PRIVADA DE OBRA MENOR
566/2010
566/10 Y 433/16
OBRA MENOR
SIN EFECTO
DECRETO N° 433/16
ADICIONAL DE MANTENIMIENTO
```

#### 7. Financiamiento
  - `id`: Variable identificadora únca. Almacena el identificador de cada fila.
  - `financiamiento`: Variable de texto no única. Almacena el nombre del financiamiento.

Algunos valores permitidos:
```
FUENTE 11
PRÉSTAMO BIRF 8706-AR
PRÉSTAMO BID AR-L1260
NACIÓN
F11
PPI
NACIÓN-GCBA
CAF-NACIÓN-GCBA
FUENTE 14
FODUS
```

#### 8. Obra
  - `id`: Variable identificadora únca. Almacena el identificador de cada fila.
  - `nombre`: Variable de texto única. Almacena el nombre de la obra.
  - `tipo`: Variable de clave foránea única. Almacena el ID relacionado a la tabla `Tipo`
  - `area`: Variable de clave foránea única. Almacena el ID relacionado a la tabla `Area`
  - `barrio`: Variable de clave foránea única. Almacena el ID relacionado a la tabla `Barrio`
  - `comuna`: Variable de número entero no única. Almacena el número de comuna.
  - `monto_contrato`: Variable de número decimal no única. Almacena el monto total del contrato.
  - `etapa`: Variable de clave foránea única. Almacena el ID relacionado a la tabla `Etapa`
  - `contratacion_tipo`: Variable de clave foránea única. Almacena el ID relacionado a la tabla `Contratacion`
  - `nro_contratacion`: Variable de texto no única. Almacena el número de contratación.
  - `licitacion_oferta_empresa`: Variable de clave foránea única. Almacena el ID relacionado a la tabla `Empresa`
  - `expediente_numero`: Variable de texto no única. Almacena el número de expediente.
  - `destacada`: Variable booleana. Confirma si la obra es destacada o no.
  - `fecha_inicio`: Variable de fecha no única. Almacena la fecha de inicio de la obra.
  - `fecha_fin_inicial`: Variable de fecha no única. Almacena la fecha de finalización de la obra.
  - `financiamiento`: Variable de clave foránea única. Almacena el ID relacionado a la tabla `Financiamiento`
  - `porcentaje_avance`: Variable de número entero no única. Almacena el número del porcentaje de avance actual.
  - `plazo_meses`: Variable de número entero no única. Almacena el número del plazo total en meses.
  - `mano_obra`: Variable de número entero no única. Almacena el número de la mano de obra total.

<hr>

#### ¡Gracias!

<img width=100% src="https://capsule-render.vercel.app/api?type=waving&color=e1bbbd&height=120&section=footer"/>