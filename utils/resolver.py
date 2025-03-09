import sympy as sp
import re

def corregir_multiplicacion_implicita(expresion):
    """Corrige la notación matemática implícita, reemplazando casos como '3x' con '3*x'."""
    expresion = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expresion)
    expresion = re.sub(r'([a-zA-Z])([a-zA-Z])', r'\1*\2', expresion)
    expresion = expresion.replace('^', '**')
    return expresion
def latex_sin_left_right(expresion):
    """Convierte una expresión de SymPy a LaTeX sin \left y \right."""
    return sp.latex(expresion, mode='plain').replace(r"\left", "").replace(r"\right", "")

def resolver_expresion(expresion):
    pasos = []
    
    try:
        sp.init_printing(use_unicode=True)
        expresion = corregir_multiplicacion_implicita(expresion)

        if "=" in expresion:
            izquierda, derecha = expresion.split("=")
            izquierda = sp.sympify(izquierda)
            derecha = sp.sympify(derecha)
            x = sp.Symbol('x')  # Definir variable principal
            ecuacion = sp.Eq(izquierda, derecha)
            pasos.append(f"**Ecuación dada:**\n{latex_sin_left_right(ecuacion)}")

            # Paso 1: Pasar todo al lado izquierdo
            ecuacion_transformada = sp.simplify(izquierda - derecha)
            pasos.append(f"**Paso 1:** Restamos ambos lados para igualar a 0:\n{latex_sin_left_right(ecuacion_transformada)} = 0")

            # Intentamos factorizar
            ecuacion_factorizada = sp.factor(ecuacion_transformada)
            if ecuacion_factorizada != ecuacion_transformada:
                pasos.append(f"**Paso 2:** Factorizamos la ecuación:\n{latex_sin_left_right(ecuacion_factorizada)} = 0")
            else:
                pasos.append("**Paso 2:** No se puede factorizar, aplicamos la fórmula cuadrática si es de segundo grado.")

            # Intentamos resolver con la fórmula cuadrática
            coeficientes = sp.Poly(ecuacion_transformada, x).all_coeffs()
            if len(coeficientes) == 3:  # Solo aplicamos si es cuadrática
                a, b, c = coeficientes
                discriminante = b**2 - 4*a*c
                pasos.append(f"**Paso 3:** Calculamos el discriminante:\nΔ = {b}² - 4({a})({c}) = {discriminante}")

                if discriminante >= 0:
                    solucion1 = (-b - sp.sqrt(discriminante)) / (2*a)
                    solucion2 = (-b + sp.sqrt(discriminante)) / (2*a)
                    pasos.append(f"**Paso 4:** Aplicamos la fórmula cuadrática:")
                    pasos.append(f"x₁ = {latex_sin_left_right(solucion1)}")
                    pasos.append(f"x₂ = {latex_sin_left_right(solucion2)}")
                else:
                    pasos.append("El discriminante es negativo, no hay soluciones reales.")
            else:
                # Resolver directamente si es lineal
                solucion = sp.solve(ecuacion_transformada, x)
                pasos.append(f"**Solución:** x = {latex_sin_left_right(solucion)}")

        else:
            # Si no es una ecuación, simplemente simplificar
            expr = sp.sympify(expresion)
            pasos.append(f"**Expresión original:**\n{latex_sin_left_right(expr)}")

            # Expandir si es posible
            expr_expandida = sp.expand(expr)
            if expr_expandida != expr:
                pasos.append(f"**Paso 1:** Expandimos la expresión:\n{latex_sin_left_right(expr_expandida)}")
            
            # Factorizar si es posible
            expr_factorizada = sp.factor(expr_expandida)
            if expr_factorizada != expr_expandida:
                pasos.append(f"**Paso 2:** Factorizamos la expresión:\n{latex_sin_left_right(expr_factorizada)}")

            # Simplificar
            expr_simplificada = sp.simplify(expr_factorizada)
            pasos.append(f"**Paso 3:** Simplificamos la expresión:\n{latex_sin_left_right(expr_simplificada)}")


    except Exception as e:
        pasos.append(f"⚠️ **Error al resolver:** {str(e)}")
    
    return pasos
