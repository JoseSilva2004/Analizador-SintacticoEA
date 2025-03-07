import sympy as sp
import re

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
        # Inicializar la impresión en formato Unicode para mejor legibilidad
        sp.init_printing(use_unicode=True)
        
        # Corregir la entrada para manejar multiplicaciones implícitas y potencias
        expresion = corregir_multiplicacion_implicita(expresion)
        
        # Verificar si la expresión es una ecuación
        if "=" in expresion:
            # Dividir la expresión en lado izquierdo y derecho de la igualdad
            izquierda, derecha = expresion.split("=")
            
            # Convertir las cadenas a expresiones simbólicas de SymPy
            izquierda = sp.sympify(izquierda)
            derecha = sp.sympify(derecha)
            
            # Crear la ecuación simbólica
            ecuacion = sp.Eq(izquierda, derecha)
            pasos.append(f"Ecuación dada: {sp.pretty(ecuacion)}")
            
            # Resolver la ecuación
            soluciones = sp.solve(ecuacion)
            pasos.append("Pasos de solución:")
            
            # Si hay múltiples soluciones, enumerarlas
            if len(soluciones) > 1:
                for i, sol in enumerate(soluciones, 1):
                    pasos.append(f"Solución {i}: {sp.pretty(sol)}")
            elif soluciones:
                pasos.append(f"Solución: {sp.pretty(soluciones[0])}")
            else:
                pasos.append("No se encontraron soluciones.")
        else:
            # Si no es una ecuación, simplificar la expresión
            expresion_simplificada = sp.sympify(expresion)
            pasos.append(f"Expresión original: {sp.pretty(expresion_simplificada)}")
            pasos.append("Paso 1: Simplificamos la expresión:")
            expresion_simplificada = sp.simplify(expresion_simplificada)
            pasos.append(f"Expresión simplificada: {sp.pretty(expresion_simplificada)}")

    except Exception as e:
        pasos.append(f"Error al resolver: {str(e)}")
    
    return pasos
