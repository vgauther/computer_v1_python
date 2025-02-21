import re
import sys


def split_expression(expression):
    terms = re.findall(r'[+-]?[^+-]+', expression)
    return [term.strip() for term in terms if term]

def contains_invalid_characters(expression):
    return not re.fullmatch(r'[0-9x+\-* .]+', expression)

def split_by_sign(expression):
    terms = re.split(r'(?=[+-])', expression.replace(' ', ''))
    return terms

def parse_polynomial(terms):
    result = []
    for s in terms:
        tmp = s.split('*')
        if len(tmp) != 2:
            result.append([float(s), 0])
        else:
            if 'x' in tmp[0]:
                if '^' in tmp[0]:
                    tmp2 = tmp[0].split("^")
                    if '.'in tmp2[-1]:
                        raise ValueError("L'exposant ne peux pas être à virgule")
                    result.append([float(tmp[1]), int(tmp2[-1])])
                else:
                    result.append([float(tmp[1]), 1])
            elif 'x' in tmp[1]:
                if '^' in tmp[1]:
                    tmp2 = tmp[1].split("^")
                    if '.'in tmp2[-1]:
                        raise ValueError("L'exposant ne peux pas être à virgule")
                    result.append([float(tmp[0]), int(tmp2[-1])])
                else:
                    result.append([float(tmp[0]), 1])
    return result

def parse_equation(equation):
    # Nettoyer et normaliser l'équation
    equation = equation.replace('*', '*')
    # equation = equation.replace('.', ',')
    equation = equation.replace(' ', '').lower()
    sides = equation.split('=')
    if len(sides) != 2:
        raise ValueError("L'équation doit contenir un et un seul signe égal.")
    
    left_terms = split_by_sign(sides[0])
    left_terms = parse_polynomial(left_terms)

    right_terms = split_by_sign(sides[1])
    right_terms = parse_polynomial(right_terms)
    
    print("Termes trouvés :")
    print("  Gauche :")
    print(left_terms)
    
    print("  Droite :")
    print(right_terms)

    # Initialiser les coefficients
    coefficients = {0: 0, 1: 0, 2: 0}

    # Traiter les termes
    for terms, sign in [(left_terms, 1), (right_terms, -1)]:
        for coef, exp in terms:
            if coef in ('', '+'):
                coef = 1
            elif coef == '-':
                coef = -1
            else:
                coef = float(coef)
            
            # Déterminer l'exposant
            if exp == '':
                exp = 1 if 'x' in terms[0][1] else 0
            else:
                exp = int(exp)
            
            if exp > 2:
                raise ValueError("Le degré de l'équation ne peut pas dépasser 2.")
            
            coefficients[exp] += sign * coef

    return coefficients

def solve_equation(coefficients):
    a, b, c = coefficients[2], coefficients[1], coefficients[0]
    
    if abs(a) < 1e-10 and abs(b) < 1e-10 and abs(c) < 1e-10:
        return "Tous les nombres réels sont solutions."
    elif abs(a) < 1e-10 and abs(b) < 1e-10:
        return "Pas de solution."
    elif abs(a) < 1e-10:
        return f"La solution est : {-c/b}"
    
    discriminant = b**2 - 4*a*c
    
    if discriminant > 0:
        x1 = (-b + discriminant**0.5) / (2*a)
        x2 = (-b - discriminant**0.5) / (2*a)
        return f"Les solutions sont : {x1} et {x2}"
    elif abs(discriminant) < 1e-10:
        x = -b / (2*a)
        return f"La solution unique est : {x}"
    else:
        real_part = -b / (2*a)
        imag_part = ((-discriminant)**0.5) / (2*a)
        return f"Les solutions complexes sont : {real_part} + {imag_part}i et {real_part} - {imag_part}i"

def main():
    if len(sys.argv) != 2:
        print("Usage: python computer_v1.py \"<équation>\"")
        sys.exit(1)

    equation = sys.argv[1]
    
    try:
        coefficients = parse_equation(equation)
        degree = max([k for k, v in coefficients.items() if abs(v) > 1e-10] or [0])
        
        print(f"Forme réduite : {coefficients[2]}x^2 + {coefficients[1]}x + {coefficients[0]} = 0")
        print(f"Degré polynômial : {degree}")
        
        solution = solve_equation(coefficients)
        print(solution)
    
    except ValueError as e:
        print(f"Erreur : {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
