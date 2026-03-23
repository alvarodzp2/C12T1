#clase que represnta una celda con un nodo
class NodoCelda:
    """
    Atributos:
        fila     (int):            Indice de fila (0-indexado).
        columna  (int):            Indice de columna (0-indexado).
        valor    (float|str):      Contenido de la celda.
        sig_fila (NodoCelda|None): Siguiente celda en la misma fila
                                   (ordenada por columna ascendente).
        sig_col  (NodoCelda|None): Siguiente celda en la misma columna
                                   (ordenada por fila ascendente).
    """
    def __init__(self, fila: int, columna: int, valor):
        self.fila     = fila
        self.columna  = columna
        self.valor    = valor
        self.sig_fila = None   # siguiente en la fila
        self.sig_col  = None   # siguiente en la columna

#clase que apunta a la primera celda de la fila
class NodoFila:
    """
    Atributos:
        fila_id   (int):           Numero de fila.
        primera   (NodoCelda|None): Primera celda de esta fila.
        siguiente (NodoFila|None):  Siguiente cabecera de fila.
    """
    def __init__(self, fila_id: int):
        self.fila_id   = fila_id
        self.primera   = None
        self.siguiente = None

#clase que apunta la priemr nodo de la columna
class NodoColumna:
    """
    Atributos:
        col_id    (int):              Numero de columna.
        primera   (NodoCelda|None):   Primera celda de esta columna.
        siguiente (NodoColumna|None): Siguiente cabecera de columna.
    """
    def __init__(self, col_id: int):
        self.col_id   = col_id
        self.primera  = None
        self.siguiente = None

class HojaCalculo:
    """

    Atributos:
        filas    (NodoFila|None):    Lista enlazada de cabeceras de fila.
        columnas (NodoColumna|None): Lista enlazada de cabeceras de columna.
        n_celdas (int):              Numero de celdas no vacias almacenadas.
    """

    def __init__(self):
        self.filas    = None
        self.columnas = None
        self.n_celdas = 0

#funcion que retorna la cabecera de una fila
    def _cabecera_fila(self, fila: int, crear: bool = True) -> "NodoFila | None":

        previo = None
        actual = self.filas
        while actual is not None and actual.fila_id < fila:
            previo = actual
            actual = actual.siguiente

        if actual is not None and actual.fila_id == fila:
            return actual                       # ya existe

        if not crear:
            return None

        nuevo = NodoFila(fila)
        nuevo.siguiente = actual
        if previo is None:
            self.filas = nuevo
        else:
            previo.siguiente = nuevo
        return nuevo
#funcion que retorna la cabecera de una columna
    def _cabecera_col(self, col: int, crear: bool = True) -> "NodoColumna | None":

        previo = None
        actual = self.columnas
        while actual is not None and actual.col_id < col:
            previo = actual
            actual = actual.siguiente

        if actual is not None and actual.col_id == col:
            return actual

        if not crear:
            return None

        nuevo = NodoColumna(col)
        nuevo.siguiente = actual
        if previo is None:
            self.columnas = nuevo
        else:
            previo.siguiente = nuevo
        return nuevo

#funcion para actualizar el valor de la celda
    def insertar(self, fila: int, col: int, valor) -> None:
        """
        Parametros:
            fila  (int):       Indice de fila (0-indexado).
            col   (int):       Indice de columna (0-indexado).
            valor (float|str): Nuevo valor de la celda.
        Funcionamiento:
            Primero busca si ya existe la celda con (fila, col).
            Si existe, actualiza el valor. Si no, crea un NodoCelda y lo
            inserta en la lista de la fila (ordenado por col) y en la
            lista de la columna (ordenado por fila).
        """
        # Buscar si ya existe
        celda_existente = self._buscar_celda(fila, col)
        if celda_existente is not None:
            celda_existente.valor = valor
            return

        nueva = NodoCelda(fila, col, valor)

        # --- Insertar en lista de fila (ordenado por columna) ---
        cab_fila = self._cabecera_fila(fila)
        previo   = None
        actual   = cab_fila.primera
        while actual is not None and actual.columna < col:
            previo = actual
            actual = actual.sig_fila
        nueva.sig_fila = actual
        if previo is None:
            cab_fila.primera = nueva
        else:
            previo.sig_fila = nueva

        # --- Insertar en lista de columna (ordenado por fila) ---
        cab_col  = self._cabecera_col(col)
        previo   = None
        actual   = cab_col.primera
        while actual is not None and actual.fila < fila:
            previo = actual
            actual = actual.sig_col
        nueva.sig_col = actual
        if previo is None:
            cab_col.primera = nueva
        else:
            previo.sig_col = nueva

        self.n_celdas += 1

#fucnion para eliminar la celda de una posicion
    def eliminar(self, fila: int, col: int) -> bool:
        """
        Parametros:
            fila (int): Indice de fila.
            col  (int): Indice de columna.
        Retorna:
            True si la celda existia y fue eliminada, False si no.

        Funcionamiento:
            Elimina el nodo de la lista de su fila y de la lista de
            su columna de forma independiente, ajustando los enlaces.
        """
        cab_fila = self._cabecera_fila(fila, crear=False)
        if cab_fila is None:
            return False

        # Eliminar de la lista de fila
        previo = None
        actual = cab_fila.primera
        while actual is not None and actual.columna != col:
            previo = actual
            actual = actual.sig_fila
        if actual is None:
            return False                   # celda no existe

        if previo is None:
            cab_fila.primera = actual.sig_fila
        else:
            previo.sig_fila  = actual.sig_fila

        # Eliminar de la lista de columna
        cab_col = self._cabecera_col(col, crear=False)
        if cab_col is not None:
            previo_c = None
            actual_c = cab_col.primera
            while actual_c is not None and actual_c.fila != fila:
                previo_c = actual_c
                actual_c = actual_c.sig_col
            if actual_c is not None:
                if previo_c is None:
                    cab_col.primera = actual_c.sig_col
                else:
                    previo_c.sig_col = actual_c.sig_col

        self.n_celdas -= 1
        return True

#funcion que busca y te devuelve el valor de una celda especifica
    def _buscar_celda(self, fila: int, col: int) -> "NodoCelda | None":
        cab_fila = self._cabecera_fila(fila, crear=False)
        if cab_fila is None:
            return None
        actual = cab_fila.primera
        while actual is not None:
            if actual.columna == col:
                return actual
            if actual.columna > col:
                return None
            actual = actual.sig_fila
        return None

    def obtener(self, fila: int, col: int):
        """
        Retorna el valor de la celda (fila, col), o None si esta vacia.
        """
        celda = self._buscar_celda(fila, col)
        return celda.valor if celda else None

#funcion que suma todos los valores numericos de una celda
    def sumar_rango(self, f1: int, c1: int, f2: int, c2: int) -> float:
        """
        Parametros:
            f1, c1 (int): Esquina superior-izquierda del rango.
            f2, c2 (int): Esquina inferior-derecha del rango.

        Retorna:
            float: Suma total de los valores numericos del rango.
        """
        total = 0.0
        cab   = self.filas
        while cab is not None:
            if f1 <= cab.fila_id <= f2:
                celda = cab.primera
                while celda is not None:
                    if c1 <= celda.columna <= c2:
                        try:
                            total += float(celda.valor)
                        except (TypeError, ValueError):
                            pass
                    celda = celda.sig_fila
            cab = cab.siguiente
        return round(total, 6)
#funcion que calcula el promedio de un rango de filas
    def promedio_rango(self, f1: int, c1: int, f2: int, c2: int) -> float:
        """
        Retorna:
            float: Promedio. 0.0 si no hay celdas numericas en el rango.
        """
        total  = 0.0
        conteo = 0
        cab    = self.filas
        while cab is not None:
            if f1 <= cab.fila_id <= f2:
                celda = cab.primera
                while celda is not None:
                    if c1 <= celda.columna <= c2:
                        try:
                            total += float(celda.valor)
                            conteo += 1
                        except (TypeError, ValueError):
                            pass
                    celda = celda.sig_fila
            cab = cab.siguiente
        return round(total / conteo, 6) if conteo > 0 else 0.0

#funcion que elimina las celdas de una fila
    def eliminar_fila(self, fila: int) -> int:
        """
        Parametros:
            fila (int): Numero de fila a eliminar.

        Retorna:
            int: Numero de celdas eliminadas.
        """
        cab_fila = self._cabecera_fila(fila, crear=False)
        if cab_fila is None:
            return 0

        eliminadas = 0
        celda = cab_fila.primera
        while celda is not None:
            siguiente = celda.sig_fila
            col = celda.columna
            # Eliminar de la lista de esa columna
            cab_col = self._cabecera_col(col, crear=False)
            if cab_col:
                prev = None
                cur  = cab_col.primera
                while cur is not None and cur.fila != fila:
                    prev = cur
                    cur  = cur.sig_col
                if cur:
                    if prev is None:
                        cab_col.primera = cur.sig_col
                    else:
                        prev.sig_col = cur.sig_col
            eliminadas  += 1
            self.n_celdas -= 1
            celda = siguiente

        cab_fila.primera = None  # vaciar la fila

        # Quitar la cabecera de fila de la lista de cabeceras
        prev_cab = None
        cur_cab  = self.filas
        while cur_cab is not None and cur_cab.fila_id != fila:
            prev_cab = cur_cab
            cur_cab  = cur_cab.siguiente
        if cur_cab:
            if prev_cab is None:
                self.filas = cur_cab.siguiente
            else:
                prev_cab.siguiente = cur_cab.siguiente

        return eliminadas
#funcion que elimna varias columnas
    def eliminar_columna(self, col: int) -> int:
        """
        Parametros:
            col (int): Numero de columna a eliminar.
        Retorna:
            int: Numero de celdas eliminadas.
        """
        cab_col = self._cabecera_col(col, crear=False)
        if cab_col is None:
            return 0

        eliminadas = 0
        celda = cab_col.primera
        while celda is not None:
            siguiente = celda.sig_col
            fila = celda.fila
            # Eliminar de la lista de esa fila
            cab_fila = self._cabecera_fila(fila, crear=False)
            if cab_fila:
                prev = None
                cur  = cab_fila.primera
                while cur is not None and cur.columna != col:
                    prev = cur
                    cur  = cur.sig_fila
                if cur:
                    if prev is None:
                        cab_fila.primera = cur.sig_fila
                    else:
                        prev.sig_fila = cur.sig_fila
            eliminadas    += 1
            self.n_celdas -= 1
            celda = siguiente

        cab_col.primera = None

        # Quitar la cabecera de columna
        prev_cab = None
        cur_cab  = self.columnas
        while cur_cab is not None and cur_cab.col_id != col:
            prev_cab = cur_cab
            cur_cab  = cur_cab.siguiente
        if cur_cab:
            if prev_cab is None:
                self.columnas = cur_cab.siguiente
            else:
                prev_cab.siguiente = cur_cab.siguiente

        return eliminadas

#funcion que imprime la hoja de calculo en un formato de tabla
    def mostrar(self) -> None:
        if self.n_celdas == 0:
            print("  (hoja de calculo vacia)")
            return

        # Recopilar filas y columnas ocupadas
        filas_id = []
        cab = self.filas
        while cab is not None:
            filas_id.append(cab.fila_id)
            cab = cab.siguiente
        cols_id = []
        cab = self.columnas
        while cab is not None:
            cols_id.append(cab.col_id)
            cab = cab.siguiente

        ancho_celda = 10

        # Cabecera de columnas
        print("\n  " + " " * 5 + "".join(f"  Col{c:<{ancho_celda-5}}" for c in cols_id))
        print("  " + "-" * (6 + ancho_celda * len(cols_id)))

        for f in filas_id:
            fila_str = f"  Fila{f:<2}|"
            for c in cols_id:
                valor = self.obtener(f, c)
                celda = str(valor) if valor is not None else ""
                fila_str += f" {celda:<{ancho_celda-1}}"
            print(fila_str)

        print("  " + "-" * (6 + ancho_celda * len(cols_id)))
        print(f"\n  Celdas no vacias : {self.n_celdas}")
        f_max = max(filas_id) + 1 if filas_id else 0
        c_max = max(cols_id)  + 1 if cols_id  else 0
        total_densa = f_max * c_max
        ahorro      = round((1 - self.n_celdas / total_densa) * 100, 1) if total_densa else 0
        print(f"  Matriz densa eq  : {total_densa} celdas  "
              f"(ahorro de memoria: {ahorro}%)")

#funcion para cargar el archivo
    def guardar(self, ruta: str) -> bool:
        """
        Parametros:
            ruta (str): Ruta del archivo de salida.
        Retorna:
            True si el guardado fue exitoso.
        """
        try:
            with open(ruta, "w", encoding="utf-8") as f:
                f.write("fila,columna,valor\n")
                cab = self.filas
                while cab is not None:
                    celda = cab.primera
                    while celda is not None:
                        f.write(f"{celda.fila},{celda.columna},{celda.valor}\n")
                        celda = celda.sig_fila
                    cab = cab.siguiente
            return True
        except OSError as e:
            print(f"  [Error al guardar] {e}")
            return False

    def cargar(self, ruta: str) -> bool:
        """
        Carga una hoja de calculo desde un archivo CSV (fila,col,valor).
        Reemplaza el contenido actual.

        Parametros:
            ruta (str): Ruta del archivo a cargar.

        Retorna:
            True si la carga fue exitosa.
        """
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                lineas = f.read().splitlines()

            self.filas    = None
            self.columnas = None
            self.n_celdas = 0

            for linea in lineas[1:]:     # omitir cabecera
                partes = linea.split(",")
                if len(partes) < 3:
                    continue
                try:
                    fila = int(partes[0])
                    col  = int(partes[1])
                    try:
                        valor = float(partes[2])
                    except ValueError:
                        valor = partes[2]
                    self.insertar(fila, col, valor)
                except ValueError:
                    continue
            return True
        except OSError as e:
            print(f"  [Error al cargar] {e}")
            return False

#funcion que le ide fila y columna al usuario
def pedir_coordenadas(mensaje: str = "") -> tuple[int, int]:
    if mensaje:
        print(f"  {mensaje}")
    while True:
        try:
            fila = int(input("  Fila    (0-indexado): "))
            col  = int(input("  Columna (0-indexado): "))
            if fila < 0 or col < 0:
                print("  [Error] Los indices deben ser >= 0.")
                continue
            return fila, col
        except ValueError:
            print("  [Error] Ingrese enteros validos.")

#funcion principal con menu interactivo
def main() -> None:

    print("  PROBLEMA 4: HOJA DE CALCULO DISPERSA - LISTA ENLAZADA")

    hoja = HojaCalculo()

    while True:
        print(f"  MENU  |  Celdas no vacias: {hoja.n_celdas}")
        print("  1. Insertar o actualizar celda")
        print("  2. Eliminar celda")
        print("  3. Obtener valor de una celda")
        print("  4. Sumar rango de celdas")
        print("  5. Promediar rango de celdas")
        print("  6. Eliminar fila completa")
        print("  7. Eliminar columna completa")
        print("  8. Mostrar hoja de calculo")
        print("  9. Guardar en archivo CSV")
        print(" 10. Cargar desde archivo CSV")
        print("  0. Salir")

        op = input("\n  Opcion: ").strip()

        # --- 1. Insertar ---
        if op == "1":
            fila, col = pedir_coordenadas()
            valor_str = input("  Valor de la celda   : ").strip()
            try:
                valor = float(valor_str)
            except ValueError:
                valor = valor_str
            hoja.insertar(fila, col, valor)
            print(f"  Celda ({fila},{col}) = {valor} guardada.")

        # --- 2. Eliminar celda ---
        elif op == "2":
            fila, col = pedir_coordenadas()
            if hoja.eliminar(fila, col):
                print(f"  Celda ({fila},{col}) eliminada.")
            else:
                print(f"  La celda ({fila},{col}) no existia.")

        # --- 3. Obtener ---
        elif op == "3":
            fila, col = pedir_coordenadas()
            val = hoja.obtener(fila, col)
            if val is None:
                print(f"  Celda ({fila},{col}) esta vacia.")
            else:
                print(f"  Celda ({fila},{col}) = {val}")

        # --- 4. Sumar rango ---
        elif op == "4":
            print("  Esquina superior-izquierda del rango:")
            f1, c1 = pedir_coordenadas()
            print("  Esquina inferior-derecha del rango:")
            f2, c2 = pedir_coordenadas()
            total = hoja.sumar_rango(f1, c1, f2, c2)
            print(f"  Suma del rango [{f1}..{f2}][{c1}..{c2}] = {total}")

        # --- 5. Promediar rango ---
        elif op == "5":
            print("  Esquina superior-izquierda del rango:")
            f1, c1 = pedir_coordenadas()
            print("  Esquina inferior-derecha del rango:")
            f2, c2 = pedir_coordenadas()
            prom = hoja.promedio_rango(f1, c1, f2, c2)
            print(f"  Promedio del rango [{f1}..{f2}][{c1}..{c2}] = {prom}")

        # --- 6. Eliminar fila ---
        elif op == "6":
            try:
                fila = int(input("  Numero de fila a eliminar: "))
            except ValueError:
                print("  [Error] Ingrese un entero.")
                continue
            n = hoja.eliminar_fila(fila)
            print(f"  {n} celda(s) eliminada(s) de la fila {fila}.")

        # --- 7. Eliminar columna ---
        elif op == "7":
            try:
                col = int(input("  Numero de columna a eliminar: "))
            except ValueError:
                print("  [Error] Ingrese un entero.")
                continue
            n = hoja.eliminar_columna(col)
            print(f"  {n} celda(s) eliminada(s) de la columna {col}.")

        # --- 8. Mostrar ---
        elif op == "8":
            hoja.mostrar()

        # --- 9. Guardar ---
        elif op == "9":
            ruta = input("  Nombre del archivo (e.g. hoja.csv): ").strip()
            if hoja.guardar(ruta):
                print(f"  Hoja guardada en '{ruta}'.")

        # --- 10. Cargar ---
        elif op == "10":
            ruta = input("  Nombre del archivo CSV: ").strip()
            if hoja.cargar(ruta):
                print(f"  Hoja cargada: {hoja.n_celdas} celda(s).")

        elif op == "0":
            print("\n  Hoja de calculo cerrada.")
            break
        else:
            print("  Opcion invalida.")


if __name__ == "__main__":
    main()