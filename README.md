# Sistema de Alquiler de Vehículos - RentCar

Proyecto desarrollado para la materia de Lenguaje de Programación II, tercer semestre de la carrera de Ingeniería en Ciencias de la Computación, Universidad Agraria del Ecuador.

## Integrantes - Grupo 9

- Figueroa Figueroa Katherine Elizabeth
- Pozo Calderón Henry Xavier
- Prospel Mendoza Jhostin Elian
- Ramírez Lozano Laura del Rocío
- Sacón Rivas Kerly Michelle

## Descripción del proyecto

Este proyecto es un sistema de escritorio para administrar el alquiler de vehículos de una empresa ficticia llamada RentaCar. Permite registrar la flota de vehículos (autos, camionetas y motos), registrar clientes, generar contratos de alquiler, y llevar un control de mantenimiento de cada vehículo.

El objetivo principal del trabajo fue aplicar los temas vistos en clase de estructuras de datos: listas enlazadas, pilas, colas y algoritmos de ordenamiento y búsqueda, integrándolos en un sistema funcional con base de datos e interfaz gráfica.

## Funcionalidades

- Registro, edición, eliminación y consulta de vehículos (automóviles, camionetas y motocicletas)
- Registro, edición, eliminación y consulta de clientes
- Generación de contratos de alquiler, con cálculo de costos distinto según el tipo de vehículo (y opción de seguro)
- Cola de espera: cuando no hay vehículos disponibles de una categoría, el cliente se pone en espera y se atiende automáticamente cuando se libera uno
- Opción para deshacer el último contrato registrado (usando una pila)
- Registro de mantenimientos por vehículo, guardados en una lista enlazada
- Ordenamiento de vehículos por tarifa (implementamos Quick Sort y también Burbuja para comparar)
- Búsqueda de vehículos por placa (lineal) y por tarifa (binaria)

## Tecnologías utilizadas

- Python 3
- CustomTkinter
- SQLite3

## Archivos del proyecto

- `sistema_alquiler_vehiculos.py`: el programa principal, con toda la lógica y la interfaz

## Cómo ejecutarlo

1. Clonar el repositorio:
```
git clone https://github.com/Jhostin-P//sistema-alquiler-vehiculos.git
```

2. Instalar la librería que falta (customtkinter):
```
pip install customtkinter
```

3. Ejecutar el programa:
```
python sistema_alquiler_vehiculos.py
```

