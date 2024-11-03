import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import re
# import matplotlib.cm as cm

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
            # raise ValueError("Derivative is zero at the current point, can not continue.")
            print("Derivative is zero at the current point, can not continue.")
            error_code = "0 derivative"
            return x, x_history, error_code
        x = x - fx / dfx
        x_history.append(x)
    print("Maximum number of iterations reached without convergence.")
    error_code = "max iterations"
    return x, x_history, error_code

def get_function_input(symbol):
    while True:
        func_input = input("Enter the function f(x) (in terms of x, e.g., sin(x) - 2*x + exp(x): ")

        # Sanitize the input: allow valid characters and functions
        # This regex allows digits, operators, x, whitespace, parentheses, and common functions
        valid_input_pattern = r"^(?:\d+|\b(?:x|sin|cos|tan|exp|ln|log|sqrt)\b|\+|\-|\*{1,2}|\^|\/|\(|\)|\s)+$"
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
    
def get_guess_input():
    while True:
        guess_input = input("Enter the initial guess: ")
        try:
            guess_input = float(guess_input)
            return guess_input 
        except ValueError:
            print("Must enter a numeric value, try again.")
            continue


plt.ion()  # Enable interactive mode in order to run the program multiple times without closing plots

x = sp.symbols('x')
try:
    f, df = get_function_input(x)
except ValueError as e:
    print(f"Error: {e}")

while True:
    x0 = get_guess_input()
    root, x_history, error_code = newton_method(f, df, x0)
    if error_code is None:
        print(f"The root of the function is: {root:.6f}")
    else:
        print("Could not find the root, plotting the attempt.")

    # Plot the function and the tangent lines
    x_min = min(x_history + [-2]) - 0.05
    x_max = max(x_history + [2]) + 0.05
    x = np.linspace(x_min, x_max, 500)
    plt.figure(figsize=(8, 6))
    plt.plot(x, [f(xi) for xi in x], label='Function')

    cmap = plt.get_cmap('Dark2')                                                              # colour map for each iteration
    for i in range(len(x_history)):
        xi = x_history[i]
        fx = f(xi)
        dfx = df(xi)
        if dfx != 0:
            x_int = xi - fx / dfx
            this_color = cmap(i / max(1, len(x_history) - 1))
            plt.plot([xi, x_int], [fx, 0], '--', color=this_color, label=f'Iteration {i+1}')    # tangent line
            plt.plot([xi, xi], [fx, 0], '--', color=this_color)                                 # vertical line to function
            plt.plot(xi, fx, 'o', color=this_color, markersize=7)                               

    plt.plot(x_history[-1], f(x_history[-1]), 'ro', markersize=10, label='Root')
    plt.axhline(y=0, color='r', linestyle='-')                                                  # highlight x-axis
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Newton\'s Method')
    plt.legend()
    plt.grid()
    plt.show()

    # Ask the user if they want to run again
    run_again = input("Do you want to guess again? (y/n): ").strip().lower()
    if run_again != 'y':
        break

plt.ioff()  # Disable interactive mode
plt.close()  # Close all open plots
