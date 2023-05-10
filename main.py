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

    equation = args.equation[0]
    if equation.lower() != 'visual':
        if not re.match(r'^([+-]?\s*\d+(\.\d+)?\s*\*\s*X\^\d+\s*)+=\s*([+-]?\s*\d+(\.\d+)?\s*\*\s*X\^0\s*)+$', equation):
            parser.error("Invalid polynomial equation. Please provide a valid polynomial equation.")

        # Extract exponents from the left side of the equation
        left_side = equation.split('=')[0]
        exponents = re.findall(r'X\^(\d+)', left_side)

        # Check if there are duplicate exponents
        if len(exponents) != len(set(exponents)):
            parser.error("Invalid polynomial equation. Each term on the left side of the equation must have a unique exponent.")

    return equation


def main():
    logger = setup_logger()
    equation = parse_args()

    logger.info(f'Solving equation: {equation}')
    # Here, you will add calls to your other functions for solving the polynomial

if __name__ == "__main__":
    main()
