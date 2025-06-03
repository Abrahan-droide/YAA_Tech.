import json
import os
from datetime import datetime

class ControlTamales:
    def __init__(self):
        # Stock de ingredientes disponibles
        self.ingredientes = {
            "masa_harina": {"stock": 0, "precio": 25, "minimo": 5},
            "carne_res": {"stock": 0, "precio": 130, "minimo": 3},
            "pollo": {"stock": 0, "precio": 85, "minimo": 3},
            "chiles": {"stock": 0, "precio": 18, "minimo": 2},
            "hojas": {"stock": 0, "precio": 35, "minimo": 8},
            "condimentos": {"stock": 0, "precio": 12, "minimo": 1}
        }
        
        # Diferentes tipos de tamales y sus precios
        self.menu_tamales = {
            "res": {"precio": 16, "costo": 9},
            "pollo": {"precio": 13, "costo": 7},
            "chile": {"precio": 11, "costo": 5}
        }
        
        # Gastos del negocio
        self.gastos_diarios = {
            "gasolina": 45,
            "gas_cocina": 75,
            "electricidad": 140,
            "agua": 90,
            "empleados": 750
        }
        
        # Registro de lo que pasa cada día
        self.registro_ventas = []
        self.hechos_hoy = {"res": 0, "pollo": 0, "chile": 0}
        self.vendidos_hoy = {"res": 0, "pollo": 0, "chile": 0}

    def menu_principal(self):
        print("\n" + "-"*45)
        print("    CONTROL DE NEGOCIO DE TAMALES")
        print("-"*45)
        print("1. Ver y manejar ingredientes")
        print("2. Hacer tamales")
        print("3. Registrar ventas")
        print("4. Ver números del negocio")
        print("5. Reporte del día")
        print("6. Guardar información")
        print("7. Cerrar programa")
        print("-"*45)

    def manejar_ingredientes(self):
        while True:
            print("\n--- INGREDIENTES ---")
            print("1. Ver lo que tengo")
            print("2. Comprar más ingredientes")
            print("3. Ver qué se está acabando")
            print("4. Regresar")
            
            que_hacer = input("\n¿Qué quieres hacer? ")
            
            if que_hacer == "1":
                self.ver_ingredientes()
            elif que_hacer == "2":
                self.comprar_ingredientes()
            elif que_hacer == "3":
                self.revisar_faltantes()
            elif que_hacer == "4":
                break
            else:
                print("Opción no válida")

    def ver_ingredientes(self):
        print("\n--- QUÉ TENGO EN STOCK ---")
        for ingrediente, info in self.ingredientes.items():
            nombre = ingrediente.replace("_", " ").title()
            print(f"{nombre}: {info['stock']} kg")
            print(f"  Cuesta: ${info['precio']} por kg")
            print()

    def comprar_ingredientes(self):
        print("\n--- COMPRAR INGREDIENTES ---")
        for i, ingrediente in enumerate(self.ingredientes.keys(), 1):
            nombre = ingrediente.replace("_", " ").title()
            print(f"{i}. {nombre}")
        
        try:
            elegir = int(input("\n¿Cuál ingrediente? ")) - 1
            ingrediente_elegido = list(self.ingredientes.keys())[elegir]
            cuanto = float(input(f"¿Cuántos kg de {ingrediente_elegido.replace('_', ' ')}? "))
            
            self.ingredientes[ingrediente_elegido]["stock"] += cuanto
            print(f"Listo! Agregué {cuanto} kg de {ingrediente_elegido.replace('_', ' ')}")
        except:
            print("Error: revisa los números que pusiste")

    def revisar_faltantes(self):
        print("\n--- INGREDIENTES QUE SE ESTÁN ACABANDO ---")
        hay_faltantes = False
        for ingrediente, info in self.ingredientes.items():
            if info["stock"] <= info["minimo"]:
                nombre = ingrediente.replace("_", " ").title()
                print(f"¡CUIDADO! {nombre}: solo quedan {info['stock']} kg (mínimo: {info['minimo']})")
                hay_faltantes = True
        
        if not hay_faltantes:
            print("Todo bien, hay suficientes ingredientes")

    def hacer_tamales(self):
        print("\n--- PRODUCCIÓN DE TAMALES ---")
        print("¿Qué tipo de tamales vas a hacer?")
        for i, tipo in enumerate(self.menu_tamales.keys(), 1):
            print(f"{i}. Tamales de {tipo}")
        
        try:
            elegir = int(input("\nElige el tipo: ")) - 1
            tipo_elegido = list(self.menu_tamales.keys())[elegir]
            cantidad = int(input(f"¿Cuántos tamales de {tipo_elegido}? "))
            
            # Verificar si hay suficientes ingredientes
            if self.verificar_ingredientes_suficientes(tipo_elegido, cantidad):
                self.usar_ingredientes(tipo_elegido, cantidad)
                self.hechos_hoy[tipo_elegido] += cantidad
                print(f"¡Perfecto! Hiciste {cantidad} tamales de {tipo_elegido}")
            else:
                print("No hay suficientes ingredientes")
                
        except:
            print("Error en los datos")

    def verificar_ingredientes_suficientes(self, tipo, cantidad):
        # Ingredientes básicos que necesita cada tamal
        necesarios = {
            "masa_harina": 0.1,  # 100g por tamal
            "hojas": 0.02,       # 20g por tamal
            "condimentos": 0.01   # 10g por tamal
        }
        
        # Ingredientes específicos según el tipo
        if tipo == "res":
            necesarios["carne_res"] = 0.08
        elif tipo == "pollo":
            necesarios["pollo"] = 0.08
        elif tipo == "chile":
            necesarios["chiles"] = 0.06
        
        # Revisar si hay suficiente de cada ingrediente
        for ingrediente, por_tamal in necesarios.items():
            total_necesario = por_tamal * cantidad
            if self.ingredientes[ingrediente]["stock"] < total_necesario:
                print(f"Falta {ingrediente.replace('_', ' ')}")
                return False
        return True

    def usar_ingredientes(self, tipo, cantidad):
        # Descontar ingredientes usados
        necesarios = {
            "masa_harina": 0.1,
            "hojas": 0.02,
            "condimentos": 0.01
        }
        
        if tipo == "res":
            necesarios["carne_res"] = 0.08
        elif tipo == "pollo":
            necesarios["pollo"] = 0.08
        elif tipo == "chile":
            necesarios["chiles"] = 0.06
        
        for ingrediente, por_tamal in necesarios.items():
            usado = por_tamal * cantidad
            self.ingredientes[ingrediente]["stock"] -= usado

    def registrar_ventas(self):
        print("\n--- REGISTRAR VENTAS ---")
        print("¿Qué vendiste?")
        for i, tipo in enumerate(self.menu_tamales.keys(), 1):
            precio = self.menu_tamales[tipo]["precio"]
            print(f"{i}. Tamales de {tipo} - ${precio} c/u")
        
        try:
            elegir = int(input("\nTipo vendido: ")) - 1
            tipo_vendido = list(self.menu_tamales.keys())[elegir]
            cuantos = int(input("¿Cuántos vendiste? "))
            
            if cuantos <= (self.hechos_hoy[tipo_vendido] - self.vendidos_hoy[tipo_vendido]):
                self.vendidos_hoy[tipo_vendido] += cuantos
                precio_total = cuantos * self.menu_tamales[tipo_vendido]["precio"]
                
                # Guardar la venta
                venta = {
                    "tipo": tipo_vendido,
                    "cantidad": cuantos,
                    "precio_total": precio_total,
                    "hora": datetime.now().strftime("%H:%M")
                }
                self.registro_ventas.append(venta)
                
                print(f"Venta registrada: {cuantos} tamales de {tipo_vendido}")
                print(f"Total: ${precio_total}")
            else:
                disponibles = self.hechos_hoy[tipo_vendido] - self.vendidos_hoy[tipo_vendido]
                print(f"Solo tienes {disponibles} tamales de {tipo_vendido} disponibles")
                
        except:
            print("Error en los datos")

    def calcular_finanzas(self):
        print("\n--- NÚMEROS DEL NEGOCIO ---")
        
        # Calcular ingresos del día
        ingresos_totales = 0
        for venta in self.registro_ventas:
            ingresos_totales += venta["precio_total"]
        
        # Calcular costos de producción
        costos_produccion = 0
        for tipo, cantidad in self.vendidos_hoy.items():
            costo_por_tamal = self.menu_tamales[tipo]["costo"]
            costos_produccion += cantidad * costo_por_tamal
        
        # Gastos fijos del día
        gastos_fijos = sum(self.gastos_diarios.values())
        
        # Ganancia neta
        ganancia = ingresos_totales - costos_produccion - gastos_fijos
        
        print(f"Dinero que entró: ${ingresos_totales}")
        print(f"Costo de hacer tamales: ${costos_produccion}")
        print(f"Gastos del negocio: ${gastos_fijos}")
        print(f"Ganancia del día: ${ganancia}")
        
        if ganancia > 0:
            print("¡Buen día! Hubo ganancias")
        else:
            print("Día difícil, hay pérdidas")

    def reporte_del_dia(self):
        print("\n" + "="*40)
        print("         REPORTE DEL DÍA")
        print("="*40)
        
        print("\nTAMALES HECHOS:")
        total_hechos = 0
        for tipo, cantidad in self.hechos_hoy.items():
            if cantidad > 0:
                print(f"  {tipo.title()}: {cantidad}")
                total_hechos += cantidad
        print(f"Total producidos: {total_hechos}")
        
        print("\nTAMALES VENDIDOS:")
        total_vendidos = 0
        for tipo, cantidad in self.vendidos_hoy.items():
            if cantidad > 0:
                print(f"  {tipo.title()}: {cantidad}")
                total_vendidos += cantidad
        print(f"Total vendidos: {total_vendidos}")
        
        print("\nTAMALES QUE SOBRAN:")
        total_sobran = 0
        for tipo in self.hechos_hoy.keys():
            sobran = self.hechos_hoy[tipo] - self.vendidos_hoy[tipo]
            if sobran > 0:
                print(f"  {tipo.title()}: {sobran}")
                total_sobran += sobran
        print(f"Total que sobran: {total_sobran}")
        
        self.calcular_finanzas()

    def guardar_datos(self):
        datos = {
            "ingredientes": self.ingredientes,
            "hechos_hoy": self.hechos_hoy,
            "vendidos_hoy": self.vendidos_hoy,
            "registro_ventas": self.registro_ventas,
            "fecha": datetime.now().strftime("%Y-%m-%d")
        }
        
        try:
            with open("datos_tamales.json", "w") as archivo:
                json.dump(datos, archivo, indent=2)
            print("Información guardada correctamente")
        except:
            print("Error al guardar los datos")

    def ejecutar(self):
        print("Bienvenido al sistema de tamales")
        
        while True:
            self.menu_principal()
            opcion = input("\nElige una opción: ")
            
            if opcion == "1":
                self.manejar_ingredientes()
            elif opcion == "2":
                self.hacer_tamales()
            elif opcion == "3":
                self.registrar_ventas()
            elif opcion == "4":
                self.calcular_finanzas()
            elif opcion == "5":
                self.reporte_del_dia()
            elif opcion == "6":
                self.guardar_datos()
            elif opcion == "7":
                print("¡Hasta luego!")
                break
            else:
                print("Opción no válida, intenta de nuevo")

# Iniciar el programa
if __name__ == "__main__":
    negocio = ControlTamales()
    negocio.ejecutar()
