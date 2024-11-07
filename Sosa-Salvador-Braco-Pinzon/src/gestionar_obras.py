from .modelo_orm import *
from abc import ABC, abstractmethod
from typing import Optional
from peewee import fn, DoesNotExist
import pandas as pd
import re

# Utilidades 
def limpiar_dato(datos, nombre):
  if nombre == 'licitacion_oferta_empresa':
    # Tabla Empresa

    # Eliminar espacios, saltos, caracteres inválidos y convertir en mayúscula
    datos[nombre] = datos[nombre].apply(
      lambda x: re.sub(r'[^\x00-\x7F]+', '', x)
                  .strip()
                  .replace('\n', '')
                  .replace('\r', '')
                  .upper()
                  if isinstance(x, str) and x not in [None, '', '-'] else None
    )

    # Eliminar datos vacios, nulos e incompletos
    incluir = datos[nombre].apply(lambda x: isinstance(x, str) and x not in ['', 'NA', '-', '.'])
    datos = datos[incluir].dropna()

    # Eliminar duplicados
    datos = datos.drop_duplicates(subset=[nombre]).reset_index(drop=True)

    return datos
  else:
    # Tablas Etapa, Tipo, Area, Barrio, Contratacion y Financiamiento
    
    # Eliminar espacios y convertir en mayúscula
    datos[nombre] = datos[nombre].str.strip().str.upper()
    
    # Eliminar datos vacios, nulos e incompletos
    incluir = datos[nombre].apply(lambda x: isinstance(x, str) and x not in ['', 'NA', '-', '.'])
    datos = datos[incluir].dropna()
    
    # Eliminar duplicados
    datos = datos.drop_duplicates(subset=[nombre]).reset_index(drop=True)
    
    return datos

def cargar_dato(datos, tabla, nombre):
    # Iterar sobre cada fila y pasar campo dinámicamente
    for _, row in datos.iterrows():
      if not tabla.filter(**{nombre: row[nombre]}).exists():
        tabla.create(**{nombre: row[nombre]})

def solicitar_dato(texto, tabla, campo):
  while True:
    dato = input(texto).strip().upper()

    if not tabla.select().where(getattr(tabla, campo) == dato).exists():
      print('El valor es inválido. Por favor ingrese un valor válido.')
      continue

    try:
      dato_id = tabla.select().where(getattr(tabla, campo) == dato).get().id
      return dato_id
    except DoesNotExist:
        print('El valor es inválido. Por favor ingrese un valor válido.')
        continue

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
    self.obras = None
    self.etapas = None
    self.tipos = None
    self.areas = None
    self.barrios = None
    self.empresas = None
    self.contrataciones = None
    self.financiamientos = None
    self.barrios_comunas = None

  def __str__(self) -> str:
    return 'Gestor de obras iniciado correctamente'

# Implementar métodos
  def extraer_datos(self, archivo: str) -> pd.DataFrame:
    try:
      datos = pd.read_csv(archivo, delimiter=';')

      # Guardar datos de cada tabla
      self.obras = datos
      self.etapas = pd.DataFrame(datos['etapa'])
      self.tipos = pd.DataFrame(datos['tipo'])
      self.areas = pd.DataFrame(datos['area'])
      self.barrios = pd.DataFrame(datos['barrio'])
      self.empresas = pd.DataFrame(datos['licitacion_oferta_empresa'])
      self.contrataciones = pd.DataFrame(datos['contratacion_tipo'])
      self.financiamientos = pd.DataFrame(datos['financiamiento'])
      self.barrios_comunas = datos[['barrio', 'comuna']]

      print('Datos extraídos con éxito')
      return datos
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
      db.create_tables([Etapa, Tipo, Area, Barrio, Empresa, Contratacion, Financiamiento, Obra], safe=True)
      Etapa.create(etapa='NUEVA')
      Etapa.create(etapa='PROYECTO')
      Etapa.create(etapa='FINALIZADA')
      Etapa.create(etapa='RESCINDIDA')

      print('Tablas creadas exitosamente')
      return True
    except Exception as error:
      print('Error al mapear ORM:', error)
      return False

  def limpiar_datos(self, datos: pd.DataFrame) -> pd.DataFrame:
    try:
      # Renombrar columna
      datos = datos.rename(columns={'expediente-numero': 'expediente_numero'})
      
      # Convertir string a booleano
      datos['destacada'] = datos['destacada'].apply(lambda x: True if x == 'SI' else False)
      
      # Eliminar por campos faltantes
      datos = datos.dropna(subset=self.__REQUERIDO)

      # Convertir string a decimal
      datos['monto_contrato'] = datos['monto_contrato'].apply(lambda x: float(x.replace('$', '').replace('.', '').replace(',', '.')) if isinstance(x, str) else x)
      
      # Convertir string a entero
      datos['plazo_meses'] = datos['plazo_meses'].apply(lambda x: int(x) if isinstance(x, str) and x.isdigit() else None)
      datos = datos.dropna(subset=['plazo_meses'])

      # Convertir comuna en entero y descartar vacíos
      self.barrios_comunas.loc[:, 'comuna'] = pd.to_numeric(self.barrios_comunas['comuna'], errors='coerce')
      self.barrios_comunas = self.barrios_comunas[self.barrios_comunas['comuna'].notna()]
      self.barrios_comunas['comuna'] = self.barrios_comunas['comuna'].astype(int)

      # Limpiar datos de cada tabla
      self.etapas = limpiar_dato(self.etapas, 'etapa')
      self.tipos = limpiar_dato(self.tipos, 'tipo')
      self.areas = limpiar_dato(self.areas, 'area')
      self.barrios = limpiar_dato(self.barrios, 'barrio')
      self.empresas = limpiar_dato(self.empresas, 'licitacion_oferta_empresa')
      self.contrataciones = limpiar_dato(self.contrataciones, 'contratacion_tipo')
      self.financiamientos = limpiar_dato(self.financiamientos, 'financiamiento')
      self.obras = datos
      
      print('Datos limpios generados con éxito')
      return datos
    except Exception as error:
      print(f'Error al limpiar datos: {error}')
      return datos
    
  def cargar_datos(self, datos: pd.DataFrame) -> bool:
    try:
      # Cargar datos en cada tabla
      cargar_dato(self.etapas, Etapa, 'etapa')
      cargar_dato(self.tipos, Tipo, 'tipo')
      cargar_dato(self.areas, Area, 'area')
      cargar_dato(self.barrios, Barrio, 'barrio')
      cargar_dato(self.empresas, Empresa, 'licitacion_oferta_empresa')
      cargar_dato(self.contrataciones, Contratacion, 'contratacion_tipo')
      cargar_dato(self.financiamientos, Financiamiento, 'financiamiento')

      for _, row in datos.iterrows():
        # Validar si existe para no duplicarlo
        if Obra.select().where(Obra.nombre == row['nombre']).exists():
          continue

        Obra.create(
          nombre = row['nombre'],
          tipo = Tipo.get_or_create(tipo = row['tipo'].strip().upper())[0],
          area = Area.get_or_create(area = row['area'].strip().upper())[0],
          barrio = Barrio.get_or_create(barrio = row['barrio'].strip().upper())[0],
          comuna = row['comuna'],
          monto_contrato = row['monto_contrato'],
          etapa = Etapa.get_or_create(etapa = row['etapa'].strip().upper())[0],
          contratacion_tipo = Contratacion.get_or_create(contratacion_tipo = row['contratacion_tipo'].strip().upper())[0],
          nro_contratacion = row['nro_contratacion'],
          licitacion_oferta_empresa = Empresa.get_or_create(licitacion_oferta_empresa = row['licitacion_oferta_empresa'].strip().upper())[0],
          expediente_numero = row['expediente_numero'],
          destacada = row['destacada'],
          fecha_inicio = row['fecha_inicio'],
          fecha_fin_inicial = row['fecha_fin_inicial'],
          financiamiento = Financiamiento.get_or_create(financiamiento = row['financiamiento'].strip().upper())[0],
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
      # Nombre
      while True:
        nombre = input('Ingrese el nombre de la obra: ')
        if Obra.select().where(Obra.nombre == nombre).exists():
          print('La obra ya existe. Por favor ingrese otro nombre.')
        else:
          break

      # Tipo, Area y Barrio
      tipo_id = solicitar_dato('Ingrese el tipo de obra: ', Tipo, 'tipo')
      area_id = solicitar_dato('Ingrese el área responsable: ', Area, 'area')
      barrio_id = solicitar_dato('Ingrese el barrio: ', Barrio, 'barrio')

      # Comuna y Monto
      comuna = int(input('Ingrese el número de la comuna: '))
      monto_contrato = float(input("Ingrese el monto del contrato (número): "))

      # Crear nueva entrada con los datos ingresados
      nueva_obra = Obra(
        nombre = nombre,
        tipo = tipo_id,
        area = area_id,
        barrio = barrio_id,
        comuna = comuna,
        monto_contrato = monto_contrato,
        etapa = 'NUEVA'
      )
      nueva_obra.save()

      print('Obra creada exitosamente')
      return nueva_obra
    except Exception as error:
      print(f'Error al crear nueva obra: {error}')
      return None

  def obtener_indicadores(self) -> dict:
    try:
      # Inicializar indicadores
      indicadores = {
        'areas': [],
        'tipos': [],
        'obras_por_etapa': {},
        'inversion_y_cantidad_por_tipo': {},
        'barrios_por_comuna': {},
        'obras_finalizadas_24_meses': 0,
        'porcentaje_obras_finalizadas': 0,
        'total_mano_obra': 0,
        'monto_total_inversion': 0
      }

      # Listado de todas las áreas responsables
      try:
        areas = Area.select(Area.area).distinct()
        for area in areas:
          indicadores['areas'].append(area.area)
      except OperationalError as error:
        print(f"Error al obtener áreas responsables: {error}")

      # Listado de todos los tipos de obra
      try:
        tipos = Tipo.select(Tipo.tipo).distinct()
        for tipo in tipos:
          indicadores['tipos'].append(tipo.tipo)
      except OperationalError as error:
        print(f"Error al obtener tipos de obra: {error}")

      # Cantidad de obras que se encuentran en cada etapa
      try:
        etapas = Obra.select(Etapa.etapa.alias('etapa_nombre'), fn.COUNT(Obra.id).alias('etapa_cantidad')).join(Etapa, on=(Obra.etapa == Etapa.id)).group_by(Etapa.etapa)
        for etapa in etapas:
          indicadores['obras_por_etapa'][etapa.etapa.etapa_nombre] = etapa.etapa_cantidad
      except OperationalError as error:
        print(f"Error al obtener obras por etapa: {error}")

      # Cantidad de obras y monto total de inversión por tipo de obra
      try:
        inversiones_por_tipo = Obra.select(
          Tipo.tipo.alias('tipo_nombre'),
          fn.COUNT(Obra.id).alias('cantidad'),
          fn.SUM(Obra.monto_contrato).alias('total_inversion')
        ).join(Tipo, on=(Obra.tipo == Tipo.id)).group_by(Obra.tipo)
        for tipo in inversiones_por_tipo:
          indicadores['inversion_y_cantidad_por_tipo'][tipo.tipo.tipo_nombre] = {
            'cantidad': tipo.cantidad,
            'inversion_total': tipo.total_inversion
          }
      except OperationalError as error:
        print(f"Error al obtener inversiones por tipo de obra: {error}")

      # Listado de todos los barrios pertenecientes a las comunas 1, 2 y 3
      try:
        comunas = self.barrios_comunas[self.barrios_comunas['comuna'].isin([1, 2, 3])]
        indicadores['barrios_por_comuna'] = {
          comuna: grupo['barrio'].dropna().unique().tolist()
          for comuna, grupo in comunas.groupby('comuna')
        }
      except OperationalError as error:
        print(f"Error al obtener barrios en comunas específicas: {error}")

      # Cantidad de obras finalizadas y su monto total de inversión en la comuna 1
      pass

      # Cantidad de obras finalizadas en un plazo menor o igual a 24 meses
      try:
        obras_24_meses = Obra.select().where((Obra.etapa == 3) & (Obra.plazo_meses <= 24)).count()
        indicadores['obras_finalizadas_24_meses'] = obras_24_meses
      except OperationalError as error:
        print(f"Error al obtener obras finalizadas en 24 meses o menos: {error}")

      # Porcentaje total de obras finalizadas
      try:
        total_obras = Obra.select().count()
        obras_finalizadas = Obra.select().where(Obra.etapa == 3).count()
        porcentaje_finalizadas = (obras_finalizadas / total_obras) * 100 if total_obras > 0 else 0
        indicadores['porcentaje_obras_finalizadas'] = porcentaje_finalizadas
      except OperationalError as error:
        print(f"Error al calcular porcentaje de obras finalizadas: {error}")

      # Cantidad total de mano de obra empleada
      try:
        total_mano_obra = Obra.select(fn.SUM(Obra.mano_obra)).scalar() or 0
        indicadores['total_mano_obra'] = total_mano_obra
      except OperationalError as error:
        print(f"Error al obtener cantidad total de mano de obra empleada: {error}")

      # Monto total de inversión
      try:
        monto_total_inversion = Obra.select(fn.SUM(Obra.monto_contrato)).scalar() or 0
        indicadores['monto_total_inversion'] = monto_total_inversion
      except OperationalError as error:
        print(f"Error al obtener monto total de inversión: {error}")

      print('Indicadores obtenidos con éxito')
      return indicadores

    except Exception as error:
      print('Error al obtener indicadores:', error)
      return {}