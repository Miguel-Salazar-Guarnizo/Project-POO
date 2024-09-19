class Planilla:
    def _init_(self, empleados):
        self.empleados = empleados

    def cargar_planilla(self):
        print("Planilla cargada con éxito.")

    def verificar_consistencia_datos(self):
        errores = []
        ids = set()

        for empleado in self.empleados:
            id, nombre, eps, fondo_pensiones = empleado.values()
            if not all([id, nombre, eps, fondo_pensiones]):
                errores.append(f"Faltan datos en el empleado: {empleado}")
            if id in ids:
                errores.append(f"Empleado duplicado con ID: {id}")
            ids.add(id)

        if errores:
            self.notificar_errores_planilla(errores)
            return False
        return True

    def notificar_errores_planilla(self, errores):
        print("Errores encontrados en la planilla:")
        for error in errores:
            print(error)

    def actualizar_datos_planilla(self):
        for empleado in self.empleados:
            for campo, valor in empleado.items():
                if not valor:
                    empleado[campo] = input(f"Por favor, ingrese {campo} para el empleado {empleado['id']}: ")

    def aprobar_planilla(self):
        print("¿Desea aprobar la planilla? (s/n)")
        decision = input().lower()
        if decision == 's':
            print("Planilla aprobada y contabilizada.")
        else:
            print("Planilla rechazada.")

# Ejemplo de uso
empleados = [
    {"id": "123", "nombre": "Juan Pérez", "eps": "Sura", "fondo_pensiones": "Colfondos"},
    {"id": "124", "nombre": "María Gómez", "eps": "", "fondo_pensiones": "Porvenir"}  # Datos faltantes
]

planilla = Planilla(empleados)
planilla.cargar_planilla()

if not planilla.verificar_consistencia_datos():
    planilla.actualizar_datos_planilla()

planilla.aprobar_planilla()


import pandas as pd


class ProcesadorExcel:
    def _init_(self):
        self.df = None

    def cargar_archivo_excel(self, ruta_archivo):
        try:
            self.df = pd.read_excel(ruta_archivo)
            print(f"Archivo {ruta_archivo} cargado con éxito.")
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo en la ruta especificada: {ruta_archivo}")
        except Exception as e:
            print(f"Error al cargar el archivo: {e}")

    def validar_formato_excel(self):
        if self.df is None or self.df.empty:
            print("El archivo está vacío o no se cargó correctamente.")
            return False
        return True

    def mostrar_errores_excel(self):
        if self.df is not None:
            filas_con_errores = self.df[self.df.isnull().any(axis=1)]
            if not filas_con_errores.empty:
                print("Se encontraron errores en las siguientes filas:")
                print(filas_con_errores)
            else:
                print("No se encontraron errores en el archivo.")
        else:
            print("El archivo no se ha cargado correctamente.")

    def leer_archivo_excel(self):
        if self.validar_formato_excel():
            print(f"Número de filas: {len(self.df)}")
            print(f"Número de columnas: {len(self.df.columns)}")
            print("Vista previa de los primeros datos:")
            print(self.df.head())
        else:
            self.mostrar_errores_excel()


# Solicitar ruta del archivo
ruta_archivo = input("Por favor, introduce la ruta del archivo Excel: ")
procesador = ProcesadorExcel()
procesador.cargar_archivo_excel(ruta_archivo)
procesador.leer_archivo_excel()


class OrganizadorDocumentos:
    def _init_(self, documentos):
        self.documentos = documentos
        self.documentos_clasificados = {
            "facturas_venta": [],
            "facturas_compra": [],
            "recibos_nomina": [],
            "extractos_bancarios": [],
            "sin_clasificar": []
        }

    def cargar_documentos(self):
        print("Documentos cargados para clasificación.")

    def clasificar_por_tipo(self):
        for doc in self.documentos:
            if "factura_venta" in doc.lower():
                self.documentos_clasificados["facturas_venta"].append(doc)
            elif "factura_compra" in doc.lower():
                self.documentos_clasificados["facturas_compra"].append(doc)
            elif "recibo_nomina" in doc.lower():
                self.documentos_clasificados["recibos_nomina"].append(doc)
            elif "extracto_bancario" in doc.lower():
                self.documentos_clasificados["extractos_bancarios"].append(doc)
            else:
                self.documentos_clasificados["sin_clasificar"].append(doc)

    def organizar_en_carpetas(self):
        for tipo, docs in self.documentos_clasificados.items():
            print(f"Organizando {len(docs)} documentos en la carpeta '{tipo}'.")

    def mostrar_documentos_clasificados(self):
        for tipo, docs in self.documentos_clasificados.items():
            print(f"{tipo}: {len(docs)} documentos.")
        print(f"Sin clasificar: {len(self.documentos_clasificados['sin_clasificar'])} documentos.")


# Ejemplo de uso
documentos = ["factura_venta_001.pdf", "recibo_nomina_002.pdf", "documento_sin_tipo.docx"]
organizador = OrganizadorDocumentos(documentos)
organizador.cargar_documentos()
organizador.clasificar_por_tipo()
organizador.organizar_en_carpetas()
organizador.mostrar_documentos_clasificados()
