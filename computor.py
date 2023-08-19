import re
import sys
import matplotlib.pyplot as plt  #Only for bonus graph
import numpy as np #Only for bonus graph


def plot_solution(degree, summed_terms, solutions):
    x = np.linspace(-10, 10, 400)

    if degree == 1:
        y = summed_terms.get(1, 0) * x + summed_terms.get(0, 0)
        plt.plot(x, y, '-r', label=f'{summed_terms.get(1, 0)}x + {summed_terms.get(0, 0)}')
        plt.title('Graph of Degree 1 Polynomial')
        plt.xlabel('x', color='#1C2833')
        plt.ylabel('y', color='#1C2833')
        plt.axhline(0, color='black',linewidth=0.5)
        plt.axvline(0, color='black',linewidth=0.5)
        plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
        plt.legend(loc='upper left')
        plt.scatter(solutions, [0 for _ in solutions], color='blue')  # roots of the equation
        plt.show()

    elif degree == 2:
        y = summed_terms.get(2, 0) * x**2 + summed_terms.get(1, 0) * x + summed_terms.get(0, 0)
        plt.plot(x, y, '-r', label=f'{summed_terms.get(2, 0)}x^2 + {summed_terms.get(1, 0)}x + {summed_terms.get(0, 0)}')
        plt.title('Graph of Degree 2 Polynomial')
        plt.xlabel('x', color='#1C2833')
        plt.ylabel('y', color='#1C2833')
        plt.axhline(0, color='black',linewidth=0.5)
        plt.axvline(0, color='black',linewidth=0.5)
        plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
        plt.legend(loc='upper left')
        if all(isinstance(sol, (int, float)) for sol in solutions):  # Check if solutions are real
            plt.scatter(solutions, [summed_terms.get(2, 0) * sol**2 + summed_terms.get(1, 0) * sol + summed_terms.get(0, 0) for sol in solutions], color='blue')  # roots of the equation
        plt.show()

def identify_and_split_terms(polynomial_terms):
    identified_terms = []
    number_pattern = re.compile(r'^[+-]?(\d+(\.\d+)?|\.\d+)$')
    x_pattern = re.compile(r'^[+-]?\s*X(?!\^)$')
    x_with_star_pattern = re.compile((r'^[+-]?\s*\d+\s*\*\s*X(?!\^)$'))
    x_power_pattern = re.compile(r'^[+-]?\s*X\^\d+$')
    
    for term in polynomial_terms:
        clean_term = term.replace(' ', '')
        if x_with_star_pattern.match(clean_term):
            # Split the term into coefficient and variable parts and treat X as X^1
            coefficient_part, _ = clean_term.split('*')
            variable_part = "X^1"
            identified_terms.append((coefficient_part.strip(), variable_part))
        elif '*' in clean_term:
            # Split the term into coefficient and variable parts
            coefficient_part, variable_part = term.split('*')
            identified_terms.append((coefficient_part.strip(), variable_part.strip()))
        elif number_pattern.match(clean_term):
            coefficient_part = term.strip()
            variable_part = "X^0"
            identified_terms.append((coefficient_part, variable_part))
        elif x_pattern.match(clean_term):
            # If term is just X, consider it as 1 * X^1
            sign = "-" if "-" in clean_term else ""
            coefficient_part = f"{sign}1"
            variable_part = "X^1"
            identified_terms.append((coefficient_part, variable_part))
        elif x_power_pattern.match(clean_term):
            # If term is X raised to a power, consider coefficient as 1
            sign = ''
            if '-' in clean_term:
                sign = '-'
            elif '+' in clean_term:
                sign = '+'
            coefficient_part = f"{sign}1"
            variable_part = clean_term.replace(sign, "")
            identified_terms.append((coefficient_part, variable_part))
        else:
            print(f"We didn't manage to identify this {clean_term}")
            sys.exit(1)
    #print(identified_terms)
    return identified_terms


def extract_and_sum_terms(identified_terms):
    # Dictionary to store summed coefficients by their exponent
    summed_terms = {}
    
    # Regex to check for the form X^N and extract the exponent
    variable_pattern = re.compile(r'^X\^(\d+)$')
    
    for part1, part2 in identified_terms:
        exponent = None
        coefficient = None

        if variable_pattern.match(part1):
            exponent = int(variable_pattern.match(part1).group(1))
            try:
                coefficient = float(part2.replace(' ', ''))
            except ValueError:
                print(f"Error: {part2} is not a valid coefficient in the term {part1} * {part2}")
                sys.exit(1)
        elif variable_pattern.match(part2):
            exponent = int(variable_pattern.match(part2).group(1))
            try:
                coefficient = float(part1.replace(' ', ''))
            except ValueError:
                print(f"Error: {part1} is not a valid coefficient in the term {part1} * {part2}")
                sys.exit(1)
        else:
            print(f"Error: Invalid term structure for {part1} * {part2}")
            sys.exit(1)

        # Sum the coefficients by their exponent
        summed_terms[exponent] = summed_terms.get(exponent, 0) + coefficient

    return summed_terms


def generate_reduced_form_output(summed_terms):
    # Sort the dictionary by keys (exponents) in ascending order
    sorted_terms = sorted(summed_terms.items(), key=lambda x: int(x[0]))

    # Construct the reduced form string
    terms_strings = []
    for exponent, coefficient in sorted_terms:
        if coefficient != 0:  # Exclude terms with a coefficient of 0
            term_str = f"{coefficient} * X^{exponent}"
            terms_strings.append(term_str)

    # Join the terms to create the reduced form
    reduced_form = " + ".join(terms_strings).replace(" + -", " - ") + " = 0"

    # Determine the polynomial degree
    # print(sorted_terms)
    
    for term_degree, coefficient in reversed(sorted_terms):
        if coefficient != 0:
            degree = int(term_degree)
            break
        degree = 0

    return reduced_form, degree

def solve_polynomial_degree_1(summed_terms):
    # Extracting coefficients
    a = summed_terms.get(1, 0)
    b = summed_terms.get(0, 0)

    # If a is 0, it's not a valid degree 1 polynomial
    if a == 0:
        print("Invalid degree 1 polynomial.")
        sys.exit(1)
    # Calculating the solution
    x = -b/a
    return [x]

def solve_polynomial_degree_2(summed_terms):
    # Extracting coefficients
    a = summed_terms.get(2, 0)  # Coefficient of X^2
    b = summed_terms.get(1, 0)  # Coefficient of X^1
    c = summed_terms.get(0, 0)  # Constant term

    # Calculate the discriminant
    discriminant = b**2 - 4*a*c

    # Checking the nature of the roots based on the discriminant
    if discriminant > 0:
        # Two distinct real roots
        x1 = (-b + discriminant**0.5) / (2*a)
        x2 = (-b - discriminant**0.5) / (2*a)
        return discriminant, [x1, x2]
    elif discriminant == 0:
        # One real root (or repeated real root)
        x = -b / (2*a)
        return discriminant, [x]
    else:
        # Complex conjugate roots
        real_part = -b / (2*a)
        imaginary_part = (abs(discriminant)**0.5) / (2*a)
        complex_root1 = (real_part, imaginary_part)
        complex_root2 = (real_part, -imaginary_part)
        return discriminant, [complex_root1, complex_root2]

def solve_polynomial(degree, summed_terms):
    if degree == 0:
        if summed_terms.get(0, 0) == 0:  # Using the key '0' for the constant term
            print("All real numbers are solution")
        else:
            print("There are no solutions")
        return []
    elif degree == 1:
        solution = solve_polynomial_degree_1(summed_terms)
        if solution:
            print("The solution is:", solution[0])
            return solution
    elif degree == 2:
        discriminant, solution = solve_polynomial_degree_2(summed_terms)
        if solution:
            if discriminant > 0:
                print("Discriminant is strictly positive, the two solutions are:")
                print(solution[0])
                print(solution[1])
                return solution
            elif discriminant == 0:
                print("Discriminant is equal to 0, there is only one solution.")
                print(solution[0])
                return solution
            elif discriminant < 0:
                print("Discriminant is negative, there is 2 imaginary solutions.")
                print(f"{solution[0][0]} + {solution[0][1]}i")
                print(f"{solution[1][0]} {solution[1][1]}i")
    else:
        print("The polynomial degree is strictly greater than 2, I can't solve.")
        return []

def main(equation, visual):
    # Split the equation into left and right side
    left_side, right_side = equation.split('=')

    # Split the sides into values
    left_terms = re.findall(r'([+-]?[^-+]+)', left_side)
    right_terms = re.findall(r'([+-]?[^-+]+)', right_side)
    
    for i, term in enumerate(right_terms):
        if term.startswith('-'):
            right_terms[i] = '+' + term[1:]
        elif term.startswith('+'):
            right_terms[i] = '-' + term[1:]
        else:
            right_terms[i] = '-' + term
    
    polynomial_terms = left_terms + right_terms

    #print("Combined terms:", polynomial_terms)
    identified_terms = identify_and_split_terms(polynomial_terms)
    #print("Categorized terms:", identified_terms)
    
    summed_terms = extract_and_sum_terms(identified_terms)
    #print(summed_terms)
    reduced_form, degree =generate_reduced_form_output(summed_terms)
    print("Reduced form:", reduced_form)
    print("Polynomial degree:", degree)
    solutions = solve_polynomial(degree, summed_terms)
    if solutions and visual:
        plot_solution(degree, summed_terms, solutions)
    return

if __name__ == "__main__":
    # Check if equation argument is provided

    if len(sys.argv) == 2:
        equation = sys.argv[1].strip()
        visual = False
        main(equation, visual)
    elif len(sys.argv) == 3 and sys.argv[2] == '-v':
        equation = sys.argv[1].strip()
        visual= True
        main(equation, visual)
    else:
        print("Please provide an equation as an argument.")
        sys.exit(1)
    # Read the equation from the command-line arguments