# README - C12T1: Implementacion de Estructuras de Datos con Listas Enlazadas
## Archivos

| Archivo                 | Problema                                      |
| `C12T1problema1.py`     | Gestion de procesos del sistema operativo     |
| `C12T1problema2.py`     | Editor de texto basico por lineas             |
| `C12T1problema3.py`     | Sistema de gestion de polinomios              |
| `C12T1problema4.py`     | Hoja de calculo dispersa                      |
| `README.md`             | documentacion                               |

---

## Como ejecutar
No requiere librerias externas. Solo biblioteca estandar de Python 3.

---

## Estructuras de datos

### Problema 1 - Procesos (Lista enlazada simple)

```
NodoProceso
  .proceso   : Proceso           (pid, nombre, estado, t_creacion, t_cpu)
  .siguiente : NodoProceso|None  enlace al siguiente nodo

ListaProcesos
  .cabeza : NodoProceso|None
  .tamano : int
```

Lista simple con recorrido en un solo sentido. Suficiente para todas
las operaciones requeridas ya que no necesitamos retroceder.

### Problema 2 - Editor de texto (Lista doblemente enlazada)

```
NodoLinea
  .texto     : str
  .siguiente : NodoLinea|None   enlace al nodo de la linea siguiente
  .anterior  : NodoLinea|None   enlace al nodo de la linea anterior

EditorTexto
  .cabeza : NodoLinea|None   primera linea
  .cola   : NodoLinea|None   ultima linea
  .tamano : int
```

Lista doble porque la operacion "mover linea" y la eliminacion necesitan
acceso al nodo anterior en O(1) una vez localizado el nodo objetivo.

### Problema 3 - Polinomios (Lista enlazada ordenada)

```
NodoTermino
  .coeficiente : float
  .exponente   : int
  .siguiente   : NodoTermino|None

Polinomio
  .cabeza : NodoTermino|None   termino de mayor exponente
```

La lista se mantiene ordenada de mayor a menor exponente. Esto permite
que la suma de dos polinomios se haga en O(n+m) con un recorrido paralelo
(igual que el merge de merge-sort), sin necesidad de busquedas.

### Problema 4 - Hoja dispersa (Dos listas enlazadas cruzadas)

```
NodoCelda
  .fila     : int
  .columna  : int
  .valor    : float|str
  .sig_fila : NodoCelda|None   siguiente celda en la misma fila
  .sig_col  : NodoCelda|None   siguiente celda en la misma columna

NodoFila    -> cabecera de fila, apunta a la primera celda de esa fila
NodoColumna -> cabecera de columna, apunta a la primera celda de esa columna

HojaCalculo
  .filas    : NodoFila|None    lista de cabeceras de fila
  .columnas : NodoColumna|None lista de cabeceras de columna
  .n_celdas : int
```

Cada celda pertenece simultaneamente a dos listas: la de su fila y la de
su columna. Esto permite recorrer todas las celdas de una fila O(k_f) o de
una columna O(k_c) sin tocar celdas de otras filas o columnas.

---

## Operaciones por problema

### Problema 1

| Metodo                  | Descripcion                                |
| agregar_proceso         |Inserta al final recorriendo hasta la cola  |
| cambiar_estado          |Busqueda lineal por PID                     |
| eliminar_terminados     |Una pasada con nodo centinela               |
| mover_al_inicio         |Desvincula y re-enlaza como cabeza          |
| mostrar_todos           |Recorrido completo                          |
| tiempo_promedio_espera  |Acumulador FCFS en una sola pasada          |


### Problema 3

| Metodo          |Descripcion                                       |
| insertar_termino|Busca posicion correcta o acumula en existente    |
| mostrar         |Recorre y formatea cada termino                   |
| sumar/restar    |Recorrido paralelo (merge), sin busquedas         |
| multiplicar     |Producto cruzado de todos los terminos            |
| evaluar         |Suma coef * x^exp por cada nodo                   |
| derivar         |Regla de la potencia en cada termino              |
| integrar        |Eleva exponente y divide coeficiente              |

### Problema 4

| Metodo          |Descripcion                                |
| insertar        |Enlaza en lista de fila y de columna       |
| eliminar        |Desvincula de ambas listas                 |
| obtener         |Busca en la lista de la fila               |
| sumar_rango     |Solo visita celdas no vacias del rango     |
| eliminar_fila   |Elimina de ambas listas por cada celda     |
| mostrar         |Itera filas x columnas ocupadas            |
| guardar/cargar  |Lee o escribe solo las celdas no vacias    |


---

## Ejemplo de salida esperada

### Problema 1 (fragmento)

```
MENU  |  Procesos en cola: 10
  1. Agregar nuevo proceso al final
  ...
  [ 1] PID:   1  firefox              Estado:listo         CPU:  2400 ms
  [ 2] PID:   2  bash                 Estado:ejecucion     CPU:   100 ms
  [ 3] PID:   3  systemd              Estado:listo         CPU:   800 ms
  ...
  Tiempo promedio de espera (procesos 'listo'): 1600.0 ms
```

### Problema 3 (fragmento)

```
  P1(x) = 3x^4 - 2x^2 + 5
  P2(x) = x^3 + 4x - 1
  P1 + P2 = 3x^4 + x^3 - 2x^2 + 4x + 4
  P1 * P2 = 3x^7 - 2x^5 + 12x^5 - 8x^3 + ...
  d/dx [P1] = 12x^3 - 4x
  P1(2) = 45.0
```

### Problema 4 (fragmento)

```
       Col0       Col1       Col3
  ----------------------------------------
  Fila0| 100.0    200.5
  Fila2|           50.0     999.0
  ----------------------------------------
  Celdas no vacias : 4
  Matriz densa eq  : 12 celdas  (ahorro de memoria: 66.7%)
```