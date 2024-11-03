from src.gestionar_obras import GestionarObraCSV

obra_csv = GestionarObraCSV()
print(obra_csv)
data = obra_csv.extraer_datos('data/observatorio-de-obras-urbanas.csv')
print(data)
obra_csv.conectar_db()