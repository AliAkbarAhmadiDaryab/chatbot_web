# The class for plotting
import numpy as np
import matplotlib.pyplot as plt
import torch


class plot_diagram():

    # Constructor
    def __init__(self, X, Y, w, stop, go=False):
        start = w.data
        self.error = []
        self.parameter = []
        self.X = X.numpy()
        self.Y = Y.numpy()
        self.parameter_values = torch.arange(start, stop)
        self.Loss_function = [criterion(forward(X), Y) for w.data in self.parameter_values]
        w.data = start

    # Executor
    def __call__(self, Yhat, w, error, n):
        self.error.append(error)
        self.parameter.append(w.data)
        plt.subplot(212)
        plt.plot(self.X, Yhat.detach().numpy())
        plt.plot(self.X, self.Y, 'ro')
        plt.xlabel("A")
        plt.ylim(-20, 20)
        plt.subplot(211)
        plt.title("Data Space (top) Estimated Line (bottom) Iteration " + str(n))
        plt.plot(self.parameter_values.numpy(), self.Loss_function)
        plt.plot(self.parameter, self.error, 'ro')
        plt.xlabel("B")
        plt.figure()

    # Destructor
    def __del__(self):
        plt.close('all')


def criterion(yhat, y):
    return torch.mean((yhat - y) ** 2)


def forward(x):
    return w * x


if __name__ == '__main__':
    X = torch.arange(-3, 3, 0.1).view(-1, 1)
    f = -3 * X

    plt.plot(X.numpy(), f.numpy(), label='F_Function')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.show()

    # Add some noise to f(X) and save it in Y

    Y = f + 0.1 * torch.randn(X.size())

    # Plot the data points

    plt.plot(X.numpy(), Y.numpy(), 'rx', label='Y')

    plt.plot(X.numpy(), f.numpy(), label='f')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.show()

    lr = 0.1
    LOSS = []

    w = torch.tensor(-10.0, requires_grad=True)

    gradient_plot = plot_diagram(X, Y, w, stop=5)
