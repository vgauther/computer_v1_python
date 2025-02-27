import re
import sys

def square_root(value):
    return value**0.5

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
            result.append([round(float(s), 2), 0])
        else:
            if 'x' in tmp[0]:
                if '^' in tmp[0]:
                    tmp2 = tmp[0].split("^")
                    if '.'in tmp2[-1] or '-' in tmp2[-1]:
                        raise ValueError("L'exposant doit être un entier positif ou nul")
                    result.append([round(float(tmp[1]), 2), int(tmp2[-1])])
                else:
                    result.append([round(float(tmp[1]), 2), 1])
            elif 'x' in tmp[1]:
                if '^' in tmp[1]:
                    tmp2 = tmp[1].split("^")
                    if '.'in tmp2[-1] or '-' in tmp2[-1]:
                        raise ValueError("L'exposant doit être un entier positif ou nul")
                    result.append([round(float(tmp[0]), 2), int(tmp2[-1])])
                else:
                    result.append([round(float(tmp[0]), 2), 1])
    return result

def get_biggest_exp(terms):
    i = 0 
    biggest_exp = 0
    while i < len(terms):
        if terms[i][1] > biggest_exp: 
            biggest_exp = terms[i][1] 
        i = i + 1
    return biggest_exp + 1

def print_equation(reduce):
    if reduce[0] != 0:
        p = str(reduce[0])
    else:
        p = "0"
    if reduce[1] != 0:
        p = str(reduce[1]) + " * X +" + p
        i = 2
    while i < len(reduce):
        p = str(reduce[i]) + " * X^"+ str(i) +"+"+ p
        i = i + 1
    print(p)

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
    
    biggest_exp = get_biggest_exp(left_terms)
    left_reduce = [0] * biggest_exp

    for l_terms in left_terms:
        left_reduce[l_terms[1]] = left_reduce[l_terms[1]] + l_terms[0] 
        left_reduce[l_terms[1]] = round(left_reduce[l_terms[1]],3)
    

    r_biggest_exp = get_biggest_exp(right_terms)
    while biggest_exp < r_biggest_exp:
        left_reduce.append(0)
        biggest_exp = biggest_exp + 1

    for r_terms in right_terms:
        left_reduce[r_terms[1]] = left_reduce[r_terms[1]] - r_terms[0]
        left_reduce[r_terms[1]] = round(left_reduce[r_terms[1]],3)

    # Initialiser les coefficients
    coefficients = {0: 0, 1: 0, 2: 0}
    right_terms = [[0,0]]
    left_terms = []
    i = 0
    while i < len(left_reduce):
        if left_reduce[i] != 0:
            left_terms.append([left_reduce[i], i])
        i = i + 1

    # Traiter les termes
    for terms, sign in [(left_terms, 1), (right_terms, -1)]:
        for coef, exp in terms:
            if coef in ('', '+'):
                coef = 1
            elif coef == '-':
                coef = -1
            else:
                coef = round(float(coef), 2)
            
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
    
    discriminant = b*b - 4*a*c
    
    if discriminant > 0:
        x1 = (-b + square_root(discriminant)) / (2*a)
        x2 = (-b - square_root(discriminant)) / (2*a)
        return f"Les solutions sont : {x1} et {x2}"
    elif abs(discriminant) < 1e-10:
        x = -b / (2*a)
        return f"La solution unique est : {x}"
    else:
        real_part = -b / (2*a)
        imag_part = (square_root((-discriminant))) / (2*a)
        print("Les solutions complexes non reduites")
        print( "x1 = (-" + str(b) + " - i√" + str( -1* discriminant) + ") / " + str(2 * a))
        print( "x2 = (-" + str(b) + " + i√" + str( -1* discriminant) + ") / " + str(2 * a))

        return f"Les solutions complexes sont : {real_part} + {imag_part}i et {real_part} - {imag_part}i"

def main():
    if len(sys.argv) != 2:
        print("Usage: python computer_v1.py \"<équation>\"")
        sys.exit(1)

    equation = sys.argv[1]
    
    try:
        coefficients = parse_equation(equation)
        degree = max([k for k, v in coefficients.items() if abs(v) > 1e-10] or [0])
        
        terms = []
        if abs(coefficients.get(2, 0)) > 1e-10:
            terms.append(f"{coefficients[2]}x^2")
        if abs(coefficients.get(1, 0)) > 1e-10:
            terms.append(f"{coefficients[1]}x")
        if abs(coefficients.get(0, 0)) > 1e-10:
            terms.append(f"{coefficients[0]}")
        # Joindre les termes avec des signes appropriés
        forme_reduite = " + ".join(terms).replace("+-", "- ") if terms else "0"

        print(f"Forme réduite : {forme_reduite} = 0")
        print(f"Degré polynômial : {degree}")
        
        solution = solve_equation(coefficients)
        print(solution)
    
    except ValueError as e:
        print(f"Erreur : {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
