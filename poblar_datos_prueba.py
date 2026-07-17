
"""
Script de poblamiento MASIVO de datos de prueba para el Sistema de Alquiler de Vehículos.
"""

import os
import random

from sistema_alquiler_vehiculos import GestorAlquiler, RUTA_BD

random.seed(42)  # Semilla fija para que la corrida sea reproducible

# =========================================================================
# DATOS BASE PARA GENERAR LOS REGISTROS
# =========================================================================

# (marca, modelo, tarifa_min, tarifa_max, extra_min, extra_max, anio_min, anio_max)
CATALOGO_AUTOS = [
    ("Toyota", "Corolla", 30, 40, 4, 4, 2019, 2024),
    ("Kia", "Rio", 25, 32, 4, 4, 2018, 2023),
    ("Chevrolet", "Sail", 24, 30, 4, 4, 2018, 2022),
    ("Hyundai", "Accent", 27, 34, 4, 4, 2019, 2023),
    ("Nissan", "Versa", 26, 33, 4, 4, 2019, 2024),
    ("Mazda", "2", 28, 35, 4, 4, 2020, 2024),
    ("Suzuki", "Swift", 25, 31, 2, 4, 2019, 2023),
    ("Volkswagen", "Gol", 23, 29, 4, 4, 2018, 2022),
    ("Renault", "Logan", 24, 30, 4, 4, 2018, 2023),
    ("Honda", "Civic", 35, 45, 4, 4, 2020, 2024),
    ("Kia", "Picanto", 22, 27, 2, 4, 2019, 2023),
    ("Ford", "Fiesta", 24, 30, 4, 4, 2018, 2022),
]

CATALOGO_CAMIONETAS = [
    ("Chevrolet", "D-Max", 55, 70, 900, 1300, 2019, 2024),
    ("Ford", "Ranger", 58, 75, 1000, 1400, 2020, 2024),
    ("Toyota", "Hilux", 60, 78, 1000, 1500, 2019, 2024),
    ("Nissan", "Frontier", 55, 70, 900, 1300, 2018, 2023),
    ("Mazda", "BT-50", 54, 68, 850, 1250, 2018, 2022),
    ("Great Wall", "Wingle", 48, 60, 800, 1100, 2018, 2022),
    ("JAC", "T8", 50, 65, 900, 1200, 2019, 2023),
    ("Toyota", "Tacoma", 62, 80, 1100, 1600, 2020, 2024),
    ("Ford", "F-150", 68, 85, 1300, 1800, 2020, 2024),
]

CATALOGO_MOTOS = [
    ("Yamaha", "FZ", 12, 17, 150, 150, 2020, 2024),
    ("Honda", "CB190", 11, 16, 190, 190, 2019, 2023),
    ("Suzuki", "GN125", 9, 13, 125, 125, 2018, 2022),
    ("Bajaj", "Pulsar", 13, 18, 200, 200, 2020, 2024),
    ("TVS", "Apache", 13, 18, 160, 160, 2019, 2023),
    ("Honda", "XR150", 14, 19, 150, 150, 2020, 2024),
    ("Yamaha", "YBR125", 10, 14, 125, 125, 2018, 2022),
    ("KTM", "Duke200", 16, 22, 200, 200, 2020, 2024),
    ("Suzuki", "AX100", 8, 12, 100, 100, 2017, 2021),
]

NOMBRES = [
    "Juan", "María", "Carlos", "Ana", "Luis", "Carla", "Pedro", "Sofía", "Diego", "Valentina",
    "Andrés", "Gabriela", "Miguel", "Camila", "Jorge", "Daniela", "Fernando", "Paola", "Ricardo", "Mónica",
    "Javier", "Isabel", "Alberto", "Lucía", "Roberto", "Fernanda", "Manuel", "Verónica", "Eduardo", "Cristina",
    "Alexander", "Karina", "Sebastián", "Priscila", "Marco", "Adriana", "David", "Estefanía", "Rafael", "Johanna",
]

APELLIDOS = [
    "Pérez", "López", "Sánchez", "García", "Martínez", "Rodríguez", "Fernández", "Gómez", "Torres", "Vásquez",
    "Ramírez", "Flores", "Castro", "Ortiz", "Molina", "Suárez", "Rojas", "Vera", "Chávez", "Mendoza",
    "Herrera", "Jiménez", "Morales", "Reyes", "Cabrera", "Delgado", "Paredes", "Zambrano", "Andrade", "Salazar",
]

PREFIJOS_PLACA = ["GYE", "UIO", "MAN", "CUE", "LOJ", "AMB", "PTV"]

DESCRIPCIONES_MANTENIMIENTO = [
    "Cambio de aceite y filtros",
    "Revisión de frenos",
    "Alineación y balanceo",
    "Cambio de llantas",
    "Revisión del sistema eléctrico",
    "Cambio de batería",
    "Revisión de suspensión",
    "Mantenimiento de aire acondicionado",
    "Cambio de banda de distribución",
]


# =========================================================================
# GENERADORES DE DATOS ÚNICOS
# =========================================================================

def generar_placa(usadas):
    """Genera una placa única con formato PREFIJO-NNNN."""
    while True:
        placa = f"{random.choice(PREFIJOS_PLACA)}-{random.randint(1000, 9999)}"
        if placa not in usadas:
            usadas.add(placa)
            return placa


def generar_cedula(usadas):
    """Genera una cédula única de 10 dígitos (2 dígitos de provincia + 8 dígitos)."""
    while True:
        cedula = f"{random.randint(1, 24):02d}{random.randint(0, 99999999):08d}"
        if cedula not in usadas:
            usadas.add(cedula)
            return cedula


def generar_telefono():
    return f"09{random.randint(10000000, 99999999)}"


def generar_correo(nombre, apellido, usados):
    base = f"{nombre.lower()}.{apellido.lower()}"
    correo = f"{base}@mail.com"
    contador = 1
    while correo in usados:
        contador += 1
        correo = f"{base}{contador}@mail.com"
    usados.add(correo)
    return correo


# =========================================================================
# FASES DE POBLAMIENTO
# =========================================================================

def poblar_vehiculos(g, placas_usadas):
    """Registra vehículos variados de las 3 categorías y devuelve la lista creada."""
    vehiculos_creados = []

    print("\n=== FASE 1: Registrando vehículos ===")

    print(f"-> Registrando {len(CATALOGO_AUTOS)} automóviles...")
    for marca, modelo, t_min, t_max, e_min, e_max, a_min, a_max in CATALOGO_AUTOS:
        placa = generar_placa(placas_usadas)
        anio = random.randint(a_min, a_max)
        tarifa = round(random.uniform(t_min, t_max), 2)
        puertas = random.choice([2, 4]) if e_min != e_max else e_min
        v = g.registrar_vehiculo("Automovil", placa, marca, modelo, anio, tarifa, puertas)
        vehiculos_creados.append(v)

    print(f"-> Registrando {len(CATALOGO_CAMIONETAS)} camionetas...")
    for marca, modelo, t_min, t_max, e_min, e_max, a_min, a_max in CATALOGO_CAMIONETAS:
        placa = generar_placa(placas_usadas)
        anio = random.randint(a_min, a_max)
        tarifa = round(random.uniform(t_min, t_max), 2)
        capacidad = random.randint(e_min, e_max)
        v = g.registrar_vehiculo("Camioneta", placa, marca, modelo, anio, tarifa, capacidad)
        vehiculos_creados.append(v)

    print(f"-> Registrando {len(CATALOGO_MOTOS)} motocicletas...")
    for marca, modelo, t_min, t_max, e_min, e_max, a_min, a_max in CATALOGO_MOTOS:
        placa = generar_placa(placas_usadas)
        anio = random.randint(a_min, a_max)
        tarifa = round(random.uniform(t_min, t_max), 2)
        cilindraje = random.randint(e_min, e_max)
        v = g.registrar_vehiculo("Motocicleta", placa, marca, modelo, anio, tarifa, cilindraje)
        vehiculos_creados.append(v)

    print(f"   Total de vehículos registrados: {len(vehiculos_creados)}")
    return vehiculos_creados


def poblar_clientes(g, cantidad, cedulas_usadas):
    """Registra 'cantidad' clientes con datos únicos y devuelve la lista creada."""
    clientes_creados = []
    correos_usados = set()

    print(f"\n=== FASE 2: Registrando {cantidad} clientes ===")
    for _ in range(cantidad):
        nombre = random.choice(NOMBRES)
        apellido = random.choice(APELLIDOS)
        cedula = generar_cedula(cedulas_usadas)
        telefono = generar_telefono()
        correo = generar_correo(nombre, apellido, correos_usados)
        c = g.registrar_cliente(cedula, f"{nombre} {apellido}", telefono, correo)
        clientes_creados.append(c)

    print(f"   Total de clientes registrados: {len(clientes_creados)}")
    return clientes_creados


def demostrar_ordenamiento_y_busqueda(g, vehiculos_creados, clientes_creados):
    """Ejercita los algoritmos de ordenamiento y búsqueda sobre vehículos y clientes."""

    print("\n=== FASE 3: Ordenamiento y búsqueda ===")

    print("-> Vehículos ordenados por tarifa (Quick Sort) - 5 más baratos:")
    ordenados_qs = g.vehiculos_ordenados_por_tarifa(avanzado=True)
    for v in ordenados_qs[:5]:
        print(f"   {v.placa} ({v.categoria()}) - ${v.tarifa_diaria:.2f}/día")

    print("-> Vehículos ordenados por tarifa (Burbuja) - 5 más caros:")
    ordenados_burbuja = g.vehiculos_ordenados_por_tarifa(avanzado=False)
    for v in ordenados_burbuja[-5:]:
        print(f"   {v.placa} ({v.categoria()}) - ${v.tarifa_diaria:.2f}/día")

    placa_referencia = vehiculos_creados[len(vehiculos_creados) // 2].placa
    encontrado = g.buscar_vehiculo_por_placa_lineal(placa_referencia)
    print(f"-> Búsqueda lineal por placa '{placa_referencia}': "
          f"{'encontrado -> ' + str(encontrado) if encontrado else 'no encontrado'}")

    tarifa_referencia = ordenados_qs[len(ordenados_qs) // 2].tarifa_diaria
    encontrado_bin = g.buscar_vehiculo_por_tarifa_binaria(tarifa_referencia)
    print(f"-> Búsqueda binaria por tarifa ${tarifa_referencia:.2f}: "
          f"{'encontrado -> ' + str(encontrado_bin) if encontrado_bin else 'no encontrado'}")

    print("-> Clientes ordenados por nombre (Burbuja) - primeros 5:")
    clientes_ordenados = g.clientes_ordenados_por_nombre()
    for c in clientes_ordenados[:5]:
        print(f"   {c.nombre} (Cédula: {c.cedula})")

    cedula_referencia = clientes_creados[len(clientes_creados) // 3].cedula
    cliente_encontrado = g.buscar_cliente_por_cedula_lineal(cedula_referencia)
    print(f"-> Búsqueda lineal por cédula '{cedula_referencia}': "
          f"{'encontrado -> ' + str(cliente_encontrado) if cliente_encontrado else 'no encontrado'}")


def demostrar_actualizacion_y_eliminacion(g, vehiculos_creados, clientes_creados,
                                           placas_usadas, cedulas_usadas):
    """Ejercita actualizar_vehiculo, eliminar_vehiculo, actualizar_cliente y eliminar_cliente."""

    print("\n=== FASE 4: Actualización y eliminación (CRUD completo) ===")

    vehiculo_a_actualizar = vehiculos_creados[0]
    tarifa_anterior = vehiculo_a_actualizar.tarifa_diaria
    vehiculo_a_actualizar.tarifa_diaria = round(tarifa_anterior + 5, 2)
    g.actualizar_vehiculo(vehiculo_a_actualizar)
    print(f"-> Vehículo {vehiculo_a_actualizar.placa} actualizado: "
          f"tarifa ${tarifa_anterior:.2f} -> ${vehiculo_a_actualizar.tarifa_diaria:.2f}")

    placa_prueba = generar_placa(placas_usadas)
    vehiculo_prueba = g.registrar_vehiculo("Motocicleta", placa_prueba, "Marca Prueba", "Modelo Prueba",
                                            2020, 10.0, 125)
    g.eliminar_vehiculo(vehiculo_prueba.id)
    print(f"-> Vehículo de prueba {placa_prueba} registrado y eliminado correctamente.")

    cliente_a_actualizar = clientes_creados[0]
    telefono_anterior = cliente_a_actualizar.telefono
    cliente_a_actualizar.telefono = generar_telefono()
    g.actualizar_cliente(cliente_a_actualizar)
    print(f"-> Cliente {cliente_a_actualizar.nombre} actualizado: "
          f"teléfono {telefono_anterior} -> {cliente_a_actualizar.telefono}")

    cedula_prueba = generar_cedula(cedulas_usadas)
    cliente_prueba = g.registrar_cliente(cedula_prueba, "Cliente Prueba", generar_telefono(),
                                          "cliente.prueba@mail.com")
    g.eliminar_cliente(cliente_prueba.id)
    print(f"-> Cliente de prueba (cédula {cedula_prueba}) registrado y eliminado correctamente.")


def simular_alquileres(g, clientes_creados, cantidad_solicitudes):
    """Genera solicitudes de alquiler: algunas se concretan y otras van a la cola de espera."""

    print(f"\n=== FASE 5: Simulando {cantidad_solicitudes} solicitudes de alquiler ===")

    categorias_alquiler = {
        "Automovil": "Automóvil",
        "Camioneta": "Camioneta",
        "Motocicleta": "Motocicleta",
    }
    clientes_solicitantes = random.sample(clientes_creados, cantidad_solicitudes)

    contratos_creados = []
    total_encolados = 0

    for cliente in clientes_solicitantes:
        tipo = random.choice(list(categorias_alquiler.keys()))
        categoria = categorias_alquiler[tipo]
        dias = random.randint(1, 7)
        con_seguro = random.choice([True, False])

        contrato, mensaje = g.solicitar_alquiler(cliente.id, categoria, dias, con_seguro=con_seguro)
        if contrato:
            contratos_creados.append(contrato)
        else:
            total_encolados += 1

    print(f"   Contratos generados de inmediato: {len(contratos_creados)}")
    print(f"   Clientes agregados a la cola de espera: {total_encolados}")
    print(f"   Clientes actualmente en cola de espera: {len(g.cola_espera)}")

    return contratos_creados


def demostrar_finalizacion_y_cola(g, contratos_creados):
    """Finaliza algunos contratos para liberar vehículos y atiende la cola de espera."""

    print("\n=== FASE 6: Finalización de contratos y atención de la cola de espera ===")

    a_finalizar = contratos_creados[:min(6, len(contratos_creados))]
    for contrato in a_finalizar:
        exito = g.finalizar_contrato(contrato.id)
        print(f"-> Contrato #{contrato.id} finalizado: {exito}")

    print(f"-> Clientes en cola antes de atender: {len(g.cola_espera)}")
    atendidos = 0
    for _ in range(15):
        if g.cola_espera.esta_vacia():
            break
        contrato, mensaje = g.atender_siguiente_en_espera()
        print(f"   {mensaje}")
        if contrato:
            atendidos += 1
    print(f"-> Clientes atendidos desde la cola de espera: {atendidos}")
    print(f"-> Clientes que permanecen en cola de espera: {len(g.cola_espera)}")


def demostrar_deshacer_contrato(g):
    """Ejercita la pila LIFO para deshacer el último contrato registrado."""

    print("\n=== FASE 7: Deshacer el último contrato (Pila LIFO) ===")
    contrato, mensaje = g.deshacer_ultimo_contrato()
    print(f"-> {mensaje}")


def poblar_mantenimientos(g, vehiculos_creados):
    """Registra entre 1 y 3 mantenimientos para varios vehículos al azar."""

    print("\n=== FASE 8: Registrando mantenimientos ===")
    vehiculos_con_mantenimiento = random.sample(vehiculos_creados, min(10, len(vehiculos_creados)))

    for vehiculo in vehiculos_con_mantenimiento:
        cantidad = random.randint(1, 3)
        descripciones = random.sample(DESCRIPCIONES_MANTENIMIENTO, cantidad)
        for descripcion in descripciones:
            g.registrar_mantenimiento(vehiculo.id, descripcion)
        print(f"-> {vehiculo.placa}: {cantidad} mantenimiento(s) registrado(s).")

    vehiculo_ejemplo = vehiculos_con_mantenimiento[0]
    historial = g.historial_mantenimiento(vehiculo_ejemplo.id)
    print(f"-> Historial de mantenimiento de {vehiculo_ejemplo.placa}:")
    for registro in historial:
        print(f"   {registro}")


def imprimir_resumen_final(g):
    print("\n=== RESUMEN FINAL ===")
    vehiculos = g.listar_vehiculos()
    clientes = g.listar_clientes()
    contratos = g.listar_contratos()

    disponibles = sum(1 for v in vehiculos if v.disponible)
    activos = sum(1 for c in contratos if c.estado == "Activo")
    finalizados = sum(1 for c in contratos if c.estado == "Finalizado")
    cancelados = sum(1 for c in contratos if c.estado == "Cancelado")

    print(f"Vehículos totales:        {len(vehiculos)} ({disponibles} disponibles)")
    print(f"Clientes totales:         {len(clientes)}")
    print(f"Contratos totales:        {len(contratos)}")
    print(f"   - Activos:             {activos}")
    print(f"   - Finalizados:         {finalizados}")
    print(f"   - Cancelados:          {cancelados}")
    print(f"Clientes en cola espera:  {len(g.cola_espera)}")


# =========================================================================
# FLUJO PRINCIPAL
# =========================================================================

def poblar():
    if os.path.exists(RUTA_BD):
        os.remove(RUTA_BD)                      # Parte de una base de datos limpia (placas y cédulas son únicas)
        print(f"Base de datos anterior eliminada: {RUTA_BD}")

    g = GestorAlquiler()

    placas_usadas = set()
    cedulas_usadas = set()

    vehiculos_creados = poblar_vehiculos(g, placas_usadas)
    clientes_creados = poblar_clientes(g, 70, cedulas_usadas)

    demostrar_ordenamiento_y_busqueda(g, vehiculos_creados, clientes_creados)
    demostrar_actualizacion_y_eliminacion(g, vehiculos_creados, clientes_creados,
                                          placas_usadas, cedulas_usadas)

    contratos_creados = simular_alquileres(g, clientes_creados, cantidad_solicitudes=45)
    demostrar_finalizacion_y_cola(g, contratos_creados)
    demostrar_deshacer_contrato(g)

    poblar_mantenimientos(g, vehiculos_creados)

    imprimir_resumen_final(g)

    g.cerrar()
    print(f"\n¡Base de datos poblada masivamente con éxito! Archivo: {RUTA_BD}")


if __name__ == "__main__":
    poblar()