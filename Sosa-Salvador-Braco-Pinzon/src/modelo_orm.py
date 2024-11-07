from peewee import *

db = SqliteDatabase(
  'db/obras_urbanas.db',
  pragmas={'journal_mode': 'wal'}
)

class BaseModel(Model):
  class Meta:
    database = db

class Etapa(BaseModel):
  etapa = CharField(unique=True)

class Tipo(BaseModel):
  tipo = CharField(unique=True)

class Area(BaseModel):
  area = CharField(unique=True)

class Barrio(BaseModel):
  barrio = CharField(unique=True)

class Empresa(BaseModel):
  licitacion_oferta_empresa = CharField(unique=True)

class Contratacion(BaseModel):
  contratacion_tipo = CharField(unique=False)

class Financiamiento(BaseModel):
  financiamiento = CharField(unique=False)

class Obra(BaseModel):
  # Definir campos
  nombre = CharField(unique=True)
  tipo = ForeignKeyField(Tipo, backref='obras')
  area = ForeignKeyField(Area, backref='obras')
  barrio = ForeignKeyField(Barrio, backref='obras')
  comuna = IntegerField(default=0)
  monto_contrato = DecimalField(default=0)
  etapa = ForeignKeyField(Etapa, backref='obras')
  contratacion_tipo = ForeignKeyField(Contratacion, backref='obras', null=True)
  nro_contratacion = CharField(unique=False, null=True)
  licitacion_oferta_empresa = ForeignKeyField(Empresa, backref='obras', null=True)
  expediente_numero = CharField(unique=False, null=True)
  destacada = BooleanField(default=False, null=True)
  fecha_inicio = DateField(null=True)
  fecha_fin_inicial = DateField(null=True)
  financiamiento = ForeignKeyField(Financiamiento, backref='obras', null=True)
  porcentaje_avance = IntegerField(default=0, null=True)
  plazo_meses = IntegerField(default=0, null=True)
  mano_obra = IntegerField(default=0, null=True)

  # Establecer campos
  def nuevo_proyecto(self):
    self.etapa = 2
    self.save()

  def iniciar_contratacion(self, contratacion, nro_contratacion):
    self.nro_contratacion = nro_contratacion

    try:
      contratacion_id = Contratacion.get(Contratacion.contratacion_tipo == contratacion.strip().upper()).id
      self.contratacion_tipo = contratacion_id
      self.save()
    except DoesNotExist:
      print('El tipo de contratación no existe.')
  
  def adjudicar_obra(self, empresa, expediente_numero):
    self.expediente_numero = expediente_numero

    try:
      empresa_id = Empresa.get(Empresa.licitacion_oferta_empresa == empresa.strip().upper()).id
      self.licitacion_oferta_empresa = empresa_id
      self.save()
    except DoesNotExist:
      print('La empresa no existe.')
  
  def iniciar_obra(self, destacada, fecha_inicio, fecha_fin_inicial, financiamiento_tipo, mano_obra):
    self.destacada = destacada
    self.fecha_inicio = fecha_inicio
    self.fecha_fin_inicial = fecha_fin_inicial
    self.mano_obra = mano_obra

    try:
      financiamiento_id = Financiamiento.get(Financiamiento.financiamiento == financiamiento_tipo.strip().upper()).id
      self.financiamiento = financiamiento_id
      self.save()
    except DoesNotExist:
      print('El tipo de financiamiento no existe.')
  
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
    self.porcentaje_avance = 100
    self.etapa = 3
    self.save()
  
  def rescindir_obra(self):
    self.etapa = 4
    self.save()