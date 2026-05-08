#Question 5

data = [
    (-4,  0, -1),
    (-1,  1, +1),
    ( 0, -1, -1),
    ( 2,  1, +1),
    ( 3,  0, +1),
    ( 6, -1, -1),
]

# Hyperparameters
learning_rate = 0.1
threshold = 1e-5
max_iter = 1000

# Initialize weights
w0, w1, w2 = 0.0, 0.0, 0.0

def compute_gradients(w0, w1, w2, data):
    grad_w0 = 0.0
    grad_w1 = 0.0
    grad_w2 = 0.0
    for x1, x2, y in data:
        y_hat = w0 + w1 * x1 + w2 * x2
        # Only do gradient if margin is violated (yyhat < 1)
        if y * y_hat < 1:
            grad_w0 += -y
            grad_w1 += -y * x1
            grad_w2 += -y * x2
    return grad_w0, grad_w1, grad_w2

def misclassification_rate(w0, w1, w2, data):
    errors = 0
    for x1, x2, y in data:
        h = w0 + w1 * x1 + w2 * x2
        y_pred = 1 if h >= 0 else -1
        if y_pred != y:
            errors += 1
    return errors / len(data)

# Gradient descent loop
for iteration in range(1, max_iter + 1):
    grad_w0, grad_w1, grad_w2 = compute_gradients(w0, w1, w2, data)

    # Update weights
    new_w0 = w0 - learning_rate * grad_w0
    new_w1 = w1 - learning_rate * grad_w1
    new_w2 = w2 - learning_rate * grad_w2

    # Check convergence
    change = max(abs(new_w0 - w0), abs(new_w1 - w1), abs(new_w2 - w2))

    w0, w1, w2 = new_w0, new_w1, new_w2

    if change < threshold:
        print(f"Converged at iteration {iteration}")
        break
else:
    print(f"Reached max iterations ({max_iter})")

print(f"\nGD Results")
print(f"w0 = {w0}, w1 = {w1}, w2 = {w2}")
print(f"Training misclassification rate: {misclassification_rate(w0, w1, w2, data)}")

# Compare to SGD final weights
sgd_w0, sgd_w1, sgd_w2 = -0.1, -0.1, 0.4
sgd_error = misclassification_rate(sgd_w0, sgd_w1, sgd_w2, data)
print(f"\nSGD Results (1 pass) (same as question 4)")
print(f"w0 = {sgd_w0}, w1 = {sgd_w1}, w2 = {sgd_w2}")
print(f"Training misclassification rate: {sgd_error}")