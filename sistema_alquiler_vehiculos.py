"""
 SISTEMA DE ALQUILER DE VEHÍCULOS - GRUPO 9
 Lenguaje de Programación II - Universidad Agraria del Ecuador
 Proyecto Final 

Archivo que integra:
    SECCIÓN 1: Estructuras de Datos      
    SECCIÓN 2: Algoritmos                
    SECCIÓN 3: Modelo de Dominio (POO)  
    SECCIÓN 4: Base de Datos             
    SECCIÓN 5: Gestor del Sistema     
    SECCIÓN 6: Interfaz Gráfica          
"""

import sqlite3                              # Importa la librería para interactuar con bases de datos SQLite
import os                                   # Importa el módulo para interactuar con el sistema operativo
from abc import ABC, abstractmethod         # Importa herramientas para crear clases abstractas y métodos obligatorios
from datetime import date                   # Importa el objeto 'date' para manejar fechas de forma sencilla

# SECCIÓN 1: ESTRUCTURAS DE DATOS LINEALES (implementadas desde cero)
class Nodo:                                 # Define la clase Nodo, la pieza básica de construcción de la lista
    """Nodo básico para la lista enlazada simple."""

    def __init__(self, dato):               # Constructor que inicializa el nodo con un valor específico
        self.dato = dato                    # Guarda el valor o información dentro del nodo
        self.siguiente = None               # Apunta al siguiente nodo

    def __repr__(self):                     # Define cómo se representará el nodo al imprimirlo en consola
        return f"Nodo({self.dato})"         # Retorna un texto descriptivo con el valor del nodo

class ListaEnlazada:                        # Define la estructura de datos de una Lista Enlazada Simple
    """
    Lista Enlazada Simple.
    Se usa para almacenar el HISTORIAL DE MANTENIMIENTO de cada vehículo
    (cada mantenimiento es un nodo encadenado al anterior).
    """

    def __init__(self):                     # Constructor de la lista enlazada
        self.cabeza = None                  # El primer nodo de la lista (inicia vacía, por lo tanto es None)
        self._tamano = 0                    # Lleva la cuenta interna de cuántos elementos hay en la lista

    def esta_vacia(self):                   # Método para saber si la lista no tiene elementos
        return self.cabeza is None          # Retorna True si no hay primer nodo, de lo contrario False

    def agregar_final(self, dato):          # Método para insertar un nodo al final de la lista
        """Inserta un nuevo nodo al final de la lista. O(n)."""

        nuevo = Nodo(dato)                  # Crea un nuevo objeto Nodo con el dato entregado

        if self.esta_vacia():               # Verifica si la lista está completamente vacía
            self.cabeza = nuevo             # Si está vacía, el nuevo nodo se convierte en la cabeza de la lista

        else:                               # Si la lista ya tiene elementos
            actual = self.cabeza            # Se posiciona en el primer nodo para iniciar el recorrido

            while actual.siguiente is not None: # Avanza por la lista mientras el nodo actual apunte a otro nodo
                actual = actual.siguiente   # Mueve el puntero al siguiente nodo de la lista
            actual.siguiente = nuevo        # Conecta el último nodo encontrado con el nuevo nodo creado

        self._tamano += 1                   # Incrementa en 1 el contador del tamaño de la lista

    def agregar_inicio(self, dato):         # Método para insertar un nodo al principio de la lista

        """Inserta un nuevo nodo al inicio de la lista. O(1)."""

        nuevo = Nodo(dato)                  # Crea un nuevo objeto Nodo con el dato entregado
        nuevo.siguiente = self.cabeza       # El nuevo nodo apunta al que antes era el primer nodo
        self.cabeza = nuevo                 # La cabeza de la lista ahora pasa a ser el nuevo nodo
        self._tamano += 1                   # Incrementa en 1 el contador del tamaño de la lista

    def eliminar(self, dato):               # Método para buscar y quitar un elemento de la lista
        """Elimina la primera ocurrencia de 'dato'. O(n)."""

        actual = self.cabeza                # Comienza la búsqueda desde el primer nodo
        anterior = None                     # Guarda el nodo previo para poder reconectar la lista al borrar

        while actual is not None:           # Recorre la lista mientras queden nodos por analizar

            if actual.dato == dato:         # Compara si el dato del nodo actual es el que queremos borrar

                if anterior is None:        # Si es el primer nodo
                    self.cabeza = actual.siguiente # La cabeza ahora será el segundo nodo de la lista

                else:                       # Si el nodo a borrar está en medio o al final de la lista
                    anterior.siguiente = actual.siguiente # El nodo anterior se salta al actual y apunta al siguiente
                self._tamano -= 1           # Decrementa en 1 el contador del tamaño de la lista

                return True                 # Retorna True indicando que el elemento fue encontrado y eliminado
            
            anterior = actual               # El nodo actual pasa a ser el nodo anterior para el próximo ciclo
            actual = actual.siguiente       # Avanza al siguiente nodo de la lista

        return False                        # Retorna False si recorrió toda la lista y no encontró el dato

    def a_lista_python(self):               # Método auxiliar para convertir la lista enlazada a una lista común de Python

        resultado = []                      # Crea una lista vacía de Python para almacenar los elementos
        actual = self.cabeza                # Empieza a recorrer desde el primer nodo

        while actual is not None:           # Recorre la lista hasta llegar al final
            resultado.append(actual.dato)   # Extrae el dato del nodo y lo añade a la lista de Python
            actual = actual.siguiente       # Avanza al siguiente nodo

        return resultado                    # Retorna la lista de Python con todos los datos recolectados

    def __len__(self):                      # Permite usar la función integrada len() de Python sobre esta clase
        return self._tamano                 # Retorna el número de elementos guardado en la variable privada

    def __iter__(self):                     # Hace que la lista sea iterable (permite usarla en bucles 'for')
        actual = self.cabeza                # Empieza el recorrido desde el primer nodo

        while actual is not None:           # Mientras no se llegue al final de la lista
            yield actual.dato               # Devuelve el dato actual pausando la ejecución (generador)
            actual = actual.siguiente       # Avanza al siguiente nodo para la próxima iteración

    def __repr__(self):                     # Define la representación de la lista al imprimirla

        return f"ListaEnlazada({self.a_lista_python()})" # Imprime la lista mostrando su estructura como lista de Python


class Pila:                                 # Define la clase Pila 
    def __init__(self):                     # Constructor de la Pila
        self._lista = ListaEnlazada()       # Utiliza internamente la ListaEnlazada que creamos antes para guardar datos

    def esta_vacia(self):                   # Método para comprobar si la pila no tiene elementos
        return self._lista.esta_vacia()     # Delega la comprobación al método de la lista enlazada

    def apilar(self, dato):                 # Método para meter un elemento en la cima de la pila 
        """Push: agrega un elemento a la cima de la pila. O(1)."""
        self._lista.agregar_inicio(dato)    # Inserta al inicio de la lista enlazada, lo cual toma tiempo constante

    def desapilar(self):                    # Método para sacar y obtener el elemento de la cima 
        """Pop: remueve y retorna el elemento de la cima. O(1)."""

        if self.esta_vacia():               # Comprueba si no hay nada en la pila
            return None                     # Si está vacía, no hay nada que sacar, retorna None
        
        dato = self._lista.cabeza.dato      # Obtiene el dato que está en la cima
        self._lista.cabeza = self._lista.cabeza.siguiente # Mueve la cabeza de la lista al siguiente nodo
        self._lista._tamano -= 1            # Resta 1 al tamaño de la lista interna manualmente

        return dato                         # Retorna el dato que acabamos de remover de la cima

    def ver_cima(self):                     # Método para mirar el elemento de la cima sin quitarlo

        if self.esta_vacia():               # Comprueba si la pila está vacía
            return None                     # Retorna None si no hay elementos
        
        return self._lista.cabeza.dato      # Retorna el valor del primer nodo

    def __len__(self):                      # Permite usar len() sobre la pila
        return len(self._lista)             # Retorna el tamaño llamando a la función len de la lista interna

    def __repr__(self):                     # Define cómo se muestra la pila al imprimirla
        return f"Pila(cima->{self._lista.a_lista_python()})" # Imprime el contenido indicando dónde está la cima


class Cola:                                 # Define la clase Cola
    def __init__(self):                     # Constructor de la Cola
        self.frente = None                  # Puntero al primer elemento que va a salir
        self.final = None                   # Puntero al último elemento que entró
        self._tamano = 0                    # Lleva el conteo manual de los elementos en la cola

    def esta_vacia(self):                   # Método para saber si la cola está vacía
        return self.frente is None          # Si el frente es None, significa que no hay nadie en la cola

    def encolar(self, dato):                # Método para agregar un elemento al final de la cola
        """Agrega un elemento al final de la cola. O(1)."""
        nuevo = Nodo(dato)                  # Crea un nuevo Nodo con el dato proporcionado

        if self.esta_vacia():               # Si la cola está vacía
            self.frente = nuevo             # El nuevo nodo es el primero en la cola
            self.final = nuevo              # Al ser el único, también es el último
            
        else:                               # Si la cola ya contiene elementos
            self.final.siguiente = nuevo    # El nodo que estaba al final ahora apunta al nuevo nodo
            self.final = nuevo              # El puntero de final se actualiza para que sea el nuevo nodo
        self._tamano += 1                   # Incrementa en 1 el contador del tamaño de la cola

    def desencolar(self):                   # Método para retirar y obtener el elemento al frente de la cola
        """Remueve y retorna el elemento al frente de la cola. O(1)."""

        if self.esta_vacia():               # Comprueba si la cola está vacía
            return None                     # Retorna None porque no hay elementos para sacar
        
        dato = self.frente.dato             # Guarda el dato que está en el frente de la cola
        self.frente = self.frente.siguiente # El frente pasa a ser el siguiente nodo en la fila

        if self.frente is None:             # Si al avanzar el frente la cola queda vacía
            self.final = None               # El puntero final también se pone en None
        self._tamano -= 1                   # Resta 1 al tamaño de la cola

        return dato                         # Retorna el dato que sacamos del frente

    def ver_frente(self):                   # Método para observar el primer elemento sin sacarlo
        if self.esta_vacia():               # Comprueba si está vacía
            return None                     # Retorna None si no hay elementos
        return self.frente.dato             # Retorna el valor del nodo en el frente

    def a_lista_python(self):               # Método auxiliar para pasar los elementos de la cola a una lista estándar

        resultado = []                      # Crea una lista de Python vacía
        actual = self.frente                # Comienza a recorrer desde el frente de la cola

        while actual is not None:           # Recorre secuencialmente todos los nodos
            resultado.append(actual.dato)   # Agrega el dato actual a la lista de Python
            actual = actual.siguiente       # Avanza al siguiente nodo

        return resultado                    # Retorna la lista resultante

    def __len__(self):                      # Permite usar len() directamente en la cola
        return self._tamano                 # Retorna el número de elementos acumulado en el tamaño

    def __repr__(self):                     # Define la representación en texto de la cola
        return f"Cola(frente->{self.a_lista_python()})" # Muestra la cola en orden de salida desde el frente

# SECCIÓN 2: ALGORITMOS DE ORDENAMIENTO Y BÚSQUEDA
def ordenamiento_burbuja(lista, clave=lambda x: x): # Algoritmo de ordenación Burbuja. Recibe una lista y una función clave para comparar

    datos = list(lista)                             # Crea una copia de la lista para no modificar la original
    n = len(datos)                                  # Obtiene la cantidad de elementos de la lista

    for i in range(n - 1):                          # Bucle externo: controla cuántas pasadas completas haremos sobre la lista

        intercambio = False                         # Bandera para optimizar: rastrea si hubo algún cambio en esta pasada
        
        for j in range(n - 1 - i):                  # Bucle interno: compara elementos adyacentes reduciendo el rango en cada pasada

            if clave(datos[j]) > clave(datos[j + 1]): # Compara las claves de dos elementos vecinos consecutivos
                datos[j], datos[j + 1] = datos[j + 1], datos[j] # Intercambia las posiciones de los elementos si están desordenados
                intercambio = True                  # Marca que sí se realizó un intercambio en esta pasada

        if not intercambio:                         # Si al terminar la pasada no hubo intercambios, la lista ya está ordenada
            break                                   # Rompe el bucle de manera anticipada para ahorrar tiempo de ejecución

    return datos                                    # Retorna la lista completamente ordenada de menor a mayor


def quick_sort(lista, clave=lambda x: x):           # Algoritmo de ordenación rápida (Divide y Vencerás) de forma recursiva
    datos = list(lista)                             # Crea una copia de la lista en formato estándar

    if len(datos) <= 1:                             # Caso base de la recursión: si tiene 0 o 1 elementos, ya está ordenada
        return datos                                # Retorna directamente la lista sin hacer cambios
    
    pivote = datos[len(datos) // 2]                 # Elige el elemento del medio como punto de comparación (pivote)
    valor_pivote = clave(pivote)                    # Obtiene el valor de la propiedad que vamos a comparar del pivote
    menores = [x for x in datos if clave(x) < valor_pivote] # Filtra en una lista todos los elementos menores al pivote
    iguales = [x for x in datos if clave(x) == valor_pivote] # Filtra en una lista todos los elementos iguales al pivote
    mayores = [x for x in datos if clave(x) > valor_pivote] # Filtra en una lista todos los elementos mayores al pivote

    return quick_sort(menores, clave) + iguales + quick_sort(mayores, clave) # Une de forma ordenada las sublistas procesadas recursivamente


def busqueda_lineal(lista, valor_buscado, clave=lambda x: x): # Algoritmo de búsqueda secuencial elemento por elemento
    """
    Búsqueda LINEAL. Complejidad: O(n). No requiere lista ordenada.
    Retorna (indice, elemento) o (-1, None).
    """
    for i, elemento in enumerate(lista):            # Recorre la lista obteniendo la posición (i) y el valor (elemento)

        if clave(elemento) == valor_buscado:        # Evalúa si la propiedad del elemento actual coincide con lo buscado
            return i, elemento                      # Si coincide, retorna la posición en la lista y el objeto encontrado
        
    return -1, None                                 # Si recorre toda la lista y no encuentra nada, retorna error (-1 y None)


def busqueda_binaria(lista_ordenada, valor_buscado, clave=lambda x: x): # Búsqueda binaria (requiere que la lista esté ordenada de antemano)
    izquierda, derecha = 0, len(lista_ordenada) - 1 # Inicializa los límites de búsqueda en los extremos de la lista

    while izquierda <= derecha:                     # Bucle que se ejecuta mientras el intervalo de búsqueda sea válido
        medio = (izquierda + derecha) // 2          # Calcula la posición de la mitad del intervalo actual
        valor_medio = clave(lista_ordenada[medio])  # Extrae la propiedad de comparación del elemento del medio

        if valor_medio == valor_buscado:            # Si el elemento de en medio es lo que buscamos
            return medio, lista_ordenada[medio]     # Retorna la posición de en medio y el elemento encontrado
        
        elif valor_medio < valor_buscado:           # Si el valor de en medio es más pequeño que el buscado
            izquierda = medio + 1                   # Descarta la mitad izquierda moviendo el límite inferior hacia arriba

        else:                                       # Si el valor de en medio es más grande que el buscado
            derecha = medio - 1                     # Descarta la mitad derecha moviendo el límite superior hacia abajo

    return -1, None                                 # Retorna -1 y None si el intervalo se cierra y no se halló el valor


# SECCIÓN 3: MODELO DE DOMINIO 
class Vehiculo(ABC):                                # Define la clase abstracta base de vehículos usando herencia de ABC
    """Clase abstracta base para todos los vehículos de la flota (abstracción)."""

    def __init__(self, placa, marca, modelo, anio, tarifa_diaria, id_vehiculo=None): # Constructor de la clase base
        self._id = id_vehiculo                      # Almacena el ID del vehículo (procedente de la Base de Datos)
        self._placa = placa                         # Atributo encapsulado para la placa del vehículo
        self._marca = marca                         # Atributo encapsulado para la marca del fabricante
        self._modelo = modelo                       # Atributo encapsulado para el modelo del vehículo
        self._anio = anio                           # Atributo encapsulado para el año de fabricación
        self._tarifa_diaria = tarifa_diaria         # Atributo encapsulado para el costo de alquiler por día
        self._disponible = True                     # Estado por defecto de disponibilidad del vehículo (comienza en libre)
        self.historial_mantenimiento = ListaEnlazada() # Inicializa una lista enlazada propia para guardar mantenimientos

    # ---- Encapsulamiento: getters / setters con @property ----
    @property
    def id(self):                                   # Getter para el atributo id
        return self._id                             # Retorna el valor actual de self._id

    @id.setter
    def id(self, valor):                            # Setter para el atributo id
        self._id = valor                            # Asigna el nuevo valor de ID al objeto

    @property
    def placa(self):                                # Getter para el atributo placa
        return self._placa                          # Retorna el valor actual de self._placa

    @placa.setter
    def placa(self, valor):                         # Setter para el atributo placa con validación integrada

        if not valor or len(valor.strip()) == 0:    # Verifica que el texto ingresado no esté vacío ni lleno de puros espacios
            raise ValueError("La placa no puede estar vacía") # Genera un error si el valor no es válido
        
        self._placa = valor.strip().upper()         # Remueve espacios sobrantes y guarda la placa en mayúsculas

    @property
    def marca(self):                                # Getter para el atributo marca
        return self._marca                          # Retorna el valor de la marca

    @marca.setter
    def marca(self, valor):                         # Setter para la marca del vehículo
        self._marca = valor                         # Actualiza el valor de la marca sin validación extra

    @property
    def modelo(self):                               # Getter para el atributo modelo
        return self._modelo                         # Retorna el modelo registrado

    @modelo.setter
    def modelo(self, valor):                        # Setter para el modelo del vehículo
        self._modelo = valor                        # Actualiza el valor de la marca sin validación extra

    @property
    def anio(self):                                 # Getter para el año del vehículo
        return self._anio                           # Retorna el año registrado

    @anio.setter
    def anio(self, valor):                          # Setter para el año del vehículo
        self._anio = valor                          # Actualiza el año con el nuevo valor provisto

    @property
    def tarifa_diaria(self):                        # Getter para la tarifa de renta por día
        return self._tarifa_diaria                  # Retorna el costo diario del alquiler

    @tarifa_diaria.setter
    def tarifa_diaria(self, valor):                 # Setter para la tarifa diaria con validación financiera

        if valor < 0:                               # Evalúa si el precio ingresado es menor a cero
            raise ValueError("La tarifa diaria no puede ser negativa") # Lanza una excepción si el valor es inválido
        
        self._tarifa_diaria = valor                 # Asigna la tarifa autorizada al atributo protegido

    @property
    def disponible(self):                           # Getter para conocer el estado de renta del auto
        return self._disponible                     # Retorna True si está disponible, False si está rentado

    @disponible.setter
    def disponible(self, valor):                    # Setter para modificar el estado del vehículo
        self._disponible = bool(valor)              # Convierte el valor a tipo de dato booleano y lo asigna

    def agregar_mantenimiento(self, descripcion, fecha=None): # Añade un servicio mecánico a la lista interna del auto
        fecha = fecha or date.today().isoformat()   # Si no se provee fecha, usa el día de hoy formateado como YYYY-MM-DD
        self.historial_mantenimiento.agregar_final((fecha, descripcion)) # Añade una tupla con fecha y descripción al final de la lista enlazada

    @abstractmethod
    def categoria(self):                            # Método abstracto para obligar a las subclases a definir su tipo
        raise NotImplementedError                   # Lanza error indicando que es obligatorio implementarlo en las hijas

    def calcular_costo_alquiler(self, dias):        # Método común de cálculo financiero que puede ser heredado o modificado
        """Método polimórfico base; cada subclase puede sobrescribirlo."""
        return self._tarifa_diaria * dias           # Retorna la multiplicación de días solicitados por el costo diario

    def __str__(self):                              # Devuelve la representación en formato de texto legible del vehículo
        estado = "Disponible" if self._disponible else "Alquilado" # Evalúa si el auto está libre para alquiler o no
        return (f"[{self.categoria()}] {self._marca} {self._modelo} ({self._anio}) " # Construye y retorna la cadena de texto con la información
                f"- Placa: {self._placa} - Tarifa: ${self._tarifa_diaria:.2f}/día - {estado}")


class Automovil(Vehiculo):                          # Clase Automovil que hereda de la clase abstracta Vehiculo
    def __init__(self, placa, marca, modelo, anio, tarifa_diaria, num_puertas=4, id_vehiculo=None): # Constructor de la subclase
        super().__init__(placa, marca, modelo, anio, tarifa_diaria, id_vehiculo) # Inicializa el constructor de la clase padre Vehiculo
        self.num_puertas = num_puertas              # Define un atributo propio y exclusivo para automóviles: el número de puertas

    def categoria(self):                            # Implementación del método abstracto de la clase padre
        return "Automóvil"                          # Retorna su etiqueta identificadora de categoría

    def calcular_costo_alquiler(self, dias, con_seguro=False): # Sobrescribe el cálculo para incluir opciones de seguros
        """Sobrecarga vía parámetro por defecto: costo con o sin seguro (+10%)."""
        costo = super().calcular_costo_alquiler(dias) # Llama al cálculo de tarifa estándar de la clase padre

        if con_seguro:                              # Si se solicita activar la cobertura de seguro
            costo *= 1.10                           # Añade un 10% de recargo al valor de alquiler calculado

        return costo                                # Retorna el costo final ajustado


class Camioneta(Vehiculo):                          # Clase Camioneta que hereda de la clase abstracta Vehiculo
    def __init__(self, placa, marca, modelo, anio, tarifa_diaria, capacidad_carga_kg=0, id_vehiculo=None): # Constructor
        super().__init__(placa, marca, modelo, anio, tarifa_diaria, id_vehiculo) # Llama al constructor de la clase base
        self.capacidad_carga_kg = capacidad_carga_kg # Atributo exclusivo para camionetas: la capacidad de carga útil

    def categoria(self):                            # Implementación del método abstracto de la clase padre
        return "Camioneta"                          # Retorna su etiqueta de categoría

    def calcular_costo_alquiler(self, dias, con_seguro=False): # Sobrescribe el cálculo adaptándolo a camionetas (Polimorfismo)
        """Polimorfismo: recargo fijo adicional de $5/día."""
        costo = super().calcular_costo_alquiler(dias) + (5.0 * dias) # Aplica tarifa base más un recargo fijo de $5 por día alquilado

        if con_seguro:                              # Si se solicita la inclusión del seguro
            costo *= 1.10                           # Aplica un incremento del 10% al monto final

        return costo                                # Retorna el monto final calculado


class Motocicleta(Vehiculo):                        # Clase Motocicleta que hereda de la clase abstracta Vehiculo

    def __init__(self, placa, marca, modelo, anio, tarifa_diaria, cilindraje=0, id_vehiculo=None): # Constructor
        super().__init__(placa, marca, modelo, anio, tarifa_diaria, id_vehiculo) # Llama al inicializador de la clase padre
        self.cilindraje = cilindraje                # Atributo exclusivo para motocicletas: la cilindrada del motor

    def categoria(self):                            # Implementación del método abstracto heredado
        return "Motocicleta"                        # Retorna la identificación de tipo Motocicleta

    def calcular_costo_alquiler(self, dias, con_seguro=False): # Sobrescribe el cálculo del alquiler con reglas para motocicletas
        """Polimorfismo: descuento del 5%."""
        costo = super().calcular_costo_alquiler(dias) * 0.95 # Aplica un 5% de descuento por promoción predeterminada en motos
        if con_seguro:                              # Si el usuario elige incluir seguro en el alquiler
            costo *= 1.10                           # Añade un 10% extra sobre el total
        return costo                                # Retorna el costo del alquiler ajustado


class Cliente:                                      # Clase que representa a los clientes registrados en el sistema

    def __init__(self, cedula, nombre, telefono, correo, id_cliente=None): # Constructor que crea el perfil del cliente
        self._id = id_cliente                       # Almacena el ID único de base de datos
        self._cedula = cedula                       # Documento de identidad del cliente
        self._nombre = nombre                       # Nombre completo del usuario registrado
        self._telefono = telefono                   # Número de teléfono del cliente
        self._correo = correo                       # Dirección de correo electrónico

    @property
    def id(self):                                   # Getter para el id del cliente
        return self._id                             # Retorna el identificador interno

    @id.setter
    def id(self, valor):                            # Setter para actualizar el id
        self._id = valor                            # Guarda el nuevo id de base de datos

    @property
    def cedula(self):                               # Getter para la cédula de identidad
        return self._cedula                         # Retorna el documento del cliente

    @cedula.setter
    def cedula(self, valor):                        # Setter para modificar el número de cédula
        self._cedula = valor                        # Actualiza el atributo de cédula

    @property
    def nombre(self):                               # Getter para el nombre
        return self._nombre                         # Retorna el nombre del cliente

    @nombre.setter
    def nombre(self, valor):                        # Setter para el nombre completo
        self._nombre = valor                        # Actualiza el nombre de la persona

    @property
    def telefono(self):                             # Getter para el teléfono
        return self._telefono                       # Retorna el número de contacto

    @telefono.setter
    def telefono(self, valor):                      # Setter para modificar el número telefónico
        self._telefono = valor                      # Guarda el nuevo teléfono

    @property
    def correo(self):                               # Getter para el email
        return self._correo                         # Retorna la dirección de correo electrónico

    @correo.setter
    def correo(self, valor):                        # Setter para modificar el correo electrónico
        self._correo = valor                        # Guarda el nuevo correo en el objeto

    def __str__(self):                              # Genera la información del cliente en formato de cadena legible
        return f"{self._nombre} (Cédula: {self._cedula}) - Tel: {self._telefono} - {self._correo}" # Formatea e imprime los datos del cliente


class ContratoAlquiler:                             # Clase para gestionar los documentos y contratos de alquiler formalizados

    def __init__(self, id_cliente, id_vehiculo, fecha_inicio, dias, costo_total,
                 con_seguro=False, id_contrato=None, estado="Activo"): # Constructor del contrato
        
        self._id = id_contrato                      # ID único que provee la Base de Datos al registrar el contrato
        self.id_cliente = id_cliente                # Llave foránea que asocia al cliente con este contrato
        self.id_vehiculo = id_vehiculo              # Llave foránea que asocia al vehículo rentado con este contrato
        self.fecha_inicio = fecha_inicio            # Fecha de inicio del contrato (ISO YYYY-MM-DD)
        self.dias = dias                            # Cantidad de días de renta contratados
        self.costo_total = costo_total              # Monto final cobrado al cliente
        self.con_seguro = con_seguro                # Booleano que indica si se pagó el opcional de seguro
        self.estado = estado                        # Estado del contrato ("Activo", "Cancelado" o "Finalizado")

    @property
    def id(self):                                   # Getter para el identificador de contrato
        return self._id                             # Retorna el id del contrato

    @id.setter
    def id(self, valor):                            # Setter para asignar un id al contrato
        self._id = valor                            # Actualiza el id del documento

    def __str__(self):                              # Devuelve una cadena con el resumen de la renta efectuada
        return (f"Contrato #{self._id} - Cliente:{self.id_cliente} - Vehiculo:{self.id_vehiculo} " # Formatea todos los datos clave en texto
                f"- {self.dias} día(s) - Total: ${self.costo_total:.2f} - {self.estado}")


# SECCIÓN 4: BASE DE DATOS
RUTA_BD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alquiler_vehiculos.db") # Establece la ruta absoluta al archivo SQLite (.db)

class BaseDatos:                                    # Clase responsable del manejo de la Base de Datos SQLite y del CRUD
    """Capa de acceso a datos. Gestiona la conexión SQLite y el CRUD completo."""

    def __init__(self, ruta_bd=RUTA_BD):            # Constructor de la conexión de datos
        self.ruta_bd = ruta_bd                      # Almacena internamente la ruta del archivo de la base de datos
        self.conexion = sqlite3.connect(self.ruta_bd) # Abre o crea la base de datos y establece la conexión activa
        self.conexion.execute("PRAGMA foreign_keys = ON;") # Habilita de forma obligatoria el control de integridad referencial
        self._crear_tablas()                        # Ejecuta la creación inicial de las tablas si no existieran previamente

    def _crear_tablas(self):                        # Método privado que inicializa la estructura de la base de datos

        cursor = self.conexion.cursor()             # Crea un cursor para ejecutar sentencias de SQL
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehiculos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                placa TEXT NOT NULL UNIQUE,
                marca TEXT NOT NULL,
                modelo TEXT NOT NULL,
                anio INTEGER NOT NULL,
                tarifa_diaria REAL NOT NULL,
                atributo_extra TEXT,
                disponible INTEGER NOT NULL DEFAULT 1
            );
        """)                                        # Crea la tabla de vehículos indicando el atributo_extra según la subclase
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cedula TEXT NOT NULL UNIQUE,
                nombre TEXT NOT NULL,
                telefono TEXT,
                correo TEXT
            );
        """)                                        # Crea la tabla de clientes indexada con cédula única obligatoria
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contratos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_cliente INTEGER NOT NULL,
                id_vehiculo INTEGER NOT NULL,
                fecha_inicio TEXT NOT NULL,
                dias INTEGER NOT NULL,
                costo_total REAL NOT NULL,
                con_seguro INTEGER NOT NULL DEFAULT 0,
                estado TEXT NOT NULL DEFAULT 'Activo',
                FOREIGN KEY (id_cliente) REFERENCES clientes(id),
                FOREIGN KEY (id_vehiculo) REFERENCES vehiculos(id)
            );
        """)                                        # Crea la tabla contratos conectada a clientes y vehículos mediante relaciones foráneas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mantenimientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_vehiculo INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                FOREIGN KEY (id_vehiculo) REFERENCES vehiculos(id)
            );
        """)                                        # Crea la tabla para almacenar la bitácora de mantenimientos asociados a cada carro

        self.conexion.commit()                      # Guarda físicamente todos los cambios de estructura en el archivo de base de datos

    @staticmethod
    def _fila_a_vehiculo(fila):                     # Método estático para reconstruir objetos de Python desde registros de la base de datos
        (id_v, tipo, placa, marca, modelo, anio, tarifa, extra, disponible) = fila # Desempaqueta los elementos del registro en variables individuales

        if tipo == "Automovil":                     # Evalúa si la fila corresponde a un Automóvil
            v = Automovil(placa, marca, modelo, anio, tarifa,
                          num_puertas=int(float(extra)) if extra else 4, id_vehiculo=id_v) # Reconstruye un objeto Automóvil convirtiendo la columna extra (tolera valores guardados como decimal)
            
        elif tipo == "Camioneta":                   # Evalúa si la fila representa una Camioneta
            v = Camioneta(placa, marca, modelo, anio, tarifa,
                          capacidad_carga_kg=float(extra) if extra else 0, id_vehiculo=id_v) # Reconstruye una Camioneta asignando capacidad de carga
            
        else:                                       # En cualquier otro caso, asume que es una Motocicleta
            v = Motocicleta(placa, marca, modelo, anio, tarifa,
                             cilindraje=int(float(extra)) if extra else 0, id_vehiculo=id_v) # Reconstruye el objeto de tipo Motocicleta (tolera valores guardados como decimal)
            
        v.disponible = bool(disponible)             # Transforma el estado disponible (guardado como 1 o 0) en un booleano (True/False)

        return v                                    # Retorna la instancia de vehículo generada y lista para operar

    # ---------------- CRUD: VEHICULOS ----------------
    def crear_vehiculo(self, vehiculo):             # Operación CREATE: Guarda un nuevo vehículo en la base de datos

        tipo = vehiculo.categoria().replace("ó", "o") # Normaliza el tipo del vehículo quitando tildes para guardarlo homogéneamente
        extra = None                                # Inicializa el campo que recibirá el valor particular de cada subclase

        if isinstance(vehiculo, Automovil):         # Si la clase del vehículo es Automovil
            extra = vehiculo.num_puertas            # Se extrae el número de puertas del automóvil

        elif isinstance(vehiculo, Camioneta):       # Si la clase es Camioneta
            extra = vehiculo.capacidad_carga_kg     # Se extrae la capacidad de carga en kilogramos

        elif isinstance(vehiculo, Motocicleta):     # Si la clase es Motocicleta
            extra = vehiculo.cilindraje             # Se extrae el cilindraje

        cursor = self.conexion.cursor()             # Crea un cursor para ejecutar el SQL
        cursor.execute("""
            INSERT INTO vehiculos (tipo, placa, marca, modelo, anio, tarifa_diaria, atributo_extra, disponible)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (tipo, vehiculo.placa, vehiculo.marca, vehiculo.modelo, vehiculo.anio,
              vehiculo.tarifa_diaria, extra, int(vehiculo.disponible))) # Inserta los datos del vehículo asignándole parámetros seguros de consulta
        
        self.conexion.commit()                      # Confirma la transacción guardando el nuevo registro
        vehiculo.id = cursor.lastrowid              # Obtiene el ID numérico autogenerado por SQLite y lo guarda en el objeto Python

        return vehiculo.id                          # Retorna el ID de la base de datos para futuras referencias

    def leer_vehiculos(self):                       # Operación READ: Recupera la totalidad de vehículos del catálogo

        cursor = self.conexion.cursor()             # Abre un cursor de consulta de datos
        cursor.execute("SELECT id, tipo, placa, marca, modelo, anio, tarifa_diaria, atributo_extra, disponible FROM vehiculos") # Solicita todas las columnas de la tabla vehiculos
        filas = cursor.fetchall()                   # Recupera la lista con todas las filas devueltas
        vehiculos = [self._fila_a_vehiculo(f) for f in filas] # Transforma cada fila de SQL en su objeto correspondiente en Python 

        for v in vehiculos:                         # Ciclo para poblar la lista enlazada de mantenimiento de cada auto recuperado
            cursor.execute("SELECT fecha, descripcion FROM mantenimientos WHERE id_vehiculo=? ORDER BY id", (v.id,)) # Obtiene el historial del vehículo actual de forma ordenada
            for fecha, desc in cursor.fetchall():   # Por cada fila encontrada en la bitácora de mantenimiento
                v.historial_mantenimiento.agregar_final((fecha, desc)) # Agrega el evento a la lista enlazada de mantenimiento de ese auto
        return vehiculos                            # Devuelve el arreglo completo de objetos de tipo vehículo listos para usar
    

    def obtener_vehiculo(self, id_vehiculo):        # Operación READ (SELECT de un registro particular)

        cursor = self.conexion.cursor()             # Abre un cursor de consulta SQL
        cursor.execute("SELECT id, tipo, placa, marca, modelo, anio, tarifa_diaria, atributo_extra, disponible FROM vehiculos WHERE id=?", (id_vehiculo,)) # Busca el vehículo por ID
        fila = cursor.fetchone()                    # Recupera la fila correspondiente si es que existe

        if not fila:                                # Si no se encontró ningún registro que coincida con el ID
            return None                             # Retorna None indicando que el vehículo no está registrado
        
        vehiculo = self._fila_a_vehiculo(fila)      # Transforma la fila encontrada en su respectiva instancia de Python
        cursor.execute("SELECT fecha, descripcion FROM mantenimientos WHERE id_vehiculo=? ORDER BY id", (vehiculo.id,)) # Obtiene su historial de mantenimientos

        for fecha, desc in cursor.fetchall():       # Recorre todos los eventos de mantenimiento encontrados
            vehiculo.historial_mantenimiento.agregar_final((fecha, desc)) # Inserta cada evento al final de la lista enlazada del vehículo

        return vehiculo                             # Retorna el objeto del vehículo con su historial cargado

    def actualizar_vehiculo(self, vehiculo):        # Operación UPDATE: Actualiza los cambios de un auto en la base de datos

        extra = None                                # Inicializa la variable temporal de atributo extra

        if isinstance(vehiculo, Automovil):         # Si el vehículo a modificar es un Automóvil
            extra = vehiculo.num_puertas            # Recupera el número de puertas actual

        elif isinstance(vehiculo, Camioneta):       # Si es una Camioneta
            extra = vehiculo.capacidad_carga_kg     # Recupera su capacidad de carga

        elif isinstance(vehiculo, Motocicleta):     # Si es una Motocicleta
            extra = vehiculo.cilindraje             # Obtiene su cilindraje

        cursor = self.conexion.cursor()             # Abre un cursor
        cursor.execute("""
            UPDATE vehiculos SET placa=?, marca=?, modelo=?, anio=?, tarifa_diaria=?, atributo_extra=?, disponible=?
            WHERE id=?
        """, (vehiculo.placa, vehiculo.marca, vehiculo.modelo, vehiculo.anio,
              vehiculo.tarifa_diaria, extra, int(vehiculo.disponible), vehiculo.id)) # Ejecuta el script de actualización en base a parámetros del objeto
        self.conexion.commit()                      # Guarda de forma persistente los datos actualizados

    def eliminar_vehiculo(self, id_vehiculo):        # Operación DELETE: Elimina de la base de datos el vehículo y sus dependencias
        
        cursor = self.conexion.cursor()             # Abre un cursor para interactuar con la base de datos
        cursor.execute("DELETE FROM mantenimientos WHERE id_vehiculo=?", (id_vehiculo,)) # Elimina primero todo el historial de mantenimientos para evitar fallas de integridad
        cursor.execute("DELETE FROM vehiculos WHERE id=?", (id_vehiculo,)) # Elimina finalmente la ficha del auto por su ID único
        self.conexion.commit()                      # Guarda los cambios de la transacción

    def agregar_mantenimiento_bd(self, id_vehiculo, fecha, descripcion): # Inserta un registro de mantenimiento en la base de datos

        cursor = self.conexion.cursor()             # Abre un cursor para SQL
        cursor.execute("INSERT INTO mantenimientos (id_vehiculo, fecha, descripcion) VALUES (?, ?, ?)",
                       (id_vehiculo, fecha, descripcion)) # Inserta la tupla en la tabla correspondientemente
        
        self.conexion.commit()                      # Confirma la transacción en el disco

    # ---------------- CRUD: CLIENTES ----------------
    def crear_cliente(self, cliente):               # Operación CREATE: Registra un nuevo cliente en la base de datos

        cursor = self.conexion.cursor()             # Abre un cursor de comandos
        cursor.execute("INSERT INTO clientes (cedula, nombre, telefono, correo) VALUES (?, ?, ?, ?)",
                       (cliente.cedula, cliente.nombre, cliente.telefono, cliente.correo)) # Ejecuta el comando SQL para insertar al cliente
        self.conexion.commit()                      # Consolida el registro en la base de datos
        cliente.id = cursor.lastrowid               # Recupera el ID asignado por el autoincremental de SQLite y lo almacena

        return cliente.id                           # Retorna el nuevo ID único del cliente

    def leer_clientes(self):                        # Operación READ: Recupera la lista de todos los clientes

        cursor = self.conexion.cursor()             # Abre un cursor
        cursor.execute("SELECT id, cedula, nombre, telefono, correo FROM clientes") # Consulta la totalidad de clientes
        return [Cliente(cedula, nombre, tel, correo, id_cliente=idc)
                for (idc, cedula, nombre, tel, correo) in cursor.fetchall()] # Retorna una lista llena con objetos Cliente creados en tiempo de ejecución

    def obtener_cliente(self, id_cliente):          # Operación READ: Obtiene los datos de un cliente específico por ID
        cursor = self.conexion.cursor()             # Crea un cursor
        cursor.execute("SELECT id, cedula, nombre, telefono, correo FROM clientes WHERE id=?", (id_cliente,)) # Busca al cliente
        fila = cursor.fetchone()                    # Extrae la fila única obtenida
        if fila:                                    # Si la consulta arrojó un resultado exitoso
            idc, cedula, nombre, tel, correo = fila # Desempaqueta las columnas devueltas de la tabla
            return Cliente(cedula, nombre, tel, correo, id_cliente=idc) # Reconstruye y retorna el objeto Cliente correspondiente
        return None                                 # Retorna None si no se halló al cliente

    def actualizar_cliente(self, cliente):          # Operación UPDATE: Actualiza los datos de un cliente en la base de datos
        cursor = self.conexion.cursor()             # Crea un cursor de SQL
        cursor.execute("UPDATE clientes SET cedula=?, nombre=?, telefono=?, correo=? WHERE id=?",
                       (cliente.cedula, cliente.nombre, cliente.telefono, cliente.correo, cliente.id)) # Actualiza las columnas basándose en el ID
        self.conexion.commit()                      # Guarda los cambios aplicados en la base de datos

    def eliminar_cliente(self, id_cliente):          # Operación DELETE: Quita a un cliente de la base de datos
        cursor = self.conexion.cursor()             # Crea un cursor de comandos
        cursor.execute("DELETE FROM clientes WHERE id=?", (id_cliente,)) # Ejecuta la baja del registro mediante su identificador
        self.conexion.commit()                      # Guarda de forma persistente la eliminación del cliente

    # ---------------- CRUD: CONTRATOS ----------------
    def crear_contrato(self, contrato):             # Operación CREATE: Inserta un nuevo contrato de alquiler
        cursor = self.conexion.cursor()             # Abre un cursor
        cursor.execute("""
            INSERT INTO contratos (id_cliente, id_vehiculo, fecha_inicio, dias, costo_total, con_seguro, estado)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (contrato.id_cliente, contrato.id_vehiculo, contrato.fecha_inicio, contrato.dias,
              contrato.costo_total, int(contrato.con_seguro), contrato.estado)) # Ejecuta el comando guardando el seguro como entero (0 o 1)
        self.conexion.commit()                      # Confirma el guardado del contrato
        contrato.id = cursor.lastrowid              # Guarda en el objeto el ID autogenerado del contrato

        return contrato.id                          # Retorna el ID de la transacción

    def leer_contratos(self):                       # Operación READ: Recupera todos los contratos del sistema
        cursor = self.conexion.cursor()             # Abre un cursor SQL
        cursor.execute("""SELECT id, id_cliente, id_vehiculo, fecha_inicio, dias, costo_total, con_seguro, estado
                           FROM contratos""")       # Ejecuta la consulta completa de contratos
        return [ContratoAlquiler(idcli, idveh, fecha, dias, costo, bool(seguro), id_contrato=idc, estado=estado)
                for (idc, idcli, idveh, fecha, dias, costo, seguro, estado) in cursor.fetchall()] # Retorna el arreglo de contratos instanciados

    def obtener_contrato(self, id_contrato):        # Operación READ: Obtiene un contrato específico por ID
        cursor = self.conexion.cursor()             # Crea un cursor para comandos de base de datos
        cursor.execute("""SELECT id, id_cliente, id_vehiculo, fecha_inicio, dias, costo_total, con_seguro, estado
                           FROM contratos WHERE id=?""", (id_contrato,)) # Ejecuta la consulta filtrada
        fila = cursor.fetchone()                    # Lee el resultado
        if fila:                                    # Si existía el contrato en la base de datos
            idc, idcli, idveh, fecha, dias, costo, seguro, estado = fila # Desempaqueta las columnas del registro
            return ContratoAlquiler(idcli, idveh, fecha, dias, costo, bool(seguro), id_contrato=idc, estado=estado) # Retorna el contrato reconstruido
        return None                                 # Retorna None si no se encontró nada

    def actualizar_contrato(self, contrato):        # Operación UPDATE: Actualiza el registro de un contrato existente
        cursor = self.conexion.cursor()             # Crea un cursor de SQL
        cursor.execute("""
            UPDATE contratos SET id_cliente=?, id_vehiculo=?, fecha_inicio=?, dias=?, costo_total=?, con_seguro=?, estado=?
            WHERE id=?
        """, (contrato.id_cliente, contrato.id_vehiculo, contrato.fecha_inicio, contrato.dias,
              contrato.costo_total, int(contrato.con_seguro), contrato.estado, contrato.id)) # Reemplaza el registro actualizando el estado y datos clave
        self.conexion.commit()                      # Confirma la transacción en la base de datos

    def eliminar_contrato(self, id_contrato):        # Operación DELETE: Elimina físicamente un contrato del sistema
        cursor = self.conexion.cursor()             # Crea el cursor de comandos
        cursor.execute("DELETE FROM contratos WHERE id=?", (id_contrato,)) # Remueve la fila por ID
        self.conexion.commit()                      # Confirma la eliminación física

    def cerrar(self):                               # Método para cerrar la conexión con la base de datos de forma segura
        self.conexion.close()                       # Libera el socket y cierra la comunicación con el archivo .db


# SECCIÓN 5: GESTOR DEL SISTEMA (lógica de negocio)

class GestorAlquiler:                               # Clase principal controladora que integra la base de datos y las estructuras auxiliares

    def __init__(self, ruta_bd=None):               # Constructor que inicializa el motor lógico

        self.bd = BaseDatos(ruta_bd) if ruta_bd else BaseDatos() # Inicializa la conexión BD especificando una ruta alternativa o usando la de por defecto
        self.cola_espera = Cola()                   # Inicializa la cola de espera FIFO para procesar clientes sin vehículos disponibles
        self.pila_deshacer_contratos = Pila()       # Inicializa la pila LIFO para permitir revertir transacciones de alquiler recientes

    # ---------------- VEHICULOS ----------------
    def registrar_vehiculo(self, tipo, placa, marca, modelo, anio, tarifa_diaria, atributo_extra): # Flujo de negocio para dar de alta autos

        if tipo == "Automovil":                     # Evalúa si la categoría especificada es Automovil
            vehiculo = Automovil(placa, marca, modelo, anio, tarifa_diaria, num_puertas=atributo_extra) # Instancia el Automovil correspondiente

        elif tipo == "Camioneta":                   # Evalúa si es una Camioneta
            vehiculo = Camioneta(placa, marca, modelo, anio, tarifa_diaria, capacidad_carga_kg=atributo_extra) # Instancia la Camioneta

        else:                                       # En cualquier otro caso
            vehiculo = Motocicleta(placa, marca, modelo, anio, tarifa_diaria, cilindraje=atributo_extra) # Instancia la Motocicleta

        self.bd.crear_vehiculo(vehiculo)            # Registra de forma persistente el nuevo vehículo en la base de datos

        return vehiculo                             # Retorna el objeto vehiculo creado

    def listar_vehiculos(self):                     # Servicio de negocio para listar vehículos
        return self.bd.leer_vehiculos()             # Llama y retorna los vehículos leídos de la capa de acceso a datos

    def actualizar_vehiculo(self, vehiculo):        # Servicio de negocio para actualizar un carro
        self.bd.actualizar_vehiculo(vehiculo)       # Delega la actualización a la base de datos

    def eliminar_vehiculo(self, id_vehiculo):        # Servicio de negocio para eliminar un auto
        self.bd.eliminar_vehiculo(id_vehiculo)       # Delega el borrado a la base de datos

    def vehiculos_disponibles_por_categoria(self, categoria): # Filtra los vehículos por categoría que no estén en uso
        return [v for v in self.listar_vehiculos() if v.categoria() == categoria and v.disponible] # Retorna la lista filtrada de vehículos aptos

    # ---------------- ORDENAMIENTO Y BÚSQUEDA: vehículos ----------------
    def vehiculos_ordenados_por_tarifa(self, avanzado=True): # Método para listar vehículos ordenándolos por su tarifa diaria

        vehiculos = self.listar_vehiculos()         # Obtiene el catálogo completo de vehículos

        if avanzado:                                # Evalúa si se solicita usar el algoritmo avanzado
            return quick_sort(vehiculos, clave=lambda v: v.tarifa_diaria) # Retorna la lista ordenada mediante Quick Sort (O(n log n))
        
        return ordenamiento_burbuja(vehiculos, clave=lambda v: v.tarifa_diaria) # Retorna la lista ordenada usando Burbuja (O(n^2))

    def buscar_vehiculo_por_placa_lineal(self, placa): # Realiza búsqueda lineal de un vehículo por su placa
        vehiculos = self.listar_vehiculos()         # Recupera la lista de vehículos actuales
        return busqueda_lineal(vehiculos, placa.upper(), clave=lambda v: v.placa) # Ejecuta y retorna el resultado de buscar la placa en mayúsculas

    def buscar_vehiculo_por_tarifa_binaria(self, tarifa): # Realiza búsqueda binaria rápida por valor de tarifa diaria
        vehiculos_ordenados = self.vehiculos_ordenados_por_tarifa(avanzado=True) # Ordena previamente la lista (es requisito obligatorio para búsqueda binaria)
        return busqueda_binaria(vehiculos_ordenados, tarifa, clave=lambda v: v.tarifa_diaria) # Ejecuta y retorna el resultado de la búsqueda logarítmica

    # ---------------- CLIENTES ----------------
    def registrar_cliente(self, cedula, nombre, telefono, correo): # Flujo de negocio para registrar un nuevo cliente
        cliente = Cliente(cedula, nombre, telefono, correo) # Instancia la clase de dominio Cliente
        self.bd.crear_cliente(cliente)              # Guarda de forma persistente en la capa de datos
        return cliente                              # Retorna la instancia de cliente resultante

    def listar_clientes(self):                      # Servicio de negocio para obtener la lista de clientes
        return self.bd.leer_clientes()              # Retorna los registros leídos de la capa de datos

    def actualizar_cliente(self, cliente):          # Servicio de negocio para actualizar un perfil de cliente
        self.bd.actualizar_cliente(cliente)         # Envía los datos actualizados a la base de datos

    def eliminar_cliente(self, id_cliente):          # Servicio de negocio para borrar un cliente
        self.bd.eliminar_cliente(id_cliente)         # Envía la solicitud de eliminación por id a la base de datos

    def clientes_ordenados_por_nombre(self):        # Ordena la lista de clientes alfabéticamente por su nombre
        return ordenamiento_burbuja(self.listar_clientes(), clave=lambda c: c.nombre.lower()) # Ordena usando Burbuja convirtiendo los nombres a minúsculas

    def buscar_cliente_por_cedula_lineal(self, cedula): # Busca un cliente por su documento usando búsqueda lineal
        return busqueda_lineal(self.listar_clientes(), cedula, clave=lambda c: c.cedula) # Ejecuta el algoritmo comparando las cédulas y retorna el resultado

    # ---------------- COLA DE ESPERA ----------------
    def solicitar_alquiler(self, id_cliente, categoria, dias, con_seguro=False): # Intenta alquilar un auto o lo encola si no hay stock
        disponibles = self.vehiculos_disponibles_por_categoria(categoria) # Busca vehículos desocupados que pertenezcan a la categoría pedida
        if not disponibles:                         # Si no existe stock disponible para el alquiler en este momento
            self.cola_espera.encolar({              # Agrega un diccionario con la solicitud al final de la cola de espera
                "id_cliente": id_cliente,
                "categoria": categoria,
                "dias": dias,
                "con_seguro": con_seguro,
                "fecha_solicitud": date.today().isoformat(),
            })
            return None, "No hay vehículos disponibles. Cliente agregado a la lista de espera." # Retorna mensaje de que se encoló la petición
                                                    
        vehiculo = disponibles[0]                   # Si sí hay disponibles, toma el primer auto libre
        contrato = self._crear_contrato(id_cliente, vehiculo, dias, con_seguro) # Genera y registra el contrato de alquiler correspondientemente
        return contrato, f"Alquiler registrado con el vehículo {vehiculo.placa}." # Retorna el contrato creado y un mensaje de confirmación

    def atender_siguiente_en_espera(self):          # Procesa la solicitud al frente de la cola de espera

        if self.cola_espera.esta_vacia():           # Verifica si no existen personas esperando turno
            return None, "No hay clientes en la lista de espera." # Retorna mensaje de lista vacía
        
        solicitud = self.cola_espera.ver_frente()   # Revisa los datos de la solicitud al frente de la cola sin sacarla todavía
        disponibles = self.vehiculos_disponibles_por_categoria(solicitud["categoria"]) # Revisa si ya se desocupó un carro de esa categoría

        if not disponibles:                         # Si sigue sin haber carros libres en esa categoría
            return None, f"Aún no hay vehículos de categoría '{solicitud['categoria']}' disponibles." # Retorna mensaje de rechazo temporal
        
        solicitud = self.cola_espera.desencolar()   # Saca definitivamente la solicitud de la cola al confirmarse que se le puede atender
        vehiculo = disponibles[0]                   # Toma el auto de esa categoría que se encuentra disponible
        contrato = self._crear_contrato(solicitud["id_cliente"], vehiculo, solicitud["dias"], solicitud["con_seguro"]) # Genera el contrato para el cliente

        return contrato, f"Cliente atendido de la lista de espera con el vehículo {vehiculo.placa}." # Confirma el proceso de alquiler

    # ---------------- CONTRATOS + PILA DESHACER ----------------
    def _crear_contrato(self, id_cliente, vehiculo, dias, con_seguro): # Crea e inserta un contrato de alquiler
        costo = vehiculo.calcular_costo_alquiler(dias, con_seguro=con_seguro) # Calcula el valor total utilizando polimorfismo dinámico
        contrato = ContratoAlquiler(
            id_cliente=id_cliente, id_vehiculo=vehiculo.id,
            fecha_inicio=date.today().isoformat(), dias=dias,
            costo_total=costo, con_seguro=con_seguro,
        )                                           # Instancia el contrato de alquiler
        self.bd.crear_contrato(contrato)            # Guarda de forma persistente el contrato en la base de datos
        vehiculo.disponible = False                 # Modifica el estado del auto a alquilado (False)
        self.bd.actualizar_vehiculo(vehiculo)       # Guarda la actualización del estado del auto en la base de datos
        self.pila_deshacer_contratos.apilar(contrato) # Empuja el contrato creado a la pila LIFO para permitir deshacer esta acción rápido

        return contrato                             # Retorna el contrato generado y guardado

    def deshacer_ultimo_contrato(self):             # Revierte la última transacción de alquiler hecha utilizando la Pila

        if self.pila_deshacer_contratos.esta_vacia(): # Evalúa si no se han registrado transacciones en esta sesión
            return None, "No hay contratos recientes para deshacer." # Retorna mensaje avisando que no hay nada que revertir
        
        contrato = self.pila_deshacer_contratos.desapilar() # Extrae de la cima el último contrato guardado (LIFO)
        contrato.estado = "Cancelado"               # Cambia el estado del contrato a "Cancelado"
        self.bd.actualizar_contrato(contrato)       # Actualiza el estado del contrato en la base de datos
        vehiculo = self.bd.obtener_vehiculo(contrato.id_vehiculo) # Recupera el objeto del vehículo involucrado

        if vehiculo:                                # Si el vehículo existe en el sistema
            vehiculo.disponible = True              # Devuelve la disponibilidad del carro a disponible (True)
            self.bd.actualizar_vehiculo(vehiculo)   # Actualiza el estado de disponibilidad del vehículo en la base de datos

        return contrato, f"Contrato #{contrato.id} deshecho. El vehículo vuelve a estar disponible." # Retorna el contrato y confirmación

    def listar_contratos(self):                     # Obtiene la totalidad de contratos del sistema
        return self.bd.leer_contratos()             # Retorna los contratos recuperados desde la base de datos

    def finalizar_contrato(self, id_contrato):      # Cierra un alquiler devolviendo el auto a disponibilidad libre

        contrato = self.bd.obtener_contrato(id_contrato) # Busca el contrato de interés por su ID en la base de datos

        if not contrato:                            # Si el ID especificado no coincide con ningún contrato
            return False                            # Retorna False señalando la falla de cierre
        
        contrato.estado = "Finalizado"              # Modifica el estado de control a "Finalizado"
        self.bd.actualizar_contrato(contrato)       # Guarda la actualización del contrato en la base de datos
        vehiculo = self.bd.obtener_vehiculo(contrato.id_vehiculo) # Recupera el auto asociado a la renta para actualizarlo

        if vehiculo:                                # Si se localizó con éxito el vehículo
            vehiculo.disponible = True              # Cambia su disponibilidad a True (libre) para que otros lo alquilen
            self.bd.actualizar_vehiculo(vehiculo)   # Guarda los cambios del estado de disponibilidad del auto en la base de datos

        return True                                 # Retorna True indicando que el proceso concluyó satisfactoriamente

    # ---------------- MANTENIMIENTO (Lista Enlazada) ----------------
    def registrar_mantenimiento(self, id_vehiculo, descripcion): # Registra un servicio mecánico para un auto específico
        fecha = date.today().isoformat()            # Genera la fecha del día de hoy en formato ISO estándar
        self.bd.agregar_mantenimiento_bd(id_vehiculo, fecha, descripcion) # Guarda de forma persistente el mantenimiento en la base de datos

    def historial_mantenimiento(self, id_vehiculo):  # Obtiene los servicios mecánicos aplicados a un vehículo

        vehiculo = self.bd.obtener_vehiculo(id_vehiculo) # Solicita los datos del auto por ID

        if not vehiculo:                            # Si no existe el auto buscado
            return []                               # Retorna un arreglo vacío de historial
        
        return vehiculo.historial_mantenimiento.a_lista_python() # Convierte la lista enlazada interna a una lista de Python y la retorna

    def cerrar(self):                               # Método de cierre seguro
        self.bd.cerrar()                            # Envía la orden de liberar la conexión a la base de datos

# SECCIÓN 6: INTERFAZ GRÁFICA
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import customtkinter as ctk

ctk.set_appearance_mode("dark")          # "dark", "light" o "system"
ctk.set_default_color_theme("blue")      # tema de color base

# Paleta de colores propia para acentos visuales
COLOR_PRIMARIO = "#2563EB"      # azul
COLOR_PRIMARIO_HOVER = "#1D4ED8"
COLOR_EXITO = "#16A34A"         # verde
COLOR_EXITO_HOVER = "#15803D"
COLOR_PELIGRO = "#DC2626"       # rojo
COLOR_PELIGRO_HOVER = "#B91C1C"
COLOR_ADVERTENCIA = "#EA580C"   # naranja
COLOR_ADVERTENCIA_HOVER = "#C2410C"
COLOR_TARJETA = "#1F2937"
COLOR_TEXTO_SECUNDARIO = "#9CA3AF"

ICONO_AUTOMOVIL = "🚗"
ICONO_CAMIONETA = "🛻"
ICONO_MOTOCICLETA = "🏍️"
ICONOS_CATEGORIA = {"Automóvil": ICONO_AUTOMOVIL, "Camioneta": ICONO_CAMIONETA, "Motocicleta": ICONO_MOTOCICLETA}


def _estilizar_treeview_oscuro():
    """Aplica un tema oscuro coherente al widget ttk.Treeview (tablas),
    ya que CustomTkinter no incluye tablas propias."""
    estilo = ttk.Style()
    estilo.theme_use("clam")
    estilo.configure("Treeview",
                      background="#111827",
                      foreground="#F3F4F6",
                      fieldbackground="#111827",
                      rowheight=30,
                      borderwidth=0,
                      font=("Segoe UI", 11))
    estilo.configure("Treeview.Heading",
                      background="#374151",
                      foreground="#F9FAFB",
                      font=("Segoe UI", 11, "bold"),
                      borderwidth=0)
    estilo.map("Treeview",
               background=[("selected", COLOR_PRIMARIO)],
               foreground=[("selected", "white")])
    estilo.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])


class TarjetaResumen(ctk.CTkFrame):
    """Pequeña tarjeta de estadística (ícono + número + etiqueta) para el dashboard."""

    def __init__(self, master, icono, titulo, color=COLOR_PRIMARIO, **kwargs):
        super().__init__(master, corner_radius=14, fg_color=COLOR_TARJETA, **kwargs)
        self.lbl_icono = ctk.CTkLabel(self, text=icono, font=ctk.CTkFont(size=30))
        self.lbl_icono.pack(pady=(14, 0))
        self.lbl_valor = ctk.CTkLabel(self, text="0", font=ctk.CTkFont(size=26, weight="bold"), text_color=color)
        self.lbl_valor.pack()
        self.lbl_titulo = ctk.CTkLabel(self, text=titulo, font=ctk.CTkFont(size=12),
                                        text_color=COLOR_TEXTO_SECUNDARIO)
        self.lbl_titulo.pack(pady=(0, 14))

    def actualizar(self, valor):
        self.lbl_valor.configure(text=str(valor))


class AplicacionAlquiler(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🚗 Sistema de Alquiler de Vehículos — Grupo 9")
        self.geometry("1180x720")
        self.minsize(1000, 640)

        self.gestor = GestorAlquiler()
        _estilizar_treeview_oscuro()

        self._construir_barra_lateral()
        self._construir_contenedor_principal()
        self.mostrar_seccion("dashboard")

        self.protocol("WM_DELETE_WINDOW", self._on_cerrar)

    # ------------------------------------------------------------------
    def _construir_barra_lateral(self):
        self.barra = ctk.CTkFrame(self, width=210, corner_radius=0, fg_color="#111827")
        self.barra.pack(side="left", fill="y")
        self.barra.pack_propagate(False)

        ctk.CTkLabel(self.barra, text="🚗 RentaCar", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(28, 4))
        ctk.CTkLabel(self.barra, text="Grupo 9 · LP2", font=ctk.CTkFont(size=12),
                     text_color=COLOR_TEXTO_SECUNDARIO).pack(pady=(0, 24))

        botones = [
            ("📊  Dashboard", "dashboard"),
            ("🚙  Vehículos", "vehiculos"),
            ("👤  Clientes", "clientes"),
            ("📋  Alquileres", "alquileres"),
            ("📄  Contratos", "contratos"),
            ("🛠️  Mantenimiento", "mantenimiento"),
        ]
        self.botones_nav = {}
        for texto, clave in botones:
            btn = ctk.CTkButton(self.barra, text=texto, anchor="w", height=42,
                                 corner_radius=10, fg_color="transparent",
                                 hover_color="#1F2937", font=ctk.CTkFont(size=14),
                                 command=lambda c=clave: self.mostrar_seccion(c))
            btn.pack(fill="x", padx=14, pady=4)
            self.botones_nav[clave] = btn

    def _construir_contenedor_principal(self):
        self.contenedor = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor.pack(side="right", fill="both", expand=True, padx=18, pady=18)

        self.secciones = {}
        self.secciones["dashboard"] = SeccionDashboard(self.contenedor, self.gestor)
        self.secciones["vehiculos"] = SeccionVehiculos(self.contenedor, self.gestor)
        self.secciones["clientes"] = SeccionClientes(self.contenedor, self.gestor)
        self.secciones["alquileres"] = SeccionAlquileres(self.contenedor, self.gestor, self._refrescar_todo)
        self.secciones["contratos"] = SeccionContratos(self.contenedor, self.gestor)
        self.secciones["mantenimiento"] = SeccionMantenimiento(self.contenedor, self.gestor)

    def mostrar_seccion(self, clave):
        for c, boton in self.botones_nav.items():
            boton.configure(fg_color=COLOR_PRIMARIO if c == clave else "transparent")
        for c, seccion in self.secciones.items():
            if c == clave:
                seccion.pack(fill="both", expand=True)
                seccion.refrescar()
            else:
                seccion.pack_forget()

    def _refrescar_todo(self):
        for seccion in self.secciones.values():
            seccion.refrescar()

    def _on_cerrar(self):
        self.gestor.cerrar()
        self.destroy()

# SECCIÓN: DASHBOARD (resumen visual del sistema)
class GraficoBarras(ctk.CTkFrame):
    """
    Mini gráfico de barras horizontales dibujado a mano con tkinter Canvas.
    No requiere librerías externas (matplotlib, etc.) ni imágenes con
    derechos de autor: todo el dibujo se genera por código.
    """

    def __init__(self, master, titulo, **kwargs):
        super().__init__(master, corner_radius=14, fg_color=COLOR_TARJETA, **kwargs)
        ctk.CTkLabel(self, text=titulo, font=ctk.CTkFont(size=15, weight="bold")).pack(
            anchor="w", padx=18, pady=(16, 6))
        self.canvas = tk.Canvas(self, height=170, bg="#1F2937", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=18, pady=(0, 16))

    def actualizar(self, datos):
        """datos: lista de tuplas (etiqueta, valor, color)"""
        self.canvas.delete("all")
        self.canvas.update_idletasks()
        ancho = max(self.canvas.winfo_width(), 260)
        alto_disponible = 150
        if not datos:
            self.canvas.create_text(ancho // 2, 70, text="Sin datos aún",
                                     fill=COLOR_TEXTO_SECUNDARIO, font=("Segoe UI", 11))
            return
        maximo = max(v for _, v, _ in datos) or 1
        n = len(datos)
        alto_barra = min(30, (alto_disponible - 10 * (n + 1)) // n) if n else 20
        alto_barra = max(alto_barra, 16)
        y = 12
        etiqueta_ancho = 110
        barra_max_ancho = ancho - etiqueta_ancho - 60
        for etiqueta, valor, color in datos:
            self.canvas.create_text(8, y + alto_barra / 2, text=etiqueta, anchor="w",
                                     fill="#E5E7EB", font=("Segoe UI", 10))
            largo = int((valor / maximo) * barra_max_ancho) if maximo else 0
            largo = max(largo, 4) if valor > 0 else 0
            x0 = etiqueta_ancho
            self.canvas.create_rectangle(x0, y, x0 + max(largo, 2), y + alto_barra,
                                          fill=color, width=0)
            self.canvas.create_text(x0 + largo + 22, y + alto_barra / 2, text=str(valor),
                                     fill="#F9FAFB", font=("Segoe UI", 10, "bold"))
            y += alto_barra + 10


class GraficoDonut(ctk.CTkFrame):
    """Mini gráfico circular (donut) dibujado a mano con Canvas, sin dependencias externas."""

    def __init__(self, master, titulo, **kwargs):
        super().__init__(master, corner_radius=14, fg_color=COLOR_TARJETA, **kwargs)
        ctk.CTkLabel(self, text=titulo, font=ctk.CTkFont(size=15, weight="bold")).pack(
            anchor="w", padx=18, pady=(16, 6))
        self.canvas = tk.Canvas(self, height=170, bg="#1F2937", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=18, pady=(0, 6))
        self.marco_leyenda = ctk.CTkFrame(self, fg_color="transparent")
        self.marco_leyenda.pack(fill="x", padx=18, pady=(0, 14))

    def actualizar(self, datos):
        """datos: lista de tuplas (etiqueta, valor, color)"""
        self.canvas.delete("all")
        for w in self.marco_leyenda.winfo_children():
            w.destroy()

        total = sum(v for _, v, _ in datos)
        cx, cy, r = 85, 85, 60
        if total == 0:
            self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, outline="#374151", width=18)
            self.canvas.create_text(cx, cy, text="Sin datos", fill=COLOR_TEXTO_SECUNDARIO, font=("Segoe UI", 10))
        else:
            inicio = 90
            for etiqueta, valor, color in datos:
                extension = -360 * (valor / total)
                if valor > 0:
                    self.canvas.create_arc(cx - r, cy - r, cx + r, cy + r,
                                            start=inicio, extent=extension,
                                            style="arc", outline=color, width=18)
                inicio += extension
            self.canvas.create_oval(cx - 34, cy - 34, cx + 34, cy + 34, fill="#1F2937", width=0)
            self.canvas.create_text(cx, cy, text=str(total), fill="#F9FAFB", font=("Segoe UI", 16, "bold"))

        for etiqueta, valor, color in datos:
            fila = ctk.CTkFrame(self.marco_leyenda, fg_color="transparent")
            fila.pack(side="left", padx=8)
            punto = ctk.CTkLabel(fila, text="●", text_color=color, font=ctk.CTkFont(size=16))
            punto.pack(side="left")
            ctk.CTkLabel(fila, text=f"{etiqueta}: {valor}", font=ctk.CTkFont(size=11),
                         text_color=COLOR_TEXTO_SECUNDARIO).pack(side="left", padx=(2, 0))


class SeccionDashboard(ctk.CTkFrame):
    def __init__(self, master, gestor):
        super().__init__(master, fg_color="transparent")
        self.gestor = gestor

        ctk.CTkLabel(self, text="Panel General", font=ctk.CTkFont(size=26, weight="bold")).pack(anchor="w", pady=(0, 4))
        ctk.CTkLabel(self, text="Resumen del sistema de alquiler de vehículos",
                     text_color=COLOR_TEXTO_SECUNDARIO).pack(anchor="w", pady=(0, 20))

        marco_tarjetas = ctk.CTkFrame(self, fg_color="transparent")
        marco_tarjetas.pack(fill="x", pady=(0, 16))
        for i in range(4):
            marco_tarjetas.grid_columnconfigure(i, weight=1)

        self.tarjeta_vehiculos = TarjetaResumen(marco_tarjetas, "🚗", "Vehículos en flota", COLOR_PRIMARIO)
        self.tarjeta_disponibles = TarjetaResumen(marco_tarjetas, "✅", "Disponibles ahora", COLOR_EXITO)
        self.tarjeta_clientes = TarjetaResumen(marco_tarjetas, "👤", "Clientes registrados", COLOR_PRIMARIO)
        self.tarjeta_espera = TarjetaResumen(marco_tarjetas, "⏳", "En lista de espera", COLOR_ADVERTENCIA)

        self.tarjeta_vehiculos.grid(row=0, column=0, sticky="nsew", padx=6)
        self.tarjeta_disponibles.grid(row=0, column=1, sticky="nsew", padx=6)
        self.tarjeta_clientes.grid(row=0, column=2, sticky="nsew", padx=6)
        self.tarjeta_espera.grid(row=0, column=3, sticky="nsew", padx=6)

        # ---- Fila de gráficos: llena el espacio vacío con información útil ----
        marco_graficos = ctk.CTkFrame(self, fg_color="transparent")
        marco_graficos.pack(fill="x", pady=(0, 16))
        marco_graficos.grid_columnconfigure(0, weight=1)
        marco_graficos.grid_columnconfigure(1, weight=1)

        self.grafico_categorias = GraficoBarras(marco_graficos, "🚙 Flota por categoría")
        self.grafico_categorias.grid(row=0, column=0, sticky="nsew", padx=(0, 6))

        self.grafico_disponibilidad = GraficoDonut(marco_graficos, "📊 Disponibilidad de la flota")
        self.grafico_disponibilidad.grid(row=0, column=1, sticky="nsew", padx=(6, 0))

        marco_info = ctk.CTkFrame(self, corner_radius=14, fg_color=COLOR_TARJETA)
        marco_info.pack(fill="both", expand=True, pady=(0, 10))
        ctk.CTkLabel(marco_info, text="ℹ️  Acerca del sistema", font=ctk.CTkFont(size=16, weight="bold")).pack(
            anchor="w", padx=20, pady=(18, 8))
        texto = (
            "Este sistema aplica Programación Orientada a Objetos (clase abstracta Vehiculo, herencia en "
            "Automovil/Camioneta/Motocicleta, polimorfismo en el cálculo de costos), estructuras de datos "
            "propias (Lista Enlazada para mantenimiento, Pila para deshacer contratos, Cola FIFO para la "
            "lista de espera de clientes) y algoritmos de ordenamiento (Burbuja, Quick Sort) y búsqueda "
            "(lineal y binaria), todo respaldado por una base de datos SQLite con operaciones CRUD completas."
        )
        ctk.CTkLabel(marco_info, text=texto, wraplength=820, justify="left",
                     text_color=COLOR_TEXTO_SECUNDARIO).pack(anchor="w", padx=20, pady=(0, 20))

    def refrescar(self):
        vehiculos = self.gestor.listar_vehiculos()
        disponibles = [v for v in vehiculos if v.disponible]
        clientes = self.gestor.listar_clientes()
        self.tarjeta_vehiculos.actualizar(len(vehiculos))
        self.tarjeta_disponibles.actualizar(len(disponibles))
        self.tarjeta_clientes.actualizar(len(clientes))
        self.tarjeta_espera.actualizar(len(self.gestor.cola_espera))

        # Datos para el gráfico de barras (conteo por categoría)
        conteo_categorias = {"Automóvil": 0, "Camioneta": 0, "Motocicleta": 0}
        for v in vehiculos:
            if v.categoria() in conteo_categorias:
                conteo_categorias[v.categoria()] += 1
        colores_categoria = {"Automóvil": COLOR_PRIMARIO, "Camioneta": COLOR_ADVERTENCIA, "Motocicleta": COLOR_EXITO}
        datos_barras = [(f"{ICONOS_CATEGORIA[c]} {c}", conteo_categorias[c], colores_categoria[c])
                         for c in conteo_categorias]
        self.grafico_categorias.actualizar(datos_barras)

        # Datos para el gráfico donut (disponibles vs alquilados)
        n_disponibles = len(disponibles)
        n_alquilados = len(vehiculos) - n_disponibles
        datos_donut = [("Disponibles", n_disponibles, COLOR_EXITO), ("Alquilados", n_alquilados, COLOR_PELIGRO)]
        self.grafico_disponibilidad.actualizar(datos_donut)

# SECCIÓN: VEHÍCULOS
class SeccionVehiculos(ctk.CTkFrame):
    def __init__(self, master, gestor):
        super().__init__(master, fg_color="transparent")
        self.gestor = gestor
        self._construir_encabezado()
        self._construir_formulario()
        self._construir_tabla()
        self._construir_acciones()
        self.refrescar()

    def _construir_encabezado(self):
        ctk.CTkLabel(self, text="Gestión de Vehículos", font=ctk.CTkFont(size=26, weight="bold")).pack(
            anchor="w", pady=(0, 14))

    def _construir_formulario(self):
        marco = ctk.CTkFrame(self, corner_radius=14, fg_color=COLOR_TARJETA)
        marco.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(marco, text="Registrar / Editar Vehículo", font=ctk.CTkFont(size=15, weight="bold")).grid(
            row=0, column=0, columnspan=8, sticky="w", padx=16, pady=(14, 8))

        self.var_tipo = tk.StringVar(value="Automovil")
        self.var_placa = tk.StringVar()
        self.var_marca = tk.StringVar()
        self.var_modelo = tk.StringVar()
        self.var_anio = tk.StringVar()
        self.var_tarifa = tk.StringVar()
        self.var_extra = tk.StringVar()

        ctk.CTkLabel(marco, text="Tipo").grid(row=1, column=0, padx=(16, 6), pady=6, sticky="e")
        ctk.CTkOptionMenu(marco, values=["Automovil", "Camioneta", "Motocicleta"],
                          variable=self.var_tipo, width=140).grid(row=1, column=1, padx=6, pady=6)

        ctk.CTkLabel(marco, text="Placa").grid(row=1, column=2, padx=6, pady=6, sticky="e")
        ctk.CTkEntry(marco, textvariable=self.var_placa, width=110).grid(row=1, column=3, padx=6, pady=6)

        ctk.CTkLabel(marco, text="Marca").grid(row=1, column=4, padx=6, pady=6, sticky="e")
        ctk.CTkEntry(marco, textvariable=self.var_marca, width=110).grid(row=1, column=5, padx=6, pady=6)

        ctk.CTkLabel(marco, text="Modelo").grid(row=1, column=6, padx=6, pady=6, sticky="e")
        ctk.CTkEntry(marco, textvariable=self.var_modelo, width=110).grid(row=1, column=7, padx=(6, 16), pady=6)

        ctk.CTkLabel(marco, text="Año").grid(row=2, column=0, padx=(16, 6), pady=6, sticky="e")
        ctk.CTkEntry(marco, textvariable=self.var_anio, width=140).grid(row=2, column=1, padx=6, pady=6)

        ctk.CTkLabel(marco, text="Tarifa/día $").grid(row=2, column=2, padx=6, pady=6, sticky="e")
        ctk.CTkEntry(marco, textvariable=self.var_tarifa, width=110).grid(row=2, column=3, padx=6, pady=6)

        ctk.CTkLabel(marco, text="Puertas/Carga/CC").grid(row=2, column=4, padx=6, pady=6, sticky="e")
        ctk.CTkEntry(marco, textvariable=self.var_extra, width=110).grid(row=2, column=5, padx=6, pady=6)

        marco_btn = ctk.CTkFrame(marco, fg_color="transparent")
        marco_btn.grid(row=3, column=0, columnspan=8, pady=(8, 16), padx=16, sticky="w")
        ctk.CTkButton(marco_btn, text="➕ Agregar", fg_color=COLOR_EXITO, hover_color=COLOR_EXITO_HOVER,
                      command=self._agregar).pack(side="left", padx=4)
        ctk.CTkButton(marco_btn, text="✏️ Actualizar", command=self._actualizar).pack(side="left", padx=4)
        ctk.CTkButton(marco_btn, text="🗑️ Eliminar", fg_color=COLOR_PELIGRO, hover_color=COLOR_PELIGRO_HOVER,
                      command=self._eliminar).pack(side="left", padx=4)
        ctk.CTkButton(marco_btn, text="🧹 Limpiar", fg_color="transparent", border_width=1,
                      command=self._limpiar_campos).pack(side="left", padx=4)

    def _construir_tabla(self):
        marco = ctk.CTkFrame(self, corner_radius=14, fg_color=COLOR_TARJETA)
        marco.pack(fill="both", expand=True, pady=(0, 12))
        ctk.CTkLabel(marco, text="Flota Registrada", font=ctk.CTkFont(size=15, weight="bold")).pack(
            anchor="w", padx=16, pady=(14, 6))

        marco_tabla = ctk.CTkFrame(marco, fg_color="transparent")
        marco_tabla.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        columnas = ("id", "tipo", "placa", "marca", "modelo", "anio", "tarifa", "estado")
        self.tabla = ttk.Treeview(marco_tabla, columns=columnas, show="headings", height=9)
        titulos = {"id": "ID", "tipo": "Tipo", "placa": "Placa", "marca": "Marca",
                   "modelo": "Modelo", "anio": "Año", "tarifa": "Tarifa/día", "estado": "Estado"}
        anchos = {"id": 40, "tipo": 110, "placa": 90, "marca": 110, "modelo": 110, "anio": 60, "tarifa": 90, "estado": 100}
        for c in columnas:
            self.tabla.heading(c, text=titulos[c])
            self.tabla.column(c, width=anchos[c], anchor="center")
        self.tabla.pack(fill="both", expand=True, side="left")

        scroll = ttk.Scrollbar(marco_tabla, orient="vertical", command=self.tabla.yview)
        scroll.pack(side="right", fill="y")
        self.tabla.configure(yscrollcommand=scroll.set)
        self.tabla.bind("<<TreeviewSelect>>", self._on_seleccion)

    def _construir_acciones(self):
        marco = ctk.CTkFrame(self, corner_radius=14, fg_color=COLOR_TARJETA)
        marco.pack(fill="x")
        ctk.CTkLabel(marco, text="Ordenamiento, Búsqueda y Mantenimiento",
                     font=ctk.CTkFont(size=15, weight="bold")).grid(row=0, column=0, columnspan=8, sticky="w",
                                                                     padx=16, pady=(14, 8))

        etiqueta_kwargs = dict(font=ctk.CTkFont(size=11), text_color=COLOR_TEXTO_SECUNDARIO)

        # ---- Fila de leyendas (indican qué hace / qué campo usa cada control) ----
        ctk.CTkLabel(marco, text="Ordenar por tarifa", **etiqueta_kwargs).grid(
            row=1, column=0, padx=(16, 6), sticky="w")
        ctk.CTkLabel(marco, text="Ordenar por tarifa", **etiqueta_kwargs).grid(
            row=1, column=1, padx=6, sticky="w")
        ctk.CTkLabel(marco, text="Restaurar", **etiqueta_kwargs).grid(
            row=1, column=2, padx=6, sticky="w")
        ctk.CTkLabel(marco, text="Buscar por placa", **etiqueta_kwargs).grid(
            row=1, column=3, padx=6, sticky="w")
        ctk.CTkLabel(marco, text="Buscar por tarifa", **etiqueta_kwargs).grid(
            row=1, column=5, padx=6, sticky="w")

        # ---- Fila de controles ----
        ctk.CTkButton(marco, text="⬆️ Quick Sort",
                      command=lambda: self._ordenar(True)).grid(row=2, column=0, padx=(16, 6), pady=(2, 16))
        ctk.CTkButton(marco, text="⬆️ Burbuja",
                      command=lambda: self._ordenar(False)).grid(row=2, column=1, padx=6, pady=(2, 16))
        ctk.CTkButton(marco, text="🔄 Orden original", fg_color="transparent", border_width=1,
                      command=self.refrescar).grid(row=2, column=2, padx=6, pady=(2, 16))

        self.var_buscar_placa = tk.StringVar()
        ctk.CTkEntry(marco, textvariable=self.var_buscar_placa, placeholder_text="Ej: GYE-1234",
                     width=130).grid(row=2, column=3, padx=6, pady=(2, 16))
        ctk.CTkButton(marco, text="🔎 Buscar (lineal)", command=self._buscar_placa).grid(
            row=2, column=4, padx=6, pady=(2, 16))

        self.var_buscar_tarifa = tk.StringVar()
        ctk.CTkEntry(marco, textvariable=self.var_buscar_tarifa, placeholder_text="Ej: 35.00",
                     width=100).grid(row=2, column=5, padx=6, pady=(2, 16))
        ctk.CTkButton(marco, text="🔎 Buscar (binaria)", command=self._buscar_tarifa).grid(
            row=2, column=6, padx=(6, 16), pady=(2, 16))

    # ---------------- lógica ----------------
    def refrescar(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        for v in self.gestor.listar_vehiculos():
            icono = ICONOS_CATEGORIA.get(v.categoria(), "")
            estado = "✅ Disponible" if v.disponible else "🔒 Alquilado"
            self.tabla.insert("", "end", iid=str(v.id),
                               values=(v.id, f"{icono} {v.categoria()}", v.placa, v.marca, v.modelo, v.anio,
                                       f"${v.tarifa_diaria:.2f}", estado))

    def _on_seleccion(self, event):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        valores = self.tabla.item(seleccion[0], "values")
        _id, tipo, placa, marca, modelo, anio, tarifa, estado = valores
        tipo_limpio = tipo.split(" ", 1)[-1]
        self.var_tipo.set("Automovil" if tipo_limpio == "Automóvil" else tipo_limpio)
        self.var_placa.set(placa)
        self.var_marca.set(marca)
        self.var_modelo.set(modelo)
        self.var_anio.set(anio)
        self.var_tarifa.set(tarifa.replace("$", ""))

    def _obtener_seleccionado_id(self):
        seleccion = self.tabla.selection()
        return int(seleccion[0]) if seleccion else None

    def _limpiar_campos(self):
        self.var_placa.set(""); self.var_marca.set(""); self.var_modelo.set("")
        self.var_anio.set(""); self.var_tarifa.set(""); self.var_extra.set("")

    def _validar_formulario(self):
        if not self.var_placa.get().strip() or not self.var_marca.get().strip():
            messagebox.showwarning("Datos incompletos", "Placa y Marca son obligatorios.")
            return False
        try:
            int(self.var_anio.get())
            float(self.var_tarifa.get())
        except ValueError:
            messagebox.showwarning("Datos inválidos", "Año y Tarifa deben ser numéricos.")
            return False
        extra = self.var_extra.get().strip()          # Valor de "Puertas/Carga/CC" (puede quedar vacío y tomar un valor por defecto)
        if extra:
            try:
                if self.var_tipo.get() == "Camioneta": # La Camioneta admite decimales (capacidad de carga en kg)
                    float(extra)
                else:                                   # Automovil (puertas) y Motocicleta (cilindraje) deben ser enteros
                    int(float(extra))
            except ValueError:
                messagebox.showwarning("Datos inválidos", "Puertas/Carga/CC debe ser numérico.")
                return False
        return True

    def _convertir_extra(self):
        """Convierte el campo Puertas/Carga/CC al tipo correcto según el tipo de vehículo seleccionado."""
        extra = self.var_extra.get().strip() or "0"
        if self.var_tipo.get() == "Camioneta":
            return float(extra)                         # Camioneta: capacidad de carga en kg (decimal)
        return int(float(extra))                        # Automovil: num. de puertas / Motocicleta: cilindraje (entero)

    def _agregar(self):
        if not self._validar_formulario():
            return
        extra = self._convertir_extra()
        try:
            self.gestor.registrar_vehiculo(
                self.var_tipo.get(), self.var_placa.get().strip().upper(),
                self.var_marca.get().strip(), self.var_modelo.get().strip(),
                int(self.var_anio.get()), float(self.var_tarifa.get()), extra)
            self.refrescar()
            self._limpiar_campos()
            messagebox.showinfo("Éxito", "Vehículo registrado correctamente.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Placa duplicada", "Ya existe un vehículo registrado con esa placa.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el vehículo:\n{e}")

    def _actualizar(self):
        id_sel = self._obtener_seleccionado_id()
        if id_sel is None:
            messagebox.showwarning("Selección requerida", "Selecciona un vehículo de la tabla.")
            return
        if not self._validar_formulario():
            return
        vehiculo = self.gestor.bd.obtener_vehiculo(id_sel)
        if not vehiculo:
            return
        vehiculo.placa = self.var_placa.get().strip().upper()
        vehiculo.marca = self.var_marca.get().strip()
        vehiculo.modelo = self.var_modelo.get().strip()
        vehiculo.anio = int(self.var_anio.get())
        vehiculo.tarifa_diaria = float(self.var_tarifa.get())
        self.gestor.actualizar_vehiculo(vehiculo)
        self.refrescar()
        messagebox.showinfo("Éxito", "Vehículo actualizado correctamente.")

    def _eliminar(self):
        id_sel = self._obtener_seleccionado_id()
        if id_sel is None:
            messagebox.showwarning("Selección requerida", "Selecciona un vehículo de la tabla.")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar el vehículo seleccionado?"):
            self.gestor.eliminar_vehiculo(id_sel)
            self.refrescar()
            self._limpiar_campos()

    def _ordenar(self, avanzado):
        vehiculos = self.gestor.vehiculos_ordenados_por_tarifa(avanzado=avanzado)
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        for v in vehiculos:
            icono = ICONOS_CATEGORIA.get(v.categoria(), "")
            estado = "✅ Disponible" if v.disponible else "🔒 Alquilado"
            self.tabla.insert("", "end", iid=str(v.id),
                               values=(v.id, f"{icono} {v.categoria()}", v.placa, v.marca, v.modelo, v.anio,
                                       f"${v.tarifa_diaria:.2f}", estado))
        algoritmo = "Quick Sort" if avanzado else "Burbuja"
        messagebox.showinfo("Ordenado", f"Vehículos ordenados por tarifa usando {algoritmo}.")

    def _buscar_placa(self):
        placa = self.var_buscar_placa.get().strip()
        if not placa:
            return
        idx, vehiculo = self.gestor.buscar_vehiculo_por_placa_lineal(placa)
        if vehiculo:
            messagebox.showinfo("Búsqueda lineal", f"Encontrado en posición {idx}:\n{vehiculo}")
            self.tabla.selection_set(str(vehiculo.id))
            self.tabla.see(str(vehiculo.id))
        else:
            messagebox.showinfo("Búsqueda lineal", "No se encontró ningún vehículo con esa placa.")

    def _buscar_tarifa(self):
        try:
            tarifa = float(self.var_buscar_tarifa.get())
        except ValueError:
            messagebox.showwarning("Dato inválido", "Ingresa una tarifa numérica.")
            return
        idx, vehiculo = self.gestor.buscar_vehiculo_por_tarifa_binaria(tarifa)
        if vehiculo:
            messagebox.showinfo("Búsqueda binaria", f"Encontrado en posición {idx} (lista ordenada):\n{vehiculo}")
        else:
            messagebox.showinfo("Búsqueda binaria", "No se encontró ningún vehículo con esa tarifa exacta.")

# SECCIÓN: CLIENTES
class SeccionClientes(ctk.CTkFrame):
    def __init__(self, master, gestor):
        super().__init__(master, fg_color="transparent")
        self.gestor = gestor
        ctk.CTkLabel(self, text="Gestión de Clientes", font=ctk.CTkFont(size=26, weight="bold")).pack(
            anchor="w", pady=(0, 14))
        self._construir_formulario()
        self._construir_tabla()
        self.refrescar()

    def _construir_formulario(self):
        marco = ctk.CTkFrame(self, corner_radius=14, fg_color=COLOR_TARJETA)
        marco.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(marco, text="Registrar / Editar Cliente", font=ctk.CTkFont(size=15, weight="bold")).grid(
            row=0, column=0, columnspan=8, sticky="w", padx=16, pady=(14, 8))

        self.var_cedula = tk.StringVar()
        self.var_nombre = tk.StringVar()
        self.var_telefono = tk.StringVar()
        self.var_correo = tk.StringVar()

        ctk.CTkLabel(marco, text="Cédula").grid(row=1, column=0, padx=(16, 6), pady=6, sticky="e")
        ctk.CTkEntry(marco, textvariable=self.var_cedula, width=130).grid(row=1, column=1, padx=6, pady=6)
        ctk.CTkLabel(marco, text="Nombre").grid(row=1, column=2, padx=6, pady=6, sticky="e")
        ctk.CTkEntry(marco, textvariable=self.var_nombre, width=160).grid(row=1, column=3, padx=6, pady=6)
        ctk.CTkLabel(marco, text="Teléfono").grid(row=1, column=4, padx=6, pady=6, sticky="e")
        ctk.CTkEntry(marco, textvariable=self.var_telefono, width=120).grid(row=1, column=5, padx=6, pady=6)
        ctk.CTkLabel(marco, text="Correo").grid(row=1, column=6, padx=6, pady=6, sticky="e")
        ctk.CTkEntry(marco, textvariable=self.var_correo, width=160).grid(row=1, column=7, padx=(6, 16), pady=6)

        marco_btn = ctk.CTkFrame(marco, fg_color="transparent")
        marco_btn.grid(row=2, column=0, columnspan=8, pady=(8, 8), padx=16, sticky="w")
        ctk.CTkButton(marco_btn, text="➕ Agregar", fg_color=COLOR_EXITO, hover_color=COLOR_EXITO_HOVER,
                      command=self._agregar).pack(side="left", padx=4)
        ctk.CTkButton(marco_btn, text="✏️ Actualizar", command=self._actualizar).pack(side="left", padx=4)
        ctk.CTkButton(marco_btn, text="🗑️ Eliminar", fg_color=COLOR_PELIGRO, hover_color=COLOR_PELIGRO_HOVER,
                      command=self._eliminar).pack(side="left", padx=4)
        ctk.CTkButton(marco_btn, text="🔤 Ordenar por nombre (Burbuja)", command=self._ordenar).pack(side="left", padx=4)
        ctk.CTkButton(marco_btn, text="🔄 Orden original", fg_color="transparent", border_width=1,
                      command=self.refrescar).pack(side="left", padx=4)

        marco_buscar = ctk.CTkFrame(marco, fg_color="transparent")
        marco_buscar.grid(row=3, column=0, columnspan=8, pady=(0, 16), padx=16, sticky="w")
        ctk.CTkLabel(marco_buscar, text="Buscar por cédula:", font=ctk.CTkFont(size=11),
                     text_color=COLOR_TEXTO_SECUNDARIO).pack(side="left", padx=(0, 6))
        self.var_buscar_cedula = tk.StringVar()
        ctk.CTkEntry(marco_buscar, textvariable=self.var_buscar_cedula, placeholder_text="Ej: 0912345678",
                     width=160).pack(side="left", padx=(0, 6))
        ctk.CTkButton(marco_buscar, text="🔎 Buscar (lineal)", command=self._buscar).pack(side="left", padx=4)

    def _construir_tabla(self):
        marco = ctk.CTkFrame(self, corner_radius=14, fg_color=COLOR_TARJETA)
        marco.pack(fill="both", expand=True)
        ctk.CTkLabel(marco, text="Clientes Registrados", font=ctk.CTkFont(size=15, weight="bold")).pack(
            anchor="w", padx=16, pady=(14, 6))

        marco_tabla = ctk.CTkFrame(marco, fg_color="transparent")
        marco_tabla.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        columnas = ("id", "cedula", "nombre", "telefono", "correo")
        self.tabla = ttk.Treeview(marco_tabla, columns=columnas, show="headings", height=12)
        titulos = {"id": "ID", "cedula": "Cédula", "nombre": "Nombre", "telefono": "Teléfono", "correo": "Correo"}
        for c in columnas:
            self.tabla.heading(c, text=titulos[c])
            self.tabla.column(c, width=150, anchor="center")
        self.tabla.pack(fill="both", expand=True, side="left")

        scroll = ttk.Scrollbar(marco_tabla, orient="vertical", command=self.tabla.yview)
        scroll.pack(side="right", fill="y")
        self.tabla.configure(yscrollcommand=scroll.set)
        self.tabla.bind("<<TreeviewSelect>>", self._on_seleccion)

    def refrescar(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        for c in self.gestor.listar_clientes():
            self.tabla.insert("", "end", iid=str(c.id), values=(c.id, c.cedula, c.nombre, c.telefono, c.correo))

    def _on_seleccion(self, event):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        _id, cedula, nombre, tel, correo = self.tabla.item(seleccion[0], "values")
        self.var_cedula.set(cedula); self.var_nombre.set(nombre)
        self.var_telefono.set(tel); self.var_correo.set(correo)

    def _obtener_seleccionado_id(self):
        seleccion = self.tabla.selection()
        return int(seleccion[0]) if seleccion else None

    def _agregar(self):
        if not self.var_cedula.get().strip() or not self.var_nombre.get().strip():
            messagebox.showwarning("Datos incompletos", "Cédula y Nombre son obligatorios.")
            return
        try:
            self.gestor.registrar_cliente(self.var_cedula.get().strip(), self.var_nombre.get().strip(),
                                           self.var_telefono.get().strip(), self.var_correo.get().strip())
            self.refrescar()
            messagebox.showinfo("Éxito", "Cliente registrado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar (¿cédula duplicada?):\n{e}")

    def _actualizar(self):
        id_sel = self._obtener_seleccionado_id()
        if id_sel is None:
            messagebox.showwarning("Selección requerida", "Selecciona un cliente de la tabla.")
            return
        cliente = self.gestor.bd.obtener_cliente(id_sel)
        cliente.cedula = self.var_cedula.get().strip()
        cliente.nombre = self.var_nombre.get().strip()
        cliente.telefono = self.var_telefono.get().strip()
        cliente.correo = self.var_correo.get().strip()
        self.gestor.actualizar_cliente(cliente)
        self.refrescar()
        messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")

    def _eliminar(self):
        id_sel = self._obtener_seleccionado_id()
        if id_sel is None:
            messagebox.showwarning("Selección requerida", "Selecciona un cliente de la tabla.")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar el cliente seleccionado?"):
            self.gestor.eliminar_cliente(id_sel)
            self.refrescar()

    def _ordenar(self):
        clientes = self.gestor.clientes_ordenados_por_nombre()
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        for c in clientes:
            self.tabla.insert("", "end", iid=str(c.id), values=(c.id, c.cedula, c.nombre, c.telefono, c.correo))
        messagebox.showinfo("Ordenado", "Clientes ordenados alfabéticamente por nombre (Burbuja).")

    def _buscar(self):
        cedula = self.var_buscar_cedula.get().strip()
        if not cedula:
            return
        idx, cliente = self.gestor.buscar_cliente_por_cedula_lineal(cedula)
        if cliente:
            messagebox.showinfo("Búsqueda lineal", f"Encontrado en posición {idx}:\n{cliente}")
            self.tabla.selection_set(str(cliente.id))
            self.tabla.see(str(cliente.id))
        else:
            messagebox.showinfo("Búsqueda lineal", "No se encontró ningún cliente con esa cédula.")

# SECCIÓN: ALQUILERES 
class SeccionAlquileres(ctk.CTkFrame):
    def __init__(self, master, gestor, refrescar_callback):
        super().__init__(master, fg_color="transparent")
        self.gestor = gestor
        self.refrescar_callback = refrescar_callback
        ctk.CTkLabel(self, text="Solicitudes de Alquiler", font=ctk.CTkFont(size=26, weight="bold")).pack(
            anchor="w", pady=(0, 14))
        self._construir_formulario()
        self._construir_cola()

    def _construir_formulario(self):
        marco = ctk.CTkFrame(self, corner_radius=14, fg_color=COLOR_TARJETA)
        marco.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(marco, text="Nueva Solicitud", font=ctk.CTkFont(size=15, weight="bold")).grid(
            row=0, column=0, columnspan=8, sticky="w", padx=16, pady=(14, 8))

        self.var_id_cliente = tk.StringVar()
        self.var_categoria = tk.StringVar(value="Automóvil")
        self.var_dias = tk.StringVar(value="1")
        self.var_seguro = tk.BooleanVar()

        ctk.CTkLabel(marco, text="ID Cliente").grid(row=1, column=0, padx=(16, 6), pady=6, sticky="e")
        ctk.CTkEntry(marco, textvariable=self.var_id_cliente, placeholder_text="Ej: 1", width=80).grid(
            row=1, column=1, padx=6, pady=6)

        ctk.CTkLabel(marco, text="Categoría").grid(row=1, column=2, padx=6, pady=6, sticky="e")
        ctk.CTkOptionMenu(marco, values=["Automóvil", "Camioneta", "Motocicleta"],
                          variable=self.var_categoria, width=140).grid(row=1, column=3, padx=6, pady=6)

        ctk.CTkLabel(marco, text="Días").grid(row=1, column=4, padx=6, pady=6, sticky="e")
        ctk.CTkEntry(marco, textvariable=self.var_dias, width=60).grid(row=1, column=5, padx=6, pady=6)

        ctk.CTkCheckBox(marco, text="Con seguro (+10%)", variable=self.var_seguro).grid(
            row=1, column=6, padx=10, pady=6)

        ctk.CTkButton(marco, text="🚀 Solicitar Alquiler", fg_color=COLOR_EXITO, hover_color=COLOR_EXITO_HOVER,
                      command=self._solicitar).grid(row=1, column=7, padx=(6, 16), pady=6)

        marco_btn = ctk.CTkFrame(marco, fg_color="transparent")
        marco_btn.grid(row=2, column=0, columnspan=8, pady=(4, 16), padx=16, sticky="w")
        ctk.CTkButton(marco_btn, text="↩️ Deshacer último contrato (Pila LIFO)", fg_color=COLOR_ADVERTENCIA,
                      hover_color=COLOR_ADVERTENCIA_HOVER, command=self._deshacer).pack(side="left", padx=4)
        ctk.CTkButton(marco_btn, text="▶️ Atender siguiente en espera (Cola FIFO)",
                      command=self._atender_espera).pack(side="left", padx=4)

    def _construir_cola(self):
        marco = ctk.CTkFrame(self, corner_radius=14, fg_color=COLOR_TARJETA)
        marco.pack(fill="both", expand=True)
        ctk.CTkLabel(marco, text="Cola de Espera de Clientes (FIFO)", font=ctk.CTkFont(size=15, weight="bold")).pack(
            anchor="w", padx=16, pady=(14, 6))

        marco_tabla = ctk.CTkFrame(marco, fg_color="transparent")
        marco_tabla.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        columnas = ("posicion", "id_cliente", "categoria", "dias", "seguro", "fecha")
        self.tabla_cola = ttk.Treeview(marco_tabla, columns=columnas, show="headings", height=8)
        titulos = {"posicion": "Pos.", "id_cliente": "ID Cliente", "categoria": "Categoría",
                   "dias": "Días", "seguro": "Seguro", "fecha": "Fecha Solicitud"}
        for c in columnas:
            self.tabla_cola.heading(c, text=titulos[c])
            self.tabla_cola.column(c, width=130, anchor="center")
        self.tabla_cola.pack(fill="both", expand=True)

    def refrescar(self):
        for fila in self.tabla_cola.get_children():
            self.tabla_cola.delete(fila)
        for i, solicitud in enumerate(self.gestor.cola_espera.a_lista_python(), start=1):
            self.tabla_cola.insert("", "end", values=(i, solicitud["id_cliente"], solicitud["categoria"],
                                                       solicitud["dias"], solicitud["con_seguro"],
                                                       solicitud["fecha_solicitud"]))

    def _solicitar(self):
        try:
            id_cliente = int(self.var_id_cliente.get())
            dias = int(self.var_dias.get())
        except ValueError:
            messagebox.showwarning("Datos inválidos", "ID Cliente y Días deben ser numéricos.")
            return
        if not self.gestor.bd.obtener_cliente(id_cliente):
            messagebox.showwarning("Cliente no existe", "No existe un cliente con ese ID.")
            return
        contrato, mensaje = self.gestor.solicitar_alquiler(
            id_cliente, self.var_categoria.get(), dias, con_seguro=self.var_seguro.get())
        messagebox.showinfo("Resultado", mensaje)
        self.refrescar_callback()

    def _deshacer(self):
        contrato, mensaje = self.gestor.deshacer_ultimo_contrato()
        messagebox.showinfo("Deshacer contrato", mensaje)
        self.refrescar_callback()

    def _atender_espera(self):
        contrato, mensaje = self.gestor.atender_siguiente_en_espera()
        messagebox.showinfo("Atender espera", mensaje)
        self.refrescar_callback()

# SECCIÓN: MANTENIMIENTO
class SeccionMantenimiento(ctk.CTkFrame):
    def __init__(self, master, gestor):
        super().__init__(master, fg_color="transparent")
        self.gestor = gestor
        self.id_vehiculo_seleccionado = None

        ctk.CTkLabel(self, text="Historial de Mantenimiento", font=ctk.CTkFont(size=26, weight="bold")).pack(
            anchor="w", pady=(0, 4))
        ctk.CTkLabel(self, text="Selecciona un vehículo para ver o registrar su mantenimiento (Lista Enlazada)",
                     text_color=COLOR_TEXTO_SECUNDARIO).pack(anchor="w", pady=(0, 14))

        marco_principal = ctk.CTkFrame(self, fg_color="transparent")
        marco_principal.pack(fill="both", expand=True)
        marco_principal.grid_columnconfigure(0, weight=1)
        marco_principal.grid_columnconfigure(1, weight=2)
        marco_principal.grid_rowconfigure(0, weight=1)

        self._construir_lista_vehiculos(marco_principal)
        self._construir_panel_historial(marco_principal)

    def _construir_lista_vehiculos(self, master):
        marco = ctk.CTkFrame(master, corner_radius=14, fg_color=COLOR_TARJETA)
        marco.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        ctk.CTkLabel(marco, text="Vehículos de la flota", font=ctk.CTkFont(size=15, weight="bold")).pack(
            anchor="w", padx=16, pady=(14, 6))
        ctk.CTkLabel(marco, text="Selecciona una fila", font=ctk.CTkFont(size=11),
                     text_color=COLOR_TEXTO_SECUNDARIO).pack(anchor="w", padx=16, pady=(0, 6))

        marco_tabla = ctk.CTkFrame(marco, fg_color="transparent")
        marco_tabla.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        columnas = ("id", "placa", "vehiculo")
        self.tabla_vehiculos = ttk.Treeview(marco_tabla, columns=columnas, show="headings", height=16)
        self.tabla_vehiculos.heading("id", text="ID")
        self.tabla_vehiculos.heading("placa", text="Placa")
        self.tabla_vehiculos.heading("vehiculo", text="Vehículo")
        self.tabla_vehiculos.column("id", width=40, anchor="center")
        self.tabla_vehiculos.column("placa", width=90, anchor="center")
        self.tabla_vehiculos.column("vehiculo", width=160, anchor="w")
        self.tabla_vehiculos.pack(fill="both", expand=True, side="left")

        scroll = ttk.Scrollbar(marco_tabla, orient="vertical", command=self.tabla_vehiculos.yview)
        scroll.pack(side="right", fill="y")
        self.tabla_vehiculos.configure(yscrollcommand=scroll.set)
        self.tabla_vehiculos.bind("<<TreeviewSelect>>", self._on_seleccionar_vehiculo)

    def _construir_panel_historial(self, master):
        marco = ctk.CTkFrame(master, corner_radius=14, fg_color=COLOR_TARJETA)
        marco.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        self.lbl_vehiculo_actual = ctk.CTkLabel(marco, text="Ningún vehículo seleccionado",
                                                 font=ctk.CTkFont(size=15, weight="bold"))
        self.lbl_vehiculo_actual.pack(anchor="w", padx=16, pady=(14, 10))

        marco_form = ctk.CTkFrame(marco, fg_color="transparent")
        marco_form.pack(fill="x", padx=16, pady=(0, 10))
        ctk.CTkLabel(marco_form, text="Nuevo registro de mantenimiento:", font=ctk.CTkFont(size=11),
                     text_color=COLOR_TEXTO_SECUNDARIO).pack(anchor="w", pady=(0, 4))
        marco_form_fila = ctk.CTkFrame(marco_form, fg_color="transparent")
        marco_form_fila.pack(fill="x")
        self.var_descripcion = tk.StringVar()
        self.entry_descripcion = ctk.CTkEntry(marco_form_fila, textvariable=self.var_descripcion,
                                               placeholder_text="Ej: Cambio de aceite y filtros")
        self.entry_descripcion.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.btn_agregar = ctk.CTkButton(marco_form_fila, text="➕ Registrar", fg_color=COLOR_EXITO,
                                          hover_color=COLOR_EXITO_HOVER, command=self._agregar_mantenimiento,
                                          state="disabled")
        self.btn_agregar.pack(side="left")

        ctk.CTkLabel(marco, text="Historial (Lista Enlazada, orden de registro)",
                     font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=16, pady=(6, 6))

        marco_tabla = ctk.CTkFrame(marco, fg_color="transparent")
        marco_tabla.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        columnas = ("fecha", "descripcion")
        self.tabla_historial = ttk.Treeview(marco_tabla, columns=columnas, show="headings", height=12)
        self.tabla_historial.heading("fecha", text="Fecha")
        self.tabla_historial.heading("descripcion", text="Descripción")
        self.tabla_historial.column("fecha", width=100, anchor="center")
        self.tabla_historial.column("descripcion", width=320, anchor="w")
        self.tabla_historial.pack(fill="both", expand=True, side="left")

        scroll = ttk.Scrollbar(marco_tabla, orient="vertical", command=self.tabla_historial.yview)
        scroll.pack(side="right", fill="y")
        self.tabla_historial.configure(yscrollcommand=scroll.set)

    # ---------------- lógica ----------------
    def refrescar(self):
        for fila in self.tabla_vehiculos.get_children():
            self.tabla_vehiculos.delete(fila)
        for v in self.gestor.listar_vehiculos():
            icono = ICONOS_CATEGORIA.get(v.categoria(), "")
            self.tabla_vehiculos.insert("", "end", iid=str(v.id),
                                         values=(v.id, v.placa, f"{icono} {v.marca} {v.modelo}"))
        # Si el vehículo seleccionado ya no existe (fue eliminado), limpiar el panel
        if self.id_vehiculo_seleccionado is not None and \
                not self.gestor.bd.obtener_vehiculo(self.id_vehiculo_seleccionado):
            self.id_vehiculo_seleccionado = None
        if self.id_vehiculo_seleccionado is not None:
            self.tabla_vehiculos.selection_set(str(self.id_vehiculo_seleccionado))
            self._cargar_historial(self.id_vehiculo_seleccionado)

    def _on_seleccionar_vehiculo(self, event):
        seleccion = self.tabla_vehiculos.selection()
        if not seleccion:
            return
        self.id_vehiculo_seleccionado = int(seleccion[0])
        self._cargar_historial(self.id_vehiculo_seleccionado)

    def _cargar_historial(self, id_vehiculo):
        vehiculo = self.gestor.bd.obtener_vehiculo(id_vehiculo)
        if not vehiculo:
            return
        icono = ICONOS_CATEGORIA.get(vehiculo.categoria(), "")
        self.lbl_vehiculo_actual.configure(
            text=f"{icono} {vehiculo.marca} {vehiculo.modelo} — Placa: {vehiculo.placa}")
        self.btn_agregar.configure(state="normal")

        for fila in self.tabla_historial.get_children():
            self.tabla_historial.delete(fila)
        historial = self.gestor.historial_mantenimiento(id_vehiculo)
        if not historial:
            self.tabla_historial.insert("", "end", values=("—", "Sin registros de mantenimiento aún"))
        else:
            for fecha, descripcion in historial:
                self.tabla_historial.insert("", "end", values=(fecha, descripcion))

    def _agregar_mantenimiento(self):
        if self.id_vehiculo_seleccionado is None:
            messagebox.showwarning("Selección requerida", "Selecciona un vehículo primero.")
            return
        descripcion = self.var_descripcion.get().strip()
        if not descripcion:
            messagebox.showwarning("Dato requerido", "Escribe una descripción del mantenimiento.")
            return
        self.gestor.registrar_mantenimiento(self.id_vehiculo_seleccionado, descripcion)
        self.var_descripcion.set("")
        self._cargar_historial(self.id_vehiculo_seleccionado)
        messagebox.showinfo("Éxito", "Mantenimiento registrado en el historial (Lista Enlazada).")

# SECCIÓN: CONTRATOS
class SeccionContratos(ctk.CTkFrame):
    def __init__(self, master, gestor):
        super().__init__(master, fg_color="transparent")
        self.gestor = gestor
        ctk.CTkLabel(self, text="Contratos de Alquiler", font=ctk.CTkFont(size=26, weight="bold")).pack(
            anchor="w", pady=(0, 14))
        self._construir_tabla()
        self.refrescar()

    def _construir_tabla(self):
        marco = ctk.CTkFrame(self, corner_radius=14, fg_color=COLOR_TARJETA)
        marco.pack(fill="both", expand=True)

        marco_tabla = ctk.CTkFrame(marco, fg_color="transparent")
        marco_tabla.pack(fill="both", expand=True, padx=16, pady=(16, 8))

        columnas = ("id", "id_cliente", "id_vehiculo", "fecha", "dias", "costo", "seguro", "estado")
        self.tabla = ttk.Treeview(marco_tabla, columns=columnas, show="headings", height=14)
        titulos = {"id": "ID", "id_cliente": "Cliente", "id_vehiculo": "Vehículo", "fecha": "Fecha Inicio",
                   "dias": "Días", "costo": "Costo Total", "seguro": "Seguro", "estado": "Estado"}
        for c in columnas:
            self.tabla.heading(c, text=titulos[c])
            self.tabla.column(c, width=110, anchor="center")
        self.tabla.pack(fill="both", expand=True, side="left")

        scroll = ttk.Scrollbar(marco_tabla, orient="vertical", command=self.tabla.yview)
        scroll.pack(side="right", fill="y")
        self.tabla.configure(yscrollcommand=scroll.set)

        marco_btn = ctk.CTkFrame(marco, fg_color="transparent")
        marco_btn.pack(pady=(0, 16))
        ctk.CTkButton(marco_btn, text="✅ Finalizar contrato", fg_color=COLOR_EXITO, hover_color=COLOR_EXITO_HOVER,
                      command=self._finalizar).pack(side="left", padx=6)
        ctk.CTkButton(marco_btn, text="🔄 Refrescar", command=self.refrescar).pack(side="left", padx=6)

    def refrescar(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        for c in self.gestor.listar_contratos():
            colores_estado = {"Activo": "🟢", "Finalizado": "⚪", "Cancelado": "🔴"}
            icono_estado = colores_estado.get(c.estado, "")
            self.tabla.insert("", "end", iid=str(c.id),
                               values=(c.id, c.id_cliente, c.id_vehiculo, c.fecha_inicio, c.dias,
                                       f"${c.costo_total:.2f}", "Sí" if c.con_seguro else "No",
                                       f"{icono_estado} {c.estado}"))

    def _finalizar(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Selección requerida", "Selecciona un contrato de la tabla.")
            return
        id_contrato = int(seleccion[0])
        if self.gestor.finalizar_contrato(id_contrato):
            messagebox.showinfo("Éxito", "Contrato finalizado. El vehículo vuelve a estar disponible.")
            self.refrescar()

# PUNTO DE ENTRADA
if __name__ == "__main__":
    app = AplicacionAlquiler()
    app.mainloop()
