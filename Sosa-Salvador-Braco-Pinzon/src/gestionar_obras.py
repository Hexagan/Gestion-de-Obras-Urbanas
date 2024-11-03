from abc import ABC, abstractmethod
from .modelo_orm import db
import pandas as pd

class GestionarObra(ABC):
  @abstractmethod
  def extraer_datos(self, archivo: str) -> pd.DataFrame:
    pass
  
  @abstractmethod
  def conectar_db(self):
    pass
  
  # @abstractmethod
  # def mapear_orm(self):
  #   pass
  
  # @abstractmethod
  # def limpiar_datos(self):
  #   pass
  
  # @abstractmethod
  # def cargar_datos(self):
  #   pass
  
  # @abstractmethod
  # def nueva_obra(self):
  #   pass
  
  # @abstractmethod
  # def obtener_indicadores(self):
  #   pass

class GestionarObraCSV(GestionarObra):
  def __str__(self) -> str:
    return 'Gestor de obras iniciado correctamente'

  def extraer_datos(self, archivo: str) -> pd.DataFrame:
    try:
      datos = pd.read_csv(archivo, delimiter=';')
      print('Datos extraídos con éxito')
      return datos
    except Exception as error:
      print(f'Error al extraer datos: {error}')
      return pd.DataFrame()
    
  def conectar_db(self):
    try:
      db.connect()
      print('Base de datos conectada exitosamente')
      return True
    except Exception as error:
      print('Error al conectarse con la base de datos:', error)
      return False