from abc import ABC, abstractmethod
from typing import Optional
from .modelo_orm import db, Obra
import pandas as pd

# Definir superclase abstracta
class GestionarObra(ABC):
  # Definir métodos abstractos
  @abstractmethod
  def extraer_datos(self, archivo: str) -> pd.DataFrame:
    pass
  
  @abstractmethod
  def conectar_db(self) -> bool:
    pass
  
  @abstractmethod
  def mapear_orm(self) -> bool:
    pass
  
  @abstractmethod
  def limpiar_datos(self) -> pd.DataFrame:
    pass
  
  @abstractmethod
  def cargar_datos(self) -> bool:
    pass
  
  @abstractmethod
  def nueva_obra(self) -> Optional[Obra]:
    pass
  
  @abstractmethod
  def obtener_indicadores(self) -> dict:
    pass

# Implementar subclase
class GestionarObraCSV(GestionarObra):
  # Campos requeridos (definidos previamente)
  __REQUERIDO = [
      "nombre",
      "tipo",
      "area",
      "barrio",
      "comuna",
      "monto_contrato",
      "etapa",
      "contratacion_tipo",
      "nro_contratacion",
      "licitacion_oferta_empresa",
      "expediente_numero",
      "destacada",
      "fecha_inicio",
      "fecha_fin_inicial",
      "financiamiento",
      "porcentaje_avance",
      "plazo_meses",
      "mano_obra",
  ]

  def __init__(self):
    self.datos = None

  def __str__(self) -> str:
    return 'Gestor de obras iniciado correctamente'

# Implementar métodos
  def extraer_datos(self, archivo: str) -> pd.DataFrame:
    try:
      self.datos = pd.read_csv(archivo, delimiter=';')

      print('Datos extraídos con éxito')
      return self.datos
    except Exception as error:
      print(f'Error al extraer datos: {error}')
      return pd.DataFrame()
    
  def conectar_db(self) -> bool:
    try:
      db.connect()

      print('Base de datos conectada exitosamente')
      return True
    except Exception as error:
      print('Error al conectarse con la base de datos:', error)
      return False

  def mapear_orm(self) -> bool:
    try:
      db.create_tables([Obra], safe=True)
      
      print('Tablas creadas exitosamente')
      return True
    except Exception as error:
      print('Error al mapear ORM:', error)
      return False

  def limpiar_datos(self, datos: pd.DataFrame) -> pd.DataFrame:
    try:
      REQUERIDO = self.__REQUERIDO
      
      # Renombrar columna y campos por compatibilidad 
      datos = datos.rename(columns={'expediente-numero': 'expediente_numero'})
      datos['destacada'] = datos['destacada'].apply(lambda x: True if x == 'SI' else False)

      # Filtrar y limpiar datos
      datos_filtrados = datos.dropna(how='all')
      datos_limpios = datos_filtrados.dropna(subset=REQUERIDO)
      self.datos = datos_limpios

      print('Datos limpios generados con éxito')
      return self.datos
    except Exception as error:
      print(f'Error al limpiar datos: {error}')
      return datos
    
  def cargar_datos(self, datos: pd.DataFrame) -> bool:
    try:
      REQUERIDO = self.__REQUERIDO

      # Iterar cada fila para crear entradas sin duplicados
      for _, row in datos.iterrows():
        if Obra.select().where(Obra.nombre == row['nombre']).exists():
          print(f"La obra '{row['nombre']}' ya existe.")
          continue

        if all(key in row for key in REQUERIDO):
          Obra.create(
            nombre = row['nombre'],
            tipo = row['tipo'],
            area = row['area'],
            barrio = row['barrio'],
            comuna = row['comuna'],
            monto_contrato = row['monto_contrato'],
            etapa = row['etapa'],
            contratacion_tipo = row['contratacion_tipo'],
            nro_contratacion = row['nro_contratacion'],
            licitacion_oferta_empresa = row['licitacion_oferta_empresa'],
            expediente_numero = row['expediente_numero'],
            destacada = row['destacada'],
            fecha_inicio = row['fecha_inicio'],
            fecha_fin_inicial = row['fecha_fin_inicial'],
            financiamiento = row['financiamiento'],
            porcentaje_avance = row['porcentaje_avance'],
            plazo_meses = row['plazo_meses'],
            mano_obra = row['mano_obra']
          )

      print('Datos cargados exitosamente')
      return True
    except Exception as error:
      print(f"Error al cargar los datos: {error}")
      return False

  def nueva_obra(self) -> Optional[Obra]:
    try:
      # Solicitar datos al usuario
      nombre = input("Ingrese el nombre de la obra: ")
      tipo = input("Ingrese el tipo de obra: ")
      area = input("Ingrese el área responsable: ")
      barrio = input("Ingrese el barrio: ")
      comuna = int(input('Ingrese la comuna: '))
      monto_contrato = float(input("Ingrese el monto del contrato: "))

      # Crear nueva entrada con esos datos
      nueva_obra = Obra(
        nombre = nombre,
        tipo = tipo,
        area = area,
        barrio = barrio,
        comuna = comuna,
        monto_contrato = monto_contrato
      )
      nueva_obra.save()

      print('Obra creada exitosamente')
      return nueva_obra
    except Exception as error:
      print(f'Error al crear nueva obra: {error}')
      return None

  def obtener_indicadores(self) -> dict:
    try:
      indicadores = {}
      return indicadores

    except Exception as error:
      print('Error al obtener indicadores:', error)
      return {}