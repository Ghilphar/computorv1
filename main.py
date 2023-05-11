#!/usr/bin/env python3

import re
import argparse
import logging

def rounded_solution(solution):
    rounded_value = round(solution, 4)
    if rounded_value.is_integer():
        return(int(rounded_value))
    else:
        return(rounded_value)

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def setup_logger():
    # Create a custom logger
    logger = logging.getLogger(__name__)

    # Set the level of the logger. This is SUPER USEFUL since it enables you to control what level of logging you want
    logger.setLevel(logging.INFO)

    # Create handlers
    f_handler = logging.FileHandler('file.log')
    f_handler.setLevel(logging.INFO)

    # Create formatters and add it to handlers
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(f_handler)

    return logger

def parse_args():
    parser = argparse.ArgumentParser(description='Polynomial Solver')
    parser.add_argument('equation', type=str, nargs='*', help='The polynomial equation to solve or "visual" for visual mode')
    args = parser.parse_args()

    if len(args.equation) != 1:
        parser.error("Invalid number of arguments. Provide either a single polynomial equation or 'visual' to access visual mode.")

    equation = ' '.join(args.equation)

    if equation.lower() != 'visual':
        # Adjusted regex to allow a term without an exponent, and to allow spaces around the caret (^)
        if not re.match(r'^([+-]?\s*\d+(\.\d+)?\s*(\*\s*X(\s*\^\s*\d+)?)?\s*)+(=([+-]?\s*\d+(\.\d+)?\s*(\*\s*X(\s*\^\s*\d+)?)?\s*)+)$', equation):
            parser.error("Invalid polynomial equation. Please provide a valid polynomial equation.")
    return equation

def print_reduced_form(equation):
    # Initialize an empty dictionary
    terms = {}

    # Split the equation into left and right side
    left_side, right_side = equation.split('=')

    # Split the sides into terms
    left_terms = re.findall(r'([+-]?\s*\d+(\.\d+)?\s*(\*\s*X(\s*\^\s*\d+)?)?)', left_side)
    right_terms = re.findall(r'([+-]?\s*\d+(\.\d+)?\s*(\*\s*X(\s*\^\s*\d+)?)?)', right_side)
    
    # Parse left terms
    for term_tuple in left_terms:
        term = ''.join(term_tuple)
        matches = re.findall(r'([+-])?\s*(\d+(\.\d+)?)(\s*\*\s*X(\s*\^)?\s*(\d+)?)?', term)
        sign, coef, _, multiple_x, _, exp = matches[0] if len(matches[0]) == 6 else (*matches[0], None)
        #Fix the case of 2 * X
        if (multiple_x != '' and exp == ''):
            exp = 1
        coef = float(coef)
        exp = int(exp) if exp else 0  # consider the case where exponent is not present (constant term)
    
        if sign == '-':
            coef *= -1
    
        # Add the coef to the corresponding exp in the terms dictionary
        terms[exp] = terms.get(exp, 0) + coef
    
    # Parse right terms
    for term_tuple in right_terms:
        term = ''.join(term_tuple)
        matches = re.findall(r'([+-])?\s*(\d+(\.\d+)?)(\s*\*\s*X(\s*\^)?\s*(\d+)?)?', term)
        sign, coef, _, _, _, exp = matches[0] if len(matches[0]) == 6 else (*matches[0], None)
        coef = float(coef)
        exp = int(exp) if exp else 0  # consider the case where exponent is not present (constant term)
    
        if sign != '-':
            coef *= -1
    
        # Subtract the coef for the corresponding exp in the terms dictionary
        terms[exp] = terms.get(exp, 0) + coef
    


    # Print the reduced form
    reduced_form = 'Reduced form: '
    for exp, coef in sorted(terms.items()):
        if coef != 0:
            reduced_form += f'{coef} * X^{exp} + '

    # Remove the last ' + ' and add ' = 0'
    reduced_form = reduced_form[:-3] + ' = 0'

    print(reduced_form)
    return reduced_form



def print_polynomial_degree(reduced_form):
    # Initialize an empty dictionary
    polynomial = {}

    # Find all terms in the reduced form
    terms = re.findall(r'([+-]?\s*\d+(\.\d+)?)\s*\*\s*X\^(\d+)', reduced_form)

    # Determine the degree of the polynomial
    degree = max(int(exp) for coef, _, exp in terms)
    polynomial['degree'] = degree
    print(f"Polynomial degree: {degree}")

    if degree > 2:
        print("The polynomial degree is strictly greater than 2, I can't solve.")
        return {}

    # Extract a, b, and c from the terms
    for coef, _, exp in terms:
        coef = "".join(coef.split())
        exp = int(exp)
        coef = float(coef)
        if exp == 0:
            polynomial['c'] = coef
        elif exp == 1:
            polynomial['b'] = coef
        elif exp == 2:
            polynomial['a'] = coef

    # Fill in any missing coefficients with 0
    for var in ['a', 'b', 'c']:
        if var not in polynomial:
            polynomial[var] = 0.0

    return polynomial

def sqrt(n):
    x = n
    y = (x + 1) / 2

    while abs(y - x) > 0.000001:
        x = y
        y = (x + n / x) / 2

    return y

def solve_polynomial_degree_1(polynomial):
    b = polynomial['b']
    c = polynomial['c']
    
    # bx + c = 0  =>  x = -c / b
    solution = -c / b

    # Simplify the solution as a fraction
    gcd_value = gcd(-c, b)
    simplified_solution = (-c // gcd_value, b // gcd_value)


    solution = rounded_solution(solution)
    print(f"The solution is:\n{solution}")
    if (int(simplified_solution[1]) != 1):
        print(f"As an irreducible fraction: {simplified_solution[0]}/{simplified_solution[1]}")


def solve_polynomial_degree_2(polynomial):
    a = polynomial['a']
    b = polynomial['b']
    c = polynomial['c']
    
    # Discriminant: b^2 - 4ac
    discriminant = b**2 - 4*a*c

    if discriminant > 0:
        # Two solutions: (-b ± sqrt(discriminant)) / 2a
        root_discriminant = sqrt(discriminant)
        solution1 = (-b - root_discriminant) / (2*a)
        solution2 = (-b + root_discriminant) / (2*a)

        # Simplify the solutions as fractions
        gcd_value1 = gcd(int(-b - root_discriminant), int(2*a))
        simplified_solution1 = ((-b - root_discriminant) // gcd_value1, (2*a) // gcd_value1)

        gcd_value2 = gcd(int(-b + root_discriminant), int(2*a))
        simplified_solution2 = ((-b + root_discriminant) // gcd_value2, (2*a) // gcd_value2)

        print(f"Discriminant is strictly positive ({discriminant}), the two solutions are:")

        solution1 = rounded_solution(solution1)
        solution2 = rounded_solution(solution2)


        print(round(solution1, 4))
        if (int(simplified_solution1[1]) != 1):
            print(f"As an irreducible fraction: {simplified_solution1[0]}/{simplified_solution1[1]}")
        print(round(solution2, 4))
        if (int(simplified_solution2[1]) != 1):
            print(f"As an irreducible fraction: {simplified_solution2[0]}/{simplified_solution2[1]}")

    elif discriminant == 0:
        # One solution: -b / 2a
        solution = -b / (2*a)

        # Simplify the solution as a fraction
        gcd_value = gcd(-b, 2*a)
        simplified_solution = (-b // gcd_value, (2*a) // gcd_value)


        print(f"Discriminant is zero, the solution is:")
        solution = rounded_solution(solution)
        print(solution)
        if (int(simplified_solution[1]) != 1):
            print(f"As an irreducible fraction: {simplified_solution[0]}/{simplified_solution[1]}")

    else:
        # Discriminant is negative, no real solutions
        print(f"Discriminant is strictly negative ({discriminant}), there are no real solutions.")




def   solve_polynomial(polynomial):
    degree = polynomial.get("degree")
    if degree == 1:
        solve_polynomial_degree_1(polynomial)
    elif degree == 2:
        solve_polynomial_degree_2(polynomial)
    pass


def main():
    logger = setup_logger()
    equation = parse_args()

    logger.info(f'Solving equation: {equation}')
    # Here, you will add calls to your other functions for solving the polynomial
    reduced_form = print_reduced_form(equation)
    polynomial = print_polynomial_degree(reduced_form)
    solve_polynomial(polynomial)
    #print(polynomial)

if __name__ == "__main__":
    main()
