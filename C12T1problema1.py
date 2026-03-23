#librerias
import time as tiempo_sistema

#clases
class Proceso:
    """
    Atributos:
        pid        (int):   Identificador unico autoincremental.
        nombre     (str):   Nombre descriptivo del proceso.
        estado     (str):   Estado actual del proceso.
        t_creacion (float): Marca de tiempo de creacion (epoch).
        t_cpu      (int):   Tiempo de CPU requerido en milisegundos.
    """
    ESTADOS = {"listo", "ejecucion", "bloqueado", "terminado"}

    def __init__(self, pid: int, nombre: str, estado: str, t_cpu: int):
        self.pid        = pid
        self.nombre     = nombre
        self.estado     = estado
        self.t_creacion = tiempo_sistema.time()
        self.t_cpu      = t_cpu

    def __str__(self) -> str:
        marca = tiempo_sistema.strftime(
            "%H:%M:%S", tiempo_sistema.localtime(self.t_creacion)
        )
        return (f"PID:{self.pid:>4}  {self.nombre:<22}  "
                f"Estado:{self.estado:<12}  "
                f"CPU:{self.t_cpu:>6} ms  Creado:{marca}")


class NodoProceso:
    """
    Atributos:
        proceso    (Proceso):          Datos del proceso almacenado en este nodo.
        siguiente  (NodoProceso|None): Referencia al siguiente nodo de la cadena.
                                       None indica que es el ultimo nodo.
    """
    def __init__(self, proceso: Proceso):
        self.proceso   = proceso
        self.siguiente = None          # por defecto no hay nodo siguiente

class ListaProcesos:
    """
    Atributos:
        cabeza (NodoProceso|None): Primer nodo de la lista.
        tamano (int):              Numero de nodos en la lista.

    Invariante: cabeza is None  <=>  tamano == 0
    """
    def __init__(self):
        self.cabeza = None
        self.tamano = 0

#funcion que agrega un nuevo proceso como ultimo nodo a la lista
    def agregar_proceso(self, proceso: Proceso) -> None:
        """
        Parametros:
            proceso (Proceso): Objeto proceso a insertar.
        """
        nuevo = NodoProceso(proceso)
        if self.cabeza is None:
            self.cabeza = nuevo                      # lista estaba vacia
        else:
            actual = self.cabeza
            while actual.siguiente is not None:      # avanzar hasta el ultimo
                actual = actual.siguiente
            actual.siguiente = nuevo                 # enlazar al final
        self.tamano += 1

#funcion que localiza el proceso y cambia el estado
    def cambiar_estado(self, pid: int, nuevo_estado: str) -> bool:
        """
        Parametros:
            pid          (int): Identificador del proceso.
            nuevo_estado (str): Estado destino (debe estar en Proceso.ESTADOS).
        """
        if nuevo_estado not in Proceso.ESTADOS:
            print(f"  [Error] Estado '{nuevo_estado}' no valido.")
            return False

        actual = self.cabeza
        while actual is not None:
            if actual.proceso.pid == pid:
                actual.proceso.estado = nuevo_estado
                return True
            actual = actual.siguiente
        return False

#elimina de la lista todos los nodos cuyo proceso esta terminado
    def eliminar_terminados(self) -> int:
        """
        Retorna:
            int: Cantidad de nodos eliminados.
        """
        centinela          = NodoProceso(None)   # nodo auxiliar temporal
        centinela.siguiente = self.cabeza
        previo             = centinela
        actual             = self.cabeza
        eliminados         = 0

        while actual is not None:
            if actual.proceso.estado == "terminado":
                previo.siguiente = actual.siguiente  # saltar el nodo
                self.tamano     -= 1
                eliminados      += 1
            else:
                previo = actual                      # avanzar previo solo si no se elimino
            actual = actual.siguiente

        self.cabeza = centinela.siguiente            # actualizar cabeza real
        return eliminados

#fucnion que reubica e proceso al inicio de la lista
    def mover_al_inicio(self, pid: int) -> bool:
        """
        Parametros:
            pid (int): PID del proceso a promover.

        Retorna:
            True si el proceso fue encontrado y movido.
            False si el PID no existe.
        """
        if self.cabeza is None:
            return False
        if self.cabeza.proceso.pid == pid:
            return True                              # ya es el primero

        previo = self.cabeza
        actual = self.cabeza.siguiente
        while actual is not None:
            if actual.proceso.pid == pid:
                previo.siguiente = actual.siguiente  # desvincula de su lugar
                actual.siguiente = self.cabeza       # apunta al antiguo primero
                self.cabeza      = actual            # pasa a ser el primero
                return True
            previo = actual
            actual = actual.siguiente
        return False

#fucnion para mostrar todos los proesos
    def mostrar_todos(self) -> None:
        if self.cabeza is None:
            print("  (lista vacia)")
            return
        actual   = self.cabeza
        posicion = 1
        while actual is not None:
            print(f"  [{posicion:>2}] {actual.proceso}")
            actual   = actual.siguiente
            posicion += 1

#funcion que calcula el tiempo promedio de espera de procesos
    def tiempo_promedio_espera(self) -> float:
        """
        Retorna:
            float: Promedio en ms. 0.0 si no hay procesos listos.
        """
        tiempos  = []
        acum     = 0
        actual   = self.cabeza

        while actual is not None:
            if actual.proceso.estado == "listo":
                tiempos.append(acum)
                acum += actual.proceso.t_cpu
            actual = actual.siguiente

        if not tiempos:
            return 0.0
        return round(sum(tiempos) / len(tiempos), 2)

#fucnion que cuenta cuantos procesos hay en cada estado
    def resumen_estados(self) -> dict:
        """
        Retorna:
            dict: {estado (str): cantidad (int)}
        """
        conteo = {e: 0 for e in Proceso.ESTADOS}
        actual = self.cabeza
        while actual is not None:
            conteo[actual.proceso.estado] += 1
            actual = actual.siguiente
        return conteo

_pid_global = 1   # generador de PIDs unicos

def generar_pid() -> int:
    """Devuelve el siguiente PID unico y lo incrementa."""
    global _pid_global
    pid = _pid_global
    _pid_global += 1
    return pid

#funcion que solicita datos del proceso al usuario
def pedir_proceso() -> Proceso:
    """
    Retorna:
        Proceso: Objeto con todos los campos rellenados.
    """
    print("\n  -- Datos del nuevo proceso --")

    nombre = input("  Nombre del proceso      : ").strip()
    if not nombre:
        nombre = "proceso"

    estados_ord = sorted(Proceso.ESTADOS)
    print(f"  Estados validos         : {', '.join(estados_ord)}")
    while True:
        estado = input("  Estado inicial          : ").strip().lower()
        if estado in Proceso.ESTADOS:
            break
        print("  [Error] Estado invalido, intente de nuevo.")

    while True:
        try:
            t_cpu = int(input("  Tiempo de CPU [ms]      : "))
            if t_cpu <= 0:
                print("  [Error] Debe ser un entero positivo.")
                continue
            break
        except ValueError:
            print("  [Error] Ingrese un entero.")

    pid = generar_pid()
    print(f"  PID asignado automaticamente: {pid}")
    return Proceso(pid, nombre, estado, t_cpu)

#funcion principal con menu interactuvi
def main() -> None:

    print("  PROBLEMA 1: GESTION DE PROCESOS - LISTA ENLAZADA SIMPLE")
    print("\n  El enunciado pide al menos 10 procesos.")
    print("  Use la opcion 1 para agregar todos los procesos necesarios.")

    lista = ListaProcesos()

    while True:
        print(f"  MENU  |  Procesos en cola: {lista.tamano}")
        print("  1. Agregar nuevo proceso al final")
        print("  2. Cambiar estado de un proceso")
        print("  3. Eliminar todos los procesos terminados")
        print("  4. Mover proceso al inicio (prioridad maxima)")
        print("  5. Mostrar todos los procesos en orden")
        print("  6. Calcular tiempo promedio de espera")
        print("  7. Ver resumen de estados")
        print("  0. Salir")

        op = input("\n  Opcion: ").strip()

        # --- 1. Agregar ---
        if op == "1":
            p = pedir_proceso()
            lista.agregar_proceso(p)
            print(f"\n  Proceso '{p.nombre}' (PID {p.pid}) agregado al final.")

        # --- 2. Cambiar estado ---
        elif op == "2":
            try:
                pid = int(input("  PID del proceso         : "))
            except ValueError:
                print("  [Error] PID debe ser un entero.")
                continue
            print(f"  Estados validos: {', '.join(sorted(Proceso.ESTADOS))}")
            nuevo = input("  Nuevo estado            : ").strip().lower()
            if lista.cambiar_estado(pid, nuevo):
                print(f"  Estado de PID {pid} cambiado a '{nuevo}'.")
            else:
                print(f"  PID {pid} no encontrado en la lista.")

        # --- 3. Eliminar terminados ---
        elif op == "3":
            n = lista.eliminar_terminados()
            print(f"  {n} proceso(s) con estado 'terminado' eliminado(s).")

        # --- 4. Mover al inicio ---
        elif op == "4":
            try:
                pid = int(input("  PID del proceso a promover: "))
            except ValueError:
                print("  [Error] PID debe ser un entero.")
                continue
            if lista.mover_al_inicio(pid):
                print(f"  PID {pid} movido al inicio de la cola.")
            else:
                print(f"  PID {pid} no encontrado en la lista.")

        # --- 5. Mostrar todos ---
        elif op == "5":
            print("\n  -- Lista de procesos (orden de ejecucion) --")
            lista.mostrar_todos()

        # --- 6. Tiempo promedio espera ---
        elif op == "6":
            prom = lista.tiempo_promedio_espera()
            print(f"\n  Tiempo promedio de espera (procesos 'listo'): {prom} ms")

        # --- 7. Resumen ---
        elif op == "7":
            print("\n  -- Resumen de estados --")
            for estado, cnt in sorted(lista.resumen_estados().items()):
                barra = "#" * cnt
                print(f"    {estado:<12}: {cnt:>3}  {barra}")

        elif op == "0":
            print("\n  Gestor de procesos cerrado.")
            break
        else:
            print("  Opcion invalida, intente de nuevo.")


if __name__ == "__main__":
    main()