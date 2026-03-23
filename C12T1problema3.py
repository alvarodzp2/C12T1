#clases
class NodoTermino:
    """
    Nodo de la lista enlazada que representa un termino del polinomio.

    Atributos:
        coeficiente (float):           Factor multiplicativo del termino.
        exponente   (int):             Potencia de la variable x.
        siguiente   (NodoTermino|None): Enlace al siguiente termino (menor grado).
    """
    def __init__(self, coeficiente: float, exponente: int):
        self.coeficiente = coeficiente
        self.exponente   = exponente
        self.siguiente   = None


class Polinomio:
    """
    Lista enlazada ordenada (mayor a menor exponente) que representa
    un polinomio matematico. Solo almacena terminos con coeficiente != 0.

    Atributos:
        cabeza (NodoTermino|None): Termino de mayor grado.
    """

    def __init__(self):
        self.cabeza = None

#funcion para insertar terminos
    def insertar_termino(self, coef: float, exp: int) -> None:
        """
        Parametros:
            coef (float): Coeficiente del termino.
            exp  (int):   Exponente del termino (>= 0).

        Funcionamiento:
            Si ya existe un nodo con el mismo exponente, suma el coeficiente.
            Si el resultado es 0 lo elimina. Si no existe, busca el lugar
            correcto segun el orden y enlaza el nuevo nodo ahi.
            Los terminos con coeficiente 0 no se insertan.
        """
        if coef == 0:
            return

        nuevo = NodoTermino(coef, exp)

        # Insertar al inicio (mayor exponente)
        if self.cabeza is None or exp > self.cabeza.exponente:
            nuevo.siguiente = self.cabeza
            self.cabeza     = nuevo
            return

        # Buscar posicion correcta o acumular en existente
        actual = self.cabeza
        while actual is not None:
            if actual.exponente == exp:
                actual.coeficiente += coef
                if actual.coeficiente == 0:
                    self._eliminar_exponente(exp)
                return
            if actual.siguiente is None or actual.siguiente.exponente < exp:
                nuevo.siguiente    = actual.siguiente
                actual.siguiente   = nuevo
                return
            actual = actual.siguiente

    def _eliminar_exponente(self, exp: int) -> None:
        """Elimina el nodo con el exponente dado. Uso interno."""
        if self.cabeza is None:
            return
        if self.cabeza.exponente == exp:
            self.cabeza = self.cabeza.siguiente
            return
        actual = self.cabeza
        while actual.siguiente is not None:
            if actual.siguiente.exponente == exp:
                actual.siguiente = actual.siguiente.siguiente
                return
            actual = actual.siguiente

#funcion que devuelve la cadena en formato de un polinomio
    def mostrar(self) -> str:

        if self.cabeza is None:
            return "0"

        partes = []
        actual = self.cabeza

        while actual is not None:
            c = actual.coeficiente
            e = actual.exponente

            # Formato del coeficiente
            if e == 0:
                termino = f"{c:g}"
            elif e == 1:
                termino = f"{abs(c):g}x" if abs(c) != 1 else "x"
            else:
                termino = f"{abs(c):g}x^{e}" if abs(c) != 1 else f"x^{e}"

            if partes:
                signo   = " + " if c > 0 else " - "
                partes.append(signo + termino)
            else:
                prefijo = "" if c > 0 else "-"
                partes.append(prefijo + termino)

            actual = actual.siguiente

        return "".join(partes)

#funcion que usma polinomios
    def sumar(self, otro: "Polinomio") -> "Polinomio":
        """
        Parametros:
            otro (Polinomio): Segundo operando.
        Retorna:
            Polinomio: Resultado de la suma.
        Funcionamiento:
            Recorre ambas listas en paralelo (como merge de merge-sort),
            insertando terminos al resultado segun el exponente mayor de
            cada par de punteros actuales.
        """
        resultado = Polinomio()
        a = self.cabeza
        b = otro.cabeza

        while a is not None and b is not None:
            if a.exponente > b.exponente:
                resultado.insertar_termino(a.coeficiente, a.exponente)
                a = a.siguiente
            elif b.exponente > a.exponente:
                resultado.insertar_termino(b.coeficiente, b.exponente)
                b = b.siguiente
            else:
                resultado.insertar_termino(
                    a.coeficiente + b.coeficiente, a.exponente
                )
                a = a.siguiente
                b = b.siguiente

        while a is not None:
            resultado.insertar_termino(a.coeficiente, a.exponente)
            a = a.siguiente
        while b is not None:
            resultado.insertar_termino(b.coeficiente, b.exponente)
            b = b.siguiente

        return resultado
#funcion que resta polinomios
    def restar(self, otro: "Polinomio") -> "Polinomio":
        """
        Resta 'otro' de este polinomio y retorna un nuevo Polinomio.
        Parametro:
            otro (Polinomio): Sustraendo.
        Retorna:
            Polinomio: Resultado de la resta.
        """
        negado = Polinomio()
        actual = otro.cabeza
        while actual is not None:
            negado.insertar_termino(-actual.coeficiente, actual.exponente)
            actual = actual.siguiente
        return self.sumar(negado)

 #funcion apr amultiplicar dos polinomios
    def multiplicar(self, otro: "Polinomio") -> "Polinomio":
        """
        Parametros:
            otro (Polinomio): Segundo factor.

        Retorna:
            Polinomio: Resultado del producto.
        """
        resultado = Polinomio()
        a = self.cabeza

        while a is not None:
            b = otro.cabeza
            while b is not None:
                resultado.insertar_termino(
                    a.coeficiente * b.coeficiente,
                    a.exponente   + b.exponente
                )
                b = b.siguiente
            a = a.siguiente

        return resultado

#funcion que evalua un polinomio
    def evaluar(self, x: float) -> float:
        """
        Parametros:
            x (float): Valor de la variable.
        Retorna:
            float: Resultado de P(x).

        """
        resultado = 0.0
        actual    = self.cabeza
        while actual is not None:
            resultado += actual.coeficiente * (x ** actual.exponente)
            actual     = actual.siguiente
        return round(resultado, 8)

#funcion para derivar un polinomio
    def derivar(self) -> "Polinomio":
        """
        Retorna:
            Polinomio: Derivada P'(x).
        """
        resultado = Polinomio()
        actual    = self.cabeza
        while actual is not None:
            if actual.exponente > 0:
                resultado.insertar_termino(
                    actual.coeficiente * actual.exponente,
                    actual.exponente   - 1
                )
            actual = actual.siguiente
        return resultado

#funcion apra integrar un polinomio
    def integrar(self) -> "Polinomio":
        """
        Retorna:
            Polinomio: Integral indefinida (sin constante C).

        Funcionamiento:
            Para cada termino c*x^n la integral es (c/(n+1))*x^(n+1).
        """
        resultado = Polinomio()
        actual    = self.cabeza
        while actual is not None:
            nuevo_exp  = actual.exponente + 1
            nuevo_coef = actual.coeficiente / nuevo_exp
            resultado.insertar_termino(nuevo_coef, nuevo_exp)
            actual = actual.siguiente
        return resultado

#funcion en la que el usuario ingresa el polinomio
def pedir_polinomio(nombre: str) -> Polinomio:
    """
    Parametros:
        nombre (str): Etiqueta del polinomio (e.g. "P1").
    Retorna:
        Polinomio: Objeto construido con los terminos ingresados.
    Funcionamiento:
        El usuario ingresa pares (coeficiente, exponente)
    """
    p = Polinomio()
    print(f"\n  -- Ingreso del {nombre} --")
    print("  Ingrese terminos (coeficiente y exponente).")
    print("  Presione ENTER sin coeficiente para terminar.\n")

    while True:
        coef_str = input("  Coeficiente (o ENTER para terminar): ").strip()
        if not coef_str:
            break
        try:
            coef = float(coef_str)
        except ValueError:
            print("  [Error] Coeficiente invalido.")
            continue
        try:
            exp = int(input("  Exponente                          : "))
            if exp < 0:
                print("  [Error] El exponente debe ser >= 0.")
                continue
        except ValueError:
            print("  [Error] Exponente debe ser entero.")
            continue

        p.insertar_termino(coef, exp)
        print(f"  Termino agregado. {nombre} = {p.mostrar()}")

    return p

#funcion principal con menu interactivo
def main() -> None:
    """
    Menu interactivo del sistema de gestion de polinomios.
    El usuario ingresa al menos 3 polinomios y realiza todas las operaciones.
    """
    print(" PROBLEMA 3: GESTION DE POLINOMIOS - LISTA ENLAZADA")
    print("\n  Primero ingrese al menos 3 polinomios.")

    polinomios: dict[str, Polinomio] = {}

    while True:
        print(f"  MENU  |  Polinomios guardados: {list(polinomios.keys())}")
        print("  1. Ingresar nuevo polinomio")
        print("  2. Mostrar un polinomio")
        print("  3. Sumar dos polinomios")
        print("  4. Restar dos polinomios")
        print("  5. Multiplicar dos polinomios")
        print("  6. Evaluar un polinomio en x")
        print("  7. Derivar un polinomio")
        print("  8. Integrar un polinomio")
        print("  0. Salir")

        op = input("\n  Opcion: ").strip()

        # --- 1. Ingresar ---
        if op == "1":
            nombre = input("  Nombre del polinomio (e.g. P1): ").strip()
            if not nombre:
                print("  [Error] El nombre no puede estar vacio.")
                continue
            polinomios[nombre] = pedir_polinomio(nombre)
            print(f"\n  {nombre} = {polinomios[nombre].mostrar()}")

        # --- 2. Mostrar ---
        elif op == "2":
            nombre = input("  Nombre del polinomio: ").strip()
            if nombre not in polinomios:
                print(f"  '{nombre}' no existe.")
            else:
                print(f"\n  {nombre}(x) = {polinomios[nombre].mostrar()}")

        # --- 3. Sumar ---
        elif op == "3":
            a = input("  Primer polinomio  : ").strip()
            b = input("  Segundo polinomio : ").strip()
            if a not in polinomios or b not in polinomios:
                print("  [Error] Alguno de los polinomios no existe.")
                continue
            resultado = polinomios[a].sumar(polinomios[b])
            nombre_r  = input("  Guardar resultado como: ").strip()
            polinomios[nombre_r] = resultado
            print(f"\n  {a} + {b} = {resultado.mostrar()}")

        # --- 4. Restar ---
        elif op == "4":
            a = input("  Primer polinomio  : ").strip()
            b = input("  Segundo polinomio : ").strip()
            if a not in polinomios or b not in polinomios:
                print("  [Error] Alguno de los polinomios no existe.")
                continue
            resultado = polinomios[a].restar(polinomios[b])
            nombre_r  = input("  Guardar resultado como: ").strip()
            polinomios[nombre_r] = resultado
            print(f"\n  {a} - {b} = {resultado.mostrar()}")

        # --- 5. Multiplicar ---
        elif op == "5":
            a = input("  Primer polinomio  : ").strip()
            b = input("  Segundo polinomio : ").strip()
            if a not in polinomios or b not in polinomios:
                print("  [Error] Alguno de los polinomios no existe.")
                continue
            resultado = polinomios[a].multiplicar(polinomios[b])
            nombre_r  = input("  Guardar resultado como: ").strip()
            polinomios[nombre_r] = resultado
            print(f"\n  {a} * {b} = {resultado.mostrar()}")

        # --- 6. Evaluar ---
        elif op == "6":
            nombre = input("  Nombre del polinomio: ").strip()
            if nombre not in polinomios:
                print(f"  '{nombre}' no existe.")
                continue
            try:
                x = float(input("  Valor de x          : "))
            except ValueError:
                print("  [Error] Ingrese un numero valido.")
                continue
            val = polinomios[nombre].evaluar(x)
            print(f"\n  {nombre}({x}) = {val}")

        # --- 7. Derivar ---
        elif op == "7":
            nombre = input("  Nombre del polinomio: ").strip()
            if nombre not in polinomios:
                print(f"  '{nombre}' no existe.")
                continue
            derivada = polinomios[nombre].derivar()
            nombre_r = input("  Guardar derivada como: ").strip()
            polinomios[nombre_r] = derivada
            print(f"\n  d/dx [{nombre}] = {derivada.mostrar()}")

        # --- 8. Integrar ---
        elif op == "8":
            nombre = input("  Nombre del polinomio: ").strip()
            if nombre not in polinomios:
                print(f"  '{nombre}' no existe.")
                continue
            integral = polinomios[nombre].integrar()
            nombre_r = input("  Guardar integral como: ").strip()
            polinomios[nombre_r] = integral
            print(f"\n  integral [{nombre}] = {integral.mostrar()} + C")

        elif op == "0":
            print("\n  Sistema de polinomios cerrado.")
            break
        else:
            print("  Opcion invalida.")


if __name__ == "__main__":
    main()