from src.gestionar_obras import GestionarObraCSV

def main():
  # Inicializar gestor y conectar base de datos
  gestor = GestionarObraCSV()
  db = gestor.conectar_db()

  # Si la conexión es exitosa, limpiar y cargar información a la base de datos
  if db:
    gestor.mapear_orm()
    datos = gestor.extraer_datos('data/observatorio-de-obras-urbanas.csv')
    datos_limpios = gestor.limpiar_datos(datos)
    print('No hay datos para cargar') if datos_limpios.empty else gestor.cargar_datos(datos_limpios)
  
  # Crear primera instancia y usar métodos.
  obra_nueva_1 = gestor.nueva_obra()
  obra_nueva_1.nuevo_proyecto()
  obra_nueva_1.iniciar_contratacion('Licitación Pública', '482/2025')
  obra_nueva_1.adjudicar_obra('Altote S.A', '5355528/2025')
  obra_nueva_1.iniciar_obra(True, '2024-10-01', '2030-05-31', 'Fuente 22', 35)
  obra_nueva_1.actualizar_porcentaje_avance(70)
  obra_nueva_1.incrementar_plazo(6)
  obra_nueva_1.incrementar_mano_obra(12)
  obra_nueva_1.finalizar_obra()

  # Crear segunda instancia y usar métodos.
  obra_nueva_2 = gestor.nueva_obra()
  obra_nueva_2.nuevo_proyecto()
  obra_nueva_2.iniciar_contratacion('Licitación Privada', '608/2024')
  obra_nueva_2.adjudicar_obra('Pepsico SRL', '5353333/2024')
  obra_nueva_2.iniciar_obra(True, '2025-01-01', '2035-12-31', 'Fuente 11', 59)
  obra_nueva_2.actualizar_porcentaje_avance(10)
  obra_nueva_2.incrementar_plazo(10)
  obra_nueva_2.incrementar_mano_obra(11)
  obra_nueva_2.rescindir_obra()
    
  # Obtener y mostrar indicadores
  indicadores = gestor.obtener_indicadores()
  print(indicadores)

if __name__ == "__main__":
  main()