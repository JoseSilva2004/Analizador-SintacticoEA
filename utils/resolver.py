import sympy as sp
import re  # Importar regex para hacer reemplazos más precisos

def corregir_multiplicacion_implicita(expresion):
    """
    Corrige la notación matemática implícita, reemplazando casos como '3x' con '3*x',
    pero evitando errores cuando 'x' o 'y' están al inicio o después de un operador.
    """
    # Reemplazar números seguidos de una letra (variable) por la versión con '*'
    expresion = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expresion)
    
    # Reemplazar una variable seguida de otra (como xy -> x*y)
    expresion = re.sub(r'([a-zA-Z])([a-zA-Z])', r'\1*\2', expresion)
    
    # Reemplazar potencias escritas con ^ por ** (Python compatible)
    expresion = expresion.replace('^', '**')

    return expresion

def resolver_expresion(expresion):
    pasos = []
    
    try:
        expresion = corregir_multiplicacion_implicita(expresion)  # Corregir la entrada
        
        # Si la expresión es una ecuación
        if "=" in expresion:
            izquierda, derecha = expresion.split("=")
            izquierda = sp.sympify(izquierda)
            derecha = sp.sympify(derecha)
            ecuacion = sp.Eq(izquierda, derecha)
            pasos.append(f"Ecuación dada: {ecuacion}")
            
            # Resolver la ecuación paso a paso
            pasos.append("Pasos de solución:")
            solucion = sp.solve(ecuacion)
            for paso in solucion:
                pasos.append(f"Solución: {paso}")

        else:
            # Si no es una ecuación, simplificar y dar los pasos
            expresion_simplificada = sp.sympify(expresion)
            pasos.append(f"Expresión original: {expresion}")
            pasos.append("Paso 1: Simplificamos la expresión:")
            expresion_simplificada = sp.simplify(expresion_simplificada)
            pasos.append(f"Expresión simplificada: {expresion_simplificada}")

    except Exception as e:
        pasos.append(f"Error al resolver: {str(e)}")
    
    return pasos
