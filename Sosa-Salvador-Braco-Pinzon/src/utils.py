import re
from peewee import DoesNotExist


def limpiar_dato(datos, nombre):
    if nombre == "licitacion_oferta_empresa":
        # Tabla Empresa
        # Eliminar espacios, saltos, caracteres inválidos y convertir en mayúscula
        datos[nombre] = datos[nombre].apply(
            lambda x: (
                re.sub(r"[^\x00-\x7F]+", "", x)
                .strip()
                .replace("\n", "")
                .replace("\r", "")
                .upper()
                if isinstance(x, str) and x not in [None, "", "-"]
                else None
            )
        )

        # Eliminar datos vacios, nulos e incompletos
        incluir = datos[nombre].apply(
            lambda x: isinstance(x, str) and x not in ["", "NA", "-", "."]
        )
        datos = datos[incluir].dropna()

        # Eliminar duplicados
        datos = datos.drop_duplicates(subset=[nombre]).reset_index(drop=True)

        return datos
    else:
        # Tablas Etapa, Tipo, Area, Barrio, Contratacion y Financiamiento
        # Eliminar espacios y convertir en mayúscula
        datos[nombre] = datos[nombre].str.strip().str.upper()

        # Eliminar datos vacios, nulos e incompletos
        incluir = datos[nombre].apply(
            lambda x: isinstance(x, str) and x not in ["", "NA", "-", "."]
        )
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
        # Solicitar valor siempre que sea inválido
        dato = input(texto).strip().upper()

        # Validar si no existe
        if not tabla.select().where(getattr(tabla, campo) == dato).exists():
            print("El valor es inválido. Por favor ingrese un valor válido.")
            continue

        try:
            # Si existe, buscar y retornar el ID
            dato_id = tabla.select().where(getattr(tabla, campo) == dato).get().id
            return dato_id
        except DoesNotExist:
            print("El valor es inválido. Por favor ingrese un valor válido.")
            continue
