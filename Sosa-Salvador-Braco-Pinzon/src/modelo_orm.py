from peewee import *

db = SqliteDatabase(
  'db/obras_urbanas.db',
  pragmas={'journal_mode': 'wal'}
)

class BaseModel(Model):
  class Meta:
    database = db

class Obra(BaseModel):
  def nuevo_proyecto(self):
    pass

  def iniciar_contratacion(self):
    pass
  
  def adjudicar_obra(self):
    pass
  
  def iniciar_obra(self):
    pass
  
  def actualizar_porcentaje_avance(self):
    pass
  
  def incrementar_plazo(self):
    pass
  
  def incrementar_mano_obra(self):
    pass
  
  def finalizar_obra(self):
    pass
  
  def rescindir_obra(self):
    pass