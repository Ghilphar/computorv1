#!/usr/bin/env python3

import re
import argparse
import logging
import sys

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
        if not re.match(r'^([+-]?\s*\d+(\.\d+)?\s*\*\s*X\^\d+\s*)+=\s*([+-]?\s*\d+(\.\d+)?\s*\*\s*X\^\d+\s*)+$', equation):
            parser.error("Invalid polynomial equation. Please provide a valid polynomial equation.")

        # Extract exponents from the left side of the equation
        left_side = equation.split('=')[0]
        exponents = re.findall(r'X\^(\d+)', left_side)

        # Check if there are duplicate exponents
        if len(exponents) != len(set(exponents)):
            parser.error("Invalid polynomial equation. Each term on the left side of the equation must have a unique exponent.")

    return equation

def print_reduced_form(equation):
    # Initialize an empty dictionary
    terms = {}

    # Split the equation into left and right side
    left_side, right_side = equation.split('=')

    # Split the sides into terms
    left_terms = re.findall(r'([+-]?\s*\d+(\.\d+)?\s*\*\s*X\^\d+)', left_side)
    right_terms = re.findall(r'([+-]?\s*\d+(\.\d+)?\s*\*\s*X\^\d+)', right_side)

    # Parse left terms
    for term in left_terms:
        term = term[0]  # Convert the tuple to string
        sign, coef, _, exp = re.findall(r'([+-])?\s*(\d+(\.\d+)?)\s*\*\s*X\^(\d+)', term.strip())[0]
        coef = float(coef)
        exp = int(exp)

        if sign == '-':
            coef *= -1

        # Add the coef to the corresponding exp in the terms dictionary
        terms[exp] = terms.get(exp, 0) + coef

    # Parse right terms
    for term in right_terms:
        term = term[0]  # Convert the tuple to string
        sign, coef, _, exp = re.findall(r'([+-])?\s*(\d+(\.\d+)?)\s*\*\s*X\^(\d+)', term.strip())[0]
        coef = float(coef)
        exp = int(exp)

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


def main():
    logger = setup_logger()
    equation = parse_args()

    logger.info(f'Solving equation: {equation}')
    # Here, you will add calls to your other functions for solving the polynomial
    print_reduced_form(equation)


if __name__ == "__main__":
    main()
