import numpy as np
import matplotlib.pyplot as plt
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
    x = x0
    x_history = [x]
    for i in range(max_iter):
        fx = f(x)
        print(f"Approximate root for iteration {i+1} is {x:.6f}")
        if abs(fx) < tol:
            return x, x_history
        dfx = df(x)
        if dfx == 0:
            raise ValueError("Derivative is zero at the current point.")
        x = x - fx / dfx
        x_history.append(x)
    raise ValueError("Maximum number of iterations reached without convergence.")

# Example usage
def f(x):
    return x**3 - 2*x + 1

def df(x):
    return 3*x**2 - 2

plt.ion()  # Enable interactive mode

while True:
    x0 = float(input("Enter the initial guess: "))
    root, x_history = newton_method(f, df, x0)
    print(f"The root of the function is: {root:.6f}")

    # Plot the function and the tangent lines
    x_min = min(x_history + [-2]) - 0.05
    x_max = max(x_history) + 0.05
    print(f"{x_min=}, {x_max=}")
    x = np.linspace(x_min, x_max, 500)
    plt.figure(figsize=(8, 6))
    plt.plot(x, [f(xi) for xi in x], label='Function')

    cmap = plt.get_cmap('viridis')
    for i in range(len(x_history)):
        xi = x_history[i]
        fx = f(xi)
        dfx = df(xi)
        x_int = xi - fx / dfx
        this_color = cmap(i / max(1, len(x_history) - 1))
        plt.plot([xi, x_int], [fx, 0], '--', color=this_color, label=f'Iteration {i+1}')
        plt.plot([xi, xi], [fx, 0], '--', color=this_color)
        plt.plot(xi, fx, 'o', color=this_color, markersize=7)

    plt.plot(x_history[-1], f(x_history[-1]), 'ro', markersize=10, label='Root')
    plt.axhline(y=0, color='r', linestyle='-')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Newton\'s Method')
    plt.legend()
    plt.grid()
    plt.show()

    # Ask the user if they want to run again
    run_again = input("Do you want to run again? (y/n): ").strip().lower()
    if run_again != 'y':
        break

plt.ioff()  # Disable interactive mode
plt.close()  # Close all open plots
