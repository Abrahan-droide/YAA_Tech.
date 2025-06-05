import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class InterfazTamales:
    def __init__(self):
        # Datos del negocio
        self.ingredientes = {
            "masa_harina": {"stock": 10, "precio": 25, "minimo": 5},
            "carne_res": {"stock": 5, "precio": 130, "minimo": 3},
            "pollo": {"stock": 8, "precio": 85, "minimo": 3},
            "chiles": {"stock": 4, "precio": 18, "minimo": 2},
            "hojas": {"stock": 15, "precio": 35, "minimo": 8},
            "condimentos": {"stock": 3, "precio": 12, "minimo": 1}
        }
        
        self.menu_tamales = {
            "res": {"precio": 16, "costo": 9},
            "pollo": {"precio": 13, "costo": 7},
            "chile": {"precio": 11, "costo": 5}
        }
        
        self.gastos_diarios = {
            "gasolina": 45,
            "gas_cocina": 75,
            "electricidad": 140,
            "agua": 90,
            "empleados": 750
        }
        
        self.registro_ventas = []
        self.hechos_hoy = {"res": 0, "pollo": 0, "chile": 0}
        self.vendidos_hoy = {"res": 0, "pollo": 0, "chile": 0}
        
        # Crear ventana principal
        self.root = tk.Tk()
        self.root.title("Control de Negocio de Tamales")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        self.crear_interfaz()

    def crear_interfaz(self):
        # Título principal
        titulo = tk.Label(self.root, text="🫔 CONTROL DE NEGOCIO DE TAMALES 🫔", 
                         font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        titulo.pack(pady=20)
        
        # Frame para los botones principales
        frame_botones = tk.Frame(self.root, bg='#f0f0f0')
        frame_botones.pack(pady=20)
        
        # Botones principales
        botones = [
            ("📦 Ver Ingredientes", self.mostrar_ingredientes, '#3498db'),
            ("➕ Comprar Ingredientes", self.comprar_ingredientes, '#2ecc71'),
            ("👨‍🍳 Hacer Tamales", self.hacer_tamales, '#e74c3c'),
            ("💰 Registrar Venta", self.registrar_venta, '#f39c12'),
            ("📊 Ver Finanzas", self.ver_finanzas, '#9b59b6'),
            ("📋 Reporte del Día", self.reporte_dia, '#1abc9c')
        ]
        
        for i, (texto, comando, color) in enumerate(botones):
            btn = tk.Button(frame_botones, text=texto, command=comando,
                           font=('Arial', 11, 'bold'), bg=color, fg='white',
                           width=20, height=2, relief='raised', bd=2)
            btn.grid(row=i//2, column=i%2, padx=10, pady=5)
        
        # Área de texto para mostrar información
        self.texto_info = tk.Text(self.root, height=20, width=90, 
                                 font=('Courier', 10), bg='white', 
                                 relief='sunken', bd=2)
        self.texto_info.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Scrollbar para el área de texto
        scrollbar = tk.Scrollbar(self.texto_info)
        scrollbar.pack(side='right', fill='y')
        self.texto_info.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.texto_info.yview)
        
        # Mensaje de bienvenida
        self.mostrar_texto("¡Bienvenido al Sistema de Control de Tamales!\n" +
                          "Selecciona una opción del menú para comenzar.\n" +
                          "="*60 + "\n")

    def mostrar_texto(self, texto):
        self.texto_info.delete(1.0, tk.END)
        self.texto_info.insert(tk.END, texto)

    def agregar_texto(self, texto):
        self.texto_info.insert(tk.END, texto)
        self.texto_info.see(tk.END)

    def mostrar_ingredientes(self):
        texto = "\n📦 INGREDIENTES DISPONIBLES\n"
        texto += "="*50 + "\n\n"
        
        for ingrediente, info in self.ingredientes.items():
            nombre = ingrediente.replace("_", " ").title()
            texto += f"{nombre}:\n"
            texto += f"  Stock: {info['stock']} kg\n"
            texto += f"  Precio: ${info['precio']} por kg\n"
            
            if info['stock'] <= info['minimo']:
                texto += f"  ⚠️ ¡STOCK BAJO! (Mínimo: {info['minimo']} kg)\n"
            texto += "\n"
        
        # Mostrar alertas
        texto += "\n🚨 ALERTAS DE STOCK:\n"
        texto += "-"*30 + "\n"
        hay_alertas = False
        for ingrediente, info in self.ingredientes.items():
            if info['stock'] <= info['minimo']:
                nombre = ingrediente.replace("_", " ").title()
                texto += f"• {nombre}: Solo {info['stock']} kg (Mínimo: {info['minimo']})\n"
                hay_alertas = True
        
        if not hay_alertas:
            texto += "✅ Todos los ingredientes tienen stock suficiente\n"
        
        self.mostrar_texto(texto)

    def comprar_ingredientes(self):
        # Crear ventana para comprar ingredientes
        ventana = tk.Toplevel(self.root)
        ventana.title("Comprar Ingredientes")
        ventana.geometry("400x300")
        ventana.configure(bg='#f0f0f0')
        
        tk.Label(ventana, text="🛒 COMPRAR INGREDIENTES", 
                font=('Arial', 14, 'bold'), bg='#f0f0f0').pack(pady=10)
        
        # Lista de ingredientes
        tk.Label(ventana, text="Selecciona el ingrediente:", 
                font=('Arial', 10), bg='#f0f0f0').pack(pady=5)
        
        ingrediente_var = tk.StringVar()
        combo_ingredientes = ttk.Combobox(ventana, textvariable=ingrediente_var,
                                         values=list(self.ingredientes.keys()),
                                         width=20)
        combo_ingredientes.pack(pady=5)
        
        # Cantidad
        tk.Label(ventana, text="Cantidad (kg):", 
                font=('Arial', 10), bg='#f0f0f0').pack(pady=5)
        
        cantidad_var = tk.StringVar()
        entry_cantidad = tk.Entry(ventana, textvariable=cantidad_var, width=15)
        entry_cantidad.pack(pady=5)
        
        def confirmar_compra():
            try:
                ingrediente = ingrediente_var.get()
                cantidad = float(cantidad_var.get())
                
                if ingrediente in self.ingredientes and cantidad > 0:
                    self.ingredientes[ingrediente]["stock"] += cantidad
                    messagebox.showinfo("✅ Compra Exitosa", 
                                      f"Se agregaron {cantidad} kg de {ingrediente.replace('_', ' ')}")
                    ventana.destroy()
                    self.mostrar_ingredientes()  # Actualizar vista
                else:
                    messagebox.showerror("Error", "Datos inválidos")
            except:
                messagebox.showerror("Error", "Ingresa una cantidad válida")
        
        tk.Button(ventana, text="Confirmar Compra", command=confirmar_compra,
                 bg='#2ecc71', fg='white', font=('Arial', 10, 'bold')).pack(pady=20)

    def hacer_tamales(self):
        # Crear ventana para producir tamales
        ventana = tk.Toplevel(self.root)
        ventana.title("Hacer Tamales")
        ventana.geometry("400x300")
        ventana.configure(bg='#f0f0f0')
        
        tk.Label(ventana, text="👨‍🍳 PRODUCIR TAMALES", 
                font=('Arial', 14, 'bold'), bg='#f0f0f0').pack(pady=10)
        
        # Tipo de tamal
        tk.Label(ventana, text="Tipo de tamal:", 
                font=('Arial', 10), bg='#f0f0f0').pack(pady=5)
        
        tipo_var = tk.StringVar()
        combo_tipos = ttk.Combobox(ventana, textvariable=tipo_var,
                                  values=list(self.menu_tamales.keys()),
                                  width=20)
        combo_tipos.pack(pady=5)
        
        # Cantidad
        tk.Label(ventana, text="Cantidad a producir:", 
                font=('Arial', 10), bg='#f0f0f0').pack(pady=5)
        
        cantidad_var = tk.StringVar()
        entry_cantidad = tk.Entry(ventana, textvariable=cantidad_var, width=15)
        entry_cantidad.pack(pady=5)
        
        def confirmar_produccion():
            try:
                tipo = tipo_var.get()
                cantidad = int(cantidad_var.get())
                
                if tipo in self.menu_tamales and cantidad > 0:
                    if self.verificar_ingredientes_suficientes(tipo, cantidad):
                        self.usar_ingredientes(tipo, cantidad)
                        self.hechos_hoy[tipo] += cantidad
                        messagebox.showinfo("✅ Producción Exitosa", 
                                          f"Se produjeron {cantidad} tamales de {tipo}")
                        ventana.destroy()
                        self.actualizar_produccion()
                    else:
                        messagebox.showerror("❌ Error", "No hay suficientes ingredientes")
                else:
                    messagebox.showerror("Error", "Datos inválidos")
            except:
                messagebox.showerror("Error", "Ingresa una cantidad válida")
        
        tk.Button(ventana, text="Producir Tamales", command=confirmar_produccion,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold')).pack(pady=20)

    def registrar_venta(self):
        # Crear ventana para registrar ventas
        ventana = tk.Toplevel(self.root)
        ventana.title("Registrar Venta")
        ventana.geometry("400x350")
        ventana.configure(bg='#f0f0f0')
        
        tk.Label(ventana, text="💰 REGISTRAR VENTA", 
                font=('Arial', 14, 'bold'), bg='#f0f0f0').pack(pady=10)
        
        # Mostrar disponibles
        texto_disponibles = "Tamales disponibles:\n"
        for tipo in self.menu_tamales.keys():
            disponibles = self.hechos_hoy[tipo] - self.vendidos_hoy[tipo]
            precio = self.menu_tamales[tipo]["precio"]
            texto_disponibles += f"• {tipo.title()}: {disponibles} (${precio} c/u)\n"
        
        tk.Label(ventana, text=texto_disponibles, 
                font=('Arial', 9), bg='#f0f0f0', justify='left').pack(pady=10)
        
        # Tipo de tamal
        tk.Label(ventana, text="Tipo vendido:", 
                font=('Arial', 10), bg='#f0f0f0').pack(pady=5)
        
        tipo_var = tk.StringVar()
        combo_tipos = ttk.Combobox(ventana, textvariable=tipo_var,
                                  values=list(self.menu_tamales.keys()),
                                  width=20)
        combo_tipos.pack(pady=5)
        
        # Cantidad
        tk.Label(ventana, text="Cantidad vendida:", 
                font=('Arial', 10), bg='#f0f0f0').pack(pady=5)
        
        cantidad_var = tk.StringVar()
        entry_cantidad = tk.Entry(ventana, textvariable=cantidad_var, width=15)
        entry_cantidad.pack(pady=5)
        
        def confirmar_venta():
            try:
                tipo = tipo_var.get()
                cantidad = int(cantidad_var.get())
                
                disponibles = self.hechos_hoy[tipo] - self.vendidos_hoy[tipo]
                
                if tipo in self.menu_tamales and cantidad > 0 and cantidad <= disponibles:
                    self.vendidos_hoy[tipo] += cantidad
                    precio_total = cantidad * self.menu_tamales[tipo]["precio"]
                    
                    venta = {
                        "tipo": tipo,
                        "cantidad": cantidad,
                        "precio_total": precio_total,
                        "hora": datetime.now().strftime("%H:%M")
                    }
                    self.registro_ventas.append(venta)
                    
                    messagebox.showinfo("✅ Venta Registrada", 
                                      f"Vendidos: {cantidad} tamales de {tipo}\nTotal: ${precio_total}")
                    ventana.destroy()
                else:
                    messagebox.showerror("❌ Error", f"Solo tienes {disponibles} tamales disponibles")
            except:
                messagebox.showerror("Error", "Ingresa datos válidos")
        
        tk.Button(ventana, text="Registrar Venta", command=confirmar_venta,
                 bg='#f39c12', fg='white', font=('Arial', 10, 'bold')).pack(pady=20)

    def ver_finanzas(self):
        # Calcular finanzas
        ingresos_totales = sum(venta["precio_total"] for venta in self.registro_ventas)
        
        costos_produccion = 0
        for tipo, cantidad in self.vendidos_hoy.items():
            costo_por_tamal = self.menu_tamales[tipo]["costo"]
            costos_produccion += cantidad * costo_por_tamal
        
        gastos_fijos = sum(self.gastos_diarios.values())
        ganancia = ingresos_totales - costos_produccion - gastos_fijos
        
        texto = "\n💰 ANÁLISIS FINANCIERO DEL DÍA\n"
        texto += "="*50 + "\n\n"
        texto += f"💵 Ingresos por ventas: ${ingresos_totales:,.2f}\n"
        texto += f"🏭 Costos de producción: ${costos_produccion:,.2f}\n"
        texto += f"🏢 Gastos fijos del negocio: ${gastos_fijos:,.2f}\n"
        texto += "-"*30 + "\n"
        
        if ganancia > 0:
            texto += f"✅ GANANCIA DEL DÍA: ${ganancia:,.2f}\n"
            texto += "¡Excelente! El negocio fue rentable hoy.\n"
        else:
            texto += f"❌ PÉRDIDA DEL DÍA: ${abs(ganancia):,.2f}\n"
            texto += "Día difícil, hay que revisar costos.\n"
        
        texto += "\n📊 DESGLOSE DE GASTOS FIJOS:\n"
        texto += "-"*30 + "\n"
        for gasto, monto in self.gastos_diarios.items():
            texto += f"• {gasto.replace('_', ' ').title()}: ${monto}\n"
        
        self.mostrar_texto(texto)

    def reporte_dia(self):
        texto = "\n📋 REPORTE COMPLETO DEL DÍA\n"
        texto += "="*50 + "\n"
        
        # Producción
        texto += "\n👨‍🍳 TAMALES PRODUCIDOS:\n"
        texto += "-"*25 + "\n"
        total_producidos = 0
        for tipo, cantidad in self.hechos_hoy.items():
            if cantidad > 0:
                texto += f"• {tipo.title()}: {cantidad} tamales\n"
                total_producidos += cantidad
        texto += f"TOTAL PRODUCIDO: {total_producidos} tamales\n"
        
        # Ventas
        texto += "\n💰 TAMALES VENDIDOS:\n"
        texto += "-"*25 + "\n"
        total_vendidos = 0
        ingresos = 0
        for tipo, cantidad in self.vendidos_hoy.items():
            if cantidad > 0:
                precio_unitario = self.menu_tamales[tipo]["precio"]
                subtotal = cantidad * precio_unitario
                texto += f"• {tipo.title()}: {cantidad} tamales (${subtotal})\n"
                total_vendidos += cantidad
                ingresos += subtotal
        texto += f"TOTAL VENDIDO: {total_vendidos} tamales\n"
        texto += f"INGRESOS: ${ingresos}\n"
        
        # Inventario restante
        texto += "\n📦 TAMALES RESTANTES:\n"
        texto += "-"*25 + "\n"
        total_restantes = 0
        for tipo in self.hechos_hoy.keys():
            restantes = self.hechos_hoy[tipo] - self.vendidos_hoy[tipo]
            if restantes > 0:
                texto += f"• {tipo.title()}: {restantes} tamales\n"
                total_restantes += restantes
        texto += f"TOTAL RESTANTE: {total_restantes} tamales\n"
        
        # Resumen financiero
        costos = sum(self.vendidos_hoy[tipo] * self.menu_tamales[tipo]["costo"] 
                    for tipo in self.vendidos_hoy.keys())
        gastos = sum(self.gastos_diarios.values())
        ganancia = ingresos - costos - gastos
        
        texto += "\n💼 RESUMEN FINANCIERO:\n"
        texto += "-"*25 + "\n"
        texto += f"• Ingresos: ${ingresos}\n"
        texto += f"• Costos: ${costos}\n"
        texto += f"• Gastos: ${gastos}\n"
        texto += f"• Ganancia/Pérdida: ${ganancia}\n"
        
        self.mostrar_texto(texto)

    def verificar_ingredientes_suficientes(self, tipo, cantidad):
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
            total_necesario = por_tamal * cantidad
            if self.ingredientes[ingrediente]["stock"] < total_necesario:
                return False
        return True

    def usar_ingredientes(self, tipo, cantidad):
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

    def actualizar_produccion(self):
        texto = "\n👨‍🍳 ESTADO DE PRODUCCIÓN ACTUALIZADO\n"
        texto += "="*40 + "\n\n"
        
        for tipo, cantidad in self.hechos_hoy.items():
            if cantidad > 0:
                vendidos = self.vendidos_hoy[tipo]
                disponibles = cantidad - vendidos
                texto += f"{tipo.title()}:\n"
                texto += f"  Producidos: {cantidad}\n"
                texto += f"  Vendidos: {vendidos}\n"
                texto += f"  Disponibles: {disponibles}\n\n"
        
        self.mostrar_texto(texto)

    def ejecutar(self):
        self.root.mainloop()

# Iniciar la aplicación
if __name__ == "__main__":
    app = InterfazTamales()
    app.ejecutar()
