#clases
class NodoLinea:
    """
    Atributos:
        texto     (str):            Contenido de la linea de texto.
        siguiente (NodoLinea|None): Enlace al nodo de la linea siguiente.
        anterior  (NodoLinea|None): Enlace al nodo de la linea anterior.
    """
    def __init__(self, texto: str):
        self.texto     = texto
        self.siguiente = None
        self.anterior  = None


class EditorTexto:
    """
    Lista doblemente enlazada que representa el contenido de un documento
    de texto como una secuencia de lineas.
    Atributos:
        cabeza (NodoLinea|None): Primera linea del documento.
        cola   (NodoLinea|None): Ultima linea del documento.
        tamano (int):            Numero total de lineas.
    """

    def __init__(self):
        self.cabeza = None
        self.cola   = None
        self.tamano = 0

#funcion auxiliar que retorna el nodo en la posicion dada
    def _nodo_en(self, numero: int) -> "NodoLinea | None":
        """
        Parametros:
            numero (int): Numero de linea (1-indexado).

        Retorna:
            NodoLinea si la posicion es valida, None si no.
        """
        if numero < 1 or numero > self.tamano:
            return None
        actual = self.cabeza
        for _ in range(numero - 1):
            actual = actual.siguiente
        return actual

#funcion que saca un nodo de la cadena 
    def _desvincular(self, nodo: NodoLinea) -> None:
        """
        Parametros:
            nodo (NodoLinea): Nodo a desvincular de la lista.
        """
        if nodo.anterior:
            nodo.anterior.siguiente = nodo.siguiente
        else:
            self.cabeza = nodo.siguiente     # era la cabeza

        if nodo.siguiente:
            nodo.siguiente.anterior = nodo.anterior
        else:
            self.cola = nodo.anterior        # era la cola

        nodo.siguiente = None
        nodo.anterior  = None
        self.tamano   -= 1

    # ------------------------------------------------------------------
    # 1. INSERTAR LINEA EN POSICION ARBITRARIA
    # ------------------------------------------------------------------
    def insertar_linea(self, numero: int, texto: str) -> None:
        """
        Inserta una nueva linea con el texto dado en la posicion indicada.
        Parametros:
            numero (int): Posicion de insercion (1-indexado).
                          Si numero > tamano, se inserta al final.
                          Si numero < 1, se inserta al inicio.
            texto  (str): Contenido de la nueva linea.
        Funcionamiento:
            Crea un nuevo NodoLinea. Si la lista esta vacia o la posicion
            es la primera, actualiza la cabeza. Si la posicion supera el
            tamano, inserta al final actualizando la cola. En otro caso,
            encuentra el nodo en la posicion (numero-1) y enlaza el nuevo
            nodo entre ese y su siguiente, actualizando todos los punteros.
        """
        nuevo = NodoLinea(texto)

        if self.cabeza is None or numero <= 1:
            # Insertar al inicio
            nuevo.siguiente = self.cabeza
            if self.cabeza:
                self.cabeza.anterior = nuevo
            self.cabeza = nuevo
            if self.cola is None:
                self.cola = nuevo
            self.tamano += 1
            return

        if numero > self.tamano:
            # Insertar al final
            nuevo.anterior   = self.cola
            self.cola.siguiente = nuevo
            self.cola        = nuevo
            self.tamano     += 1
            return

        # Insertar en posicion intermedia: encontrar el nodo en (numero-1)
        referencia = self._nodo_en(numero - 1)
        nuevo.siguiente            = referencia.siguiente
        nuevo.anterior             = referencia
        if referencia.siguiente:
            referencia.siguiente.anterior = nuevo
        referencia.siguiente       = nuevo
        self.tamano += 1

#fucnionq ue elimina una linea especifica en una posicion dada
    def eliminar_linea(self, numero: int) -> bool:
        """
        Parametros:
            numero (int): Numero de linea a eliminar (1-indexado).
        Retorna:
            True si la linea fue eliminada, False si la posicion no existe.
        """
        nodo = self._nodo_en(numero)
        if nodo is None:
            return False
        self._desvincular(nodo)
        return True

#fucnion que meuve una lina desde una posicion de origen a otra posicion
    def mover_linea(self, origen: int, destino: int) -> bool:
        """
        Parametros:
            origen  (int): Numero de linea a mover (1-indexado).
            destino (int): Posicion destino (1-indexado, antes del movimiento).
        Retorna:
            True si la operacion fue exitosa, False si las posiciones no existen.
        """
        if origen < 1 or origen > self.tamano:
            return False
        if destino < 1:
            destino = 1

        nodo = self._nodo_en(origen)
        texto = nodo.texto
        self._desvincular(nodo)

        # ajustar destino porque el tamano disminuyo
        if destino > origen:
            destino -= 1

        self.insertar_linea(destino, texto)
        return True

#funcion que bsuca un patro de texto en todas las lineas del documento
    def buscar_texto(self, patron: str) -> list[tuple[int, str]]:
        """
        Parametros:
            patron (str): Texto a buscar (busqueda insensible a mayusculas).

        Retorna:
            list[tuple[int, str]]: Lista de (numero_linea, texto_linea) donde se encontro el patron.
        """
        resultados = []
        actual     = self.cabeza
        numero     = 1
        patron_l   = patron.lower()

        while actual is not None:
            if patron_l in actual.texto.lower():
                resultados.append((numero, actual.texto))
            actual = actual.siguiente
            numero += 1

        return resultados

#funcion que reemplaa todas las ocurrencias en una linea
    def reemplazar_texto(self, numero: int,
                          buscar: str, reemplazar: str) -> bool:
        """
        Parametros:
            numero     (int): Numero de linea objetivo (1-indexado).
            buscar     (str): Texto a reemplazar.
            reemplazar (str): Texto de sustitucion.

        Retorna:
            True si la linea existe y fue modificada, False si no existe.

        """
        nodo = self._nodo_en(numero)
        if nodo is None:
            return False
        nodo.texto = nodo.texto.replace(buscar, reemplazar)
        return True
#funcion que guarda el contenido del documento en un txt
    def guardar_archivo(self, ruta: str) -> bool:
        """
        Parametros:
            ruta (str): Ruta del archivo de destino.

        Retorna:
            True si la escritura fue exitosa, False en caso de error.
        """
        try:
            with open(ruta, "w", encoding="utf-8") as f:
                actual = self.cabeza
                while actual is not None:
                    f.write(actual.texto + "\n")
                    actual = actual.siguiente
            return True
        except OSError as e:
            print(f"  [Error al guardar] {e}")
            return False

#funcion que lee una rchivo y construye una lista enlazada
    def cargar_archivo(self, ruta: str) -> bool:
        """
        Parametros:
            ruta (str): Ruta del archivo a cargar.

        Retorna:
            True si la carga fue exitosa, False en caso de error.
        """
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                lineas = f.read().splitlines()

            # Resetear la lista
            self.cabeza = None
            self.cola   = None
            self.tamano = 0

            for linea in lineas:
                self.insertar_linea(self.tamano + 1, linea)
            return True
        except OSError as e:
            print(f"  [Error al cargar] {e}")
            return False

#funcionq ue imprime el documento completo
    def mostrar(self) -> None:
        if self.cabeza is None:
            print("  (documento vacio)")
            return
        actual = self.cabeza
        num    = 1
        print(f"\n  {'Ln':>4}  Contenido")
        print("  " + "-" * 50)
        while actual is not None:
            print(f"  {num:>4}  {actual.texto}")
            actual = actual.siguiente
            num   += 1
        print("  " + "-" * 50)
        print(f"  Total: {self.tamano} linea(s)")

#funcion principal con menu interactivo
def main() -> None:

    print(" PROBLEMA 2: EDITOR DE TEXTO - LISTA DOBLEMENTE ENLAZADA")

    editor = EditorTexto()

    while True:
        print(f"  EDITOR  |  Lineas en el documento: {editor.tamano}")
        print("  1. Insertar linea en una posicion")
        print("  2. Eliminar linea")
        print("  3. Mover linea a otra posicion")
        print("  4. Buscar texto en el documento")
        print("  5. Reemplazar texto en una linea")
        print("  6. Guardar documento en archivo")
        print("  7. Cargar documento desde archivo")
        print("  8. Mostrar documento completo")
        print("  0. Salir")

        op = input("\n  Opcion: ").strip()
        # --- 1. Insertar ---
        if op == "1":
            try:
                pos = int(input("  Numero de linea (posicion de insercion): "))
            except ValueError:
                print("  [Error] Ingrese un entero.")
                continue
            texto = input("  Texto de la linea                       : ")
            editor.insertar_linea(pos, texto)
            print(f"  Linea insertada en la posicion {pos}.")
        # --- 2. Eliminar ---
        elif op == "2":
            try:
                num = int(input("  Numero de linea a eliminar: "))
            except ValueError:
                print("  [Error] Ingrese un entero.")
                continue
            if editor.eliminar_linea(num):
                print(f"  Linea {num} eliminada.")
            else:
                print(f"  La linea {num} no existe.")
        # --- 3. Mover ---
        elif op == "3":
            try:
                origen  = int(input("  Numero de linea origen  : "))
                destino = int(input("  Numero de linea destino : "))
            except ValueError:
                print("  [Error] Ingrese enteros.")
                continue
            if editor.mover_linea(origen, destino):
                print(f"  Linea {origen} movida a la posicion {destino}.")
            else:
                print(f"  Posicion de origen invalida.")
        # --- 4. Buscar ---
        elif op == "4":
            patron = input("  Texto a buscar: ")
            resultados = editor.buscar_texto(patron)
            if resultados:
                print(f"\n  {len(resultados)} coincidencia(s) encontrada(s):")
                for num, linea in resultados:
                    print(f"    Linea {num:>4}: {linea}")
            else:
                print("  Texto no encontrado en el documento.")
        # --- 5. Reemplazar ---
        elif op == "5":
            try:
                num = int(input("  Numero de linea         : "))
            except ValueError:
                print("  [Error] Ingrese un entero.")
                continue
            buscar     = input("  Texto a reemplazar      : ")
            reemplazar = input("  Nuevo texto             : ")
            if editor.reemplazar_texto(num, buscar, reemplazar):
                print(f"  Texto reemplazado en la linea {num}.")
            else:
                print(f"  La linea {num} no existe.")
        # --- 6. Guardar ---
        elif op == "6":
            ruta = input("  Ruta del archivo (e.g. documento.txt): ").strip()
            if editor.guardar_archivo(ruta):
                print(f"  Documento guardado en '{ruta}'.")
        # --- 7. Cargar ---
        elif op == "7":
            ruta = input("  Ruta del archivo a cargar: ").strip()
            if editor.cargar_archivo(ruta):
                print(f"  Documento cargado: {editor.tamano} linea(s).")
        # --- 8. Mostrar ---
        elif op == "8":
            editor.mostrar()

        elif op == "0":
            print("\n  Editor cerrado.")
            break
        else:
            print("  Opcion invalida.")


if __name__ == "__main__":
    main()