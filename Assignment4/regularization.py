#------------------------------------
# Author: T. D. Devlin
#-----------------------------------

import math
from math import sin, pi
from random import random, seed


def f(x):
    return sin(pi * x)


def generate_training_examples(n=2):
    xs = [random() * 2 - 1 for _ in range(n)]
    return [(x, f(x)) for x in xs]


def fit_without_reg(examples):
    """Computes values of w0 and w1 that minimize the sum-of-squared-errors cost function.

    With n = 2 training points and no regularization, the unique line through the two
    points is the global minimizer of C(w) (it makes both squared errors zero).
    Given (x1, y1) and (x2, y2):
        w1 = (y2 - y1) / (x2 - x1)
        w0 = y1 - w1 * x1
    """
    (x1, y1), (x2, y2) = examples[0], examples[1]
    if x1 == x2:
        w1 = 0.0
        w0 = (y1 + y2) / 2.0
        return w0, w1
    w1 = (y2 - y1) / (x2 - x1)
    w0 = y1 - w1 * x1
    return w0, w1


def fit_with_reg(examples, lambda_hp):
    """Minimize the L2-regularized SSE cost via gradient descent.

    Cost: C_tilde(w) = sum_i (y_i - (w0 + w1 x_i))^2 + lambda*(w0^2 + w1^2)
    Gradients:
        dC/dw0 = -2 * sum_i (y_i - (w0 + w1 x_i)) + 2 * lambda * w0
        dC/dw1 = -2 * sum_i x_i * (y_i - (w0 + w1 x_i)) + 2 * lambda * w1

    Step size eta = 0.05, 1000 iterations, init w0 = w1 = 0.
    """
    eta = 0.05
    num_iters = 1000

    w0 = 0.0
    w1 = 0.0
    for _ in range(num_iters):
        grad_w0 = 0.0
        grad_w1 = 0.0
        for x_i, y_i in examples:
            residual = y_i - (w0 + w1 * x_i)
            grad_w0 += -2.0 * residual
            grad_w1 += -2.0 * x_i * residual
        grad_w0 += 2.0 * lambda_hp * w0
        grad_w1 += 2.0 * lambda_hp * w1
        w0 -= eta * grad_w0
        w1 -= eta * grad_w1
    return (w0, w1)


def test_error(w0, w1):
    n = 100
    xs = [i / n for i in range(-n, n + 1)]
    return sum((w0 + w1 * x - f(x)) ** 2 for x in xs) / len(xs)


def run_simulation(num_trials=1000, lambda_hp=1.0, rng_seed=0):
    """Run the experiment in Question 5 and return averages + per-trial weights."""
    seed(rng_seed)
    weights_no_reg = []
    weights_with_reg = []
    err_no_reg_total = 0.0
    err_with_reg_total = 0.0
    for _ in range(num_trials):
        examples = generate_training_examples(n=2)
        w0_a, w1_a = fit_without_reg(examples)
        w0_b, w1_b = fit_with_reg(examples, lambda_hp)
        weights_no_reg.append((w0_a, w1_a))
        weights_with_reg.append((w0_b, w1_b))
        err_no_reg_total += test_error(w0_a, w1_a)
        err_with_reg_total += test_error(w0_b, w1_b)
    avg_no_reg = err_no_reg_total / num_trials
    avg_with_reg = err_with_reg_total / num_trials
    return avg_no_reg, avg_with_reg, weights_no_reg, weights_with_reg


def plot_trials(weights_no_reg, weights_with_reg, out_path="regularization_plot.png"):
    """Question 6 (EC): plot all fitted lines + target function f(x) = sin(pi x)."""
    import matplotlib.pyplot as plt

    n = 200
    xs = [i / n for i in range(-n, n + 1)]
    ys_target = [f(x) for x in xs]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

    for ax, weights, title in (
        (axes[0], weights_no_reg, "Without regularization"),
        (axes[1], weights_with_reg, "With L2 regularization (lambda=1)"),
    ):
        for w0, w1 in weights:
            ys = [w0 + w1 * x for x in xs]
            ax.plot(xs, ys, color="red", linewidth=0.4, alpha=0.05)
        ax.plot(xs, ys_target, color="black", linewidth=2.0, label=r"$f(x)=\sin(\pi x)$")
        ax.set_title(title)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_xlim(-1, 1)
        ax.set_ylim(-2.5, 2.5)
        ax.legend(loc="upper left")
        ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    print(f"Saved figure to {out_path}")


if __name__ == "__main__":
    avg_no_reg, avg_with_reg, w_no, w_yes = run_simulation(
        num_trials=1000, lambda_hp=1.0, rng_seed=0
    )
    print("Question 5 results (averaged over 1000 trials):")
    print(f"  Avg test error without regularization: {avg_no_reg:.4f}")
    print(f"  Avg test error with    regularization: {avg_with_reg:.4f}")

    try:
        plot_trials(w_no, w_yes, out_path="regularization_plot.png")
    except Exception as exc:
        print(f"(Plot skipped: {exc})")
