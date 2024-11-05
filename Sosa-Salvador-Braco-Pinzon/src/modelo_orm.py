from peewee import *

db = SqliteDatabase(
  'db/obras_urbanas.db',
  pragmas={'journal_mode': 'wal'}
)

class BaseModel(Model):
  class Meta:
    database = db

class Obra(BaseModel):
  # Definir campos
  nombre = CharField(unique=True)
  tipo = CharField()
  area = CharField()
  barrio = CharField()
  comuna = IntegerField(default=0)
  monto_contrato = DecimalField()
  etapa = CharField(null=True)
  contratacion_tipo = CharField(null=True)
  nro_contratacion = CharField(null=True)
  licitacion_oferta_empresa = CharField(null=True)
  expediente_numero = CharField(null=True)
  destacada = BooleanField(default=False)
  fecha_inicio = DateField(null=True)
  fecha_fin_inicial = DateField(null=True)
  financiamiento = CharField(null=True)
  porcentaje_avance = IntegerField(default=0)
  plazo_meses = IntegerField(default=0)
  mano_obra = IntegerField(default=0)

  # Establecer campos
  def nuevo_proyecto(self):
    self.etapa = 'Proyecto'
    self.save()

  def iniciar_contratacion(self, contratacion_tipo, nro_contratacion):
    self.contratacion_tipo = contratacion_tipo
    self.nro_contratacion = nro_contratacion
    self.save()
  
  def adjudicar_obra(self, licitacion_oferta_empresa, expediente_numero):
    self.licitacion_oferta_empresa = licitacion_oferta_empresa
    self.expediente_numero = expediente_numero
    self.save()
  
  def iniciar_obra(self, destacada, fecha_inicio, fecha_fin_inicial, financiamiento, mano_obra):
    self.destacada = destacada
    self.fecha_inicio = fecha_inicio
    self.fecha_fin_inicial = fecha_fin_inicial
    self.financiamiento = financiamiento
    self.mano_obra = mano_obra
    self.save()
  
  def actualizar_porcentaje_avance(self, porcentaje):
    self.porcentaje_avance = porcentaje
    self.save()
  
  def incrementar_plazo(self, meses):
    self.plazo_meses += meses
    self.save()
  
  def incrementar_mano_obra(self, cantidad):
    self.mano_obra += cantidad
    self.save()
  
  def finalizar_obra(self):
    self.etapa = 'Finalizada'
    self.porcentaje_avance = 100
    self.save()
  
  def rescindir_obra(self):
    self.etapa = 'Rescindida'
    self.save()