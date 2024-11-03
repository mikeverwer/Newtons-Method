import numpy as np
import sympy as sp
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import re

def newton_method(f, df, x0, tol=1e-6, max_iter=100):
    """
    Finds the root of a function using Newton's method.

    Parameters:
    f (function): The function whose root is to be found.
    df (function): The derivative of the function f.
    x0 (float): The initial guess for the root.
    tol (float): The tolerance for the root.
    max_iter (int): The maximum number of iterations.

    Returns:
    float: The root of the function.
    list: The history of x values at each iteration.
    """
    error_code = None
    x = x0
    x_history = [x]
    for i in range(max_iter):
        fx = f(x)
        print(f"Approximate root for iteration {i+1} is {x:.6f}")
        if abs(fx) < tol:
            return x, x_history, error_code
        dfx = df(x)
        if dfx == 0:
            print("Derivative is zero at the current point, can not continue.")
            error_code = "0 derivative"
            return x, x_history, error_code
        x = x - fx / dfx
        x_history.append(x)
    print("Maximum number of iterations reached without convergence.")
    error_code = "max iterations"
    return x, x_history, error_code


def create_functions(symbol):
    while True:
        func_input = input("Enter the function f(x) (in terms of x, e.g., sin(x) - x + exp(x) - 2: ")

        # Sanitize the input: allow valid characters and functions
        # This regex allows digits, operators, x, whitespace, parentheses, and common functions
        valid_input_pattern = r"^(?:\d+|\b(?:x|asin|acos|atan|sin|cos|tan|exp|ln|log|sqrt)\b|\+|\-|\*{1,2}|\^|\/|\(|\)|\s)+$"
        if not re.match(valid_input_pattern, func_input):
            print("Invalid input. Please use only numbers, x, and mathematical operators.")
            continue  # Prompt the user again

        # Replace '^' with '**' for Python syntax
        func_input = func_input.replace('^', '**')

        try:
            sym_f = sp.sympify(func_input)
            sym_df = sym_f.diff(symbol)

            f_callable = sp.lambdify(symbol, sym_f, 'numpy')
            df_callable = sp.lambdify(symbol, sym_df, 'numpy')
            
            return f_callable, df_callable
        except sp.SympifyError:
            print("Invalid input. Please enter a valid mathematical expression.")
            continue  # Prompt the user again

   
def ask_for_function(symbol):
    try:
        lambda_f, lambda_df = create_functions(symbol)
        return lambda_f, lambda_df
    except ValueError as e:
        print(f"Error: {e}")


def get_guess_input():
    while True:
        guess_input = input("Enter the initial guess: ")
        try:
            guess_input = float(guess_input)
            return guess_input 
        except ValueError:
            print("Must enter a numeric value, try again.")
            continue


def plot_function_and_tangents(f, df, x_history):
    # Create a new Matplotlib figure
    figure = plt.figure(figsize=(8, 6))
    ax = figure.add_subplot(111)

    # Define the range for x values
    x_min = min(x_history + [-2]) - 0.05
    x_max = max(x_history + [2]) + 0.05
    x = np.linspace(x_min, x_max, 500)

    # Plot the function
    ax.plot(x, [f(xi) for xi in x], label='Function')

    cmap = plt.get_cmap('Dark2')                                                             # Color map for each iteration
    for i in range(len(x_history)):
        xi = x_history[i]
        fx = f(xi)
        dfx = df(xi)
        if dfx != 0:
            x_int = xi - fx / dfx
            this_color = cmap(i / max(1, len(x_history) - 1))
            ax.plot([xi, x_int], [fx, 0], '--', color=this_color, label=f'Iteration {i+1}')  # Tangent line
            ax.plot([xi, xi], [fx, 0], '--', color=this_color)                               # Vertical line to function
            ax.plot(xi, fx, 'o', color=this_color, markersize=7)

    ax.plot(x_history[-1], f(x_history[-1]), 'ro', markersize=10, label='Root')
    ax.axhline(y=0, color='r', linestyle='-')                                               # Highlight x-axis
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.set_title('Newton\'s Method')
    ax.legend()
    ax.grid()

    plt.show(block=False)
    plt.pause(0.1)


# Main loop for user input and plotting
author = "\n|----------------------------------------|\n| Made by Mike Verwer, M.Sc. Mathematics |\n|----------------------------------------|\n"
print(author)

x = sp.symbols('x')

f, df = ask_for_function(x)

while True:
    x0 = get_guess_input()
    root, x_history, error_code = newton_method(f, df, x0)
    if error_code is None:
        print(f"The root of the function is: {root:.6f}")
    else:
        print("Could not find the root, plotting the attempt.")
    
    plot_function_and_tangents(f, df, x_history)

    # Ask the user if they want to run again
    run_again = input("Do you want to guess again? (y/n): ").strip().lower()
    if run_again != 'y':
        run_with_new_function = input("Would you like to use a different function? (y/n): ").strip().lower()
        if run_with_new_function != 'y':
            print(author)
            break
        else:
            f, df = ask_for_function(x)

plt.close('all')  # Close all open plots
