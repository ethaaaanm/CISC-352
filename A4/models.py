import numpy as np
import nn

class PerceptronModel(object):
    def __init__(self, dim):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dim` is the dimensionality of the data.
        For example, dim=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dim)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x_point):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x_point: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        "*** YOUR CODE HERE ***"
        return nn.DotProduct(self.w, x_point)

    def get_prediction(self, x_point):
        """
        Calculates the predicted class for a single data point `x_point`.

        Returns: -1 or 1
        """
        "*** YOUR CODE HERE ***"
        score = nn.as_scalar(self.run(x_point))
        return 1 if score >= 0 else -1

    def train_model(self, dataset):
        """
        Train the perceptron until convergence.
        """
        converged = False
        while not converged:
            converged = True
            for x_point, y_label in dataset.iterate_once(1): # Batch size = 1 for perceptron
                y_scalar = nn.as_scalar(y_label)  # Convert label to scalar node
                if self.get_prediction(x_point) != y_scalar:
                    direction = nn.Constant(x_point.data * y_scalar)  
                    self.w.update(1.0, direction)  # Apply weight update
                    converged = False

class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """
    def __init__(self):
        "*** YOUR CODE HERE ***"
        hidden_size = 100  # Between 10 and 400

        self.w1 = nn.Parameter(1, hidden_size)
        self.b1 = nn.Parameter(1, hidden_size)
        self.w2 = nn.Parameter(hidden_size, 1)
        self.b2 = nn.Parameter(1, 1)

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** YOUR CODE HERE ***"
        hidden = nn.ReLU(nn.AddBias(nn.Linear(x, self.w1), self.b1))
        return nn.AddBias(nn.Linear(hidden, self.w2), self.b2)

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SquareLoss(self.run(x), y)

    def train_model(self, dataset):
        # Adjusted Learning Rate & Batch Size
        learning_rate = 0.01  
        batch_size = 50  
        iteration = 0  # Track iterations

        while True:
            total_loss = 0
            count = 0
            for x, y in dataset.iterate_once(batch_size):
                loss = self.get_loss(x, y)
                gradients = nn.gradients([self.w1, self.b1, self.w2, self.b2], loss)

                self.w1.update(-learning_rate, gradients[0])
                self.b1.update(-learning_rate, gradients[1])
                self.w2.update(-learning_rate, gradients[2])
                self.b2.update(-learning_rate, gradients[3])

                total_loss += nn.as_scalar(loss)
                count += 1

            avg_loss = total_loss / count
            iteration += 1

            if iteration % 100 == 0:  # Print every 10 iterations
                print(f"Iteration {iteration}, Avg Loss: {avg_loss}")

            if avg_loss < 0.02:
                break


class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        "*** YOUR CODE HERE ***"
        self.w1 = nn.Parameter(784, 128)
        self.b1 = nn.Parameter(1, 128)
        self.w2 = nn.Parameter(128, 64)
        self.b2 = nn.Parameter(1, 64)
        self.w3 = nn.Parameter(64, 32)
        self.b3 = nn.Parameter(1, 32)
        self.w4 = nn.Parameter(32, 10)
        self.b4 = nn.Parameter(1, 10)

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        # hidden layers
        hidden1 = nn.ReLU(nn.AddBias(nn.Linear(x, self.w1), self.b1))
        hidden2 = nn.ReLU(nn.AddBias(nn.Linear(hidden1, self.w2), self.b2))
        hidden3 = nn.ReLU(nn.AddBias(nn.Linear(hidden2, self.w3), self.b3))  
        return nn.AddBias(nn.Linear(hidden3, self.w4), self.b4) 

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SoftmaxLoss(self.run(x), y)

    def train_model(self, dataset):
        # Adjusted Learning Rate & Batch Size
        learning_rate = 0.1
        batch_size = 32


        for i in range(10000):  # Train for many iterations
            for x, y in dataset.iterate_once(batch_size):
                loss = self.get_loss(x, y)
                gradients = nn.gradients([self.w1, self.b1, self.w2, self.b2, self.w3, self.b3], loss)

                self.w1.update(-learning_rate, gradients[0])
                self.b1.update(-learning_rate, gradients[1])
                self.w2.update(-learning_rate, gradients[2])
                self.b2.update(-learning_rate, gradients[3])
                self.w3.update(-learning_rate, gradients[4]) 
                self.b3.update(-learning_rate, gradients[5])

            if i % 10 == 0:  # Print every 25 iterations
                accuracy = dataset.get_validation_accuracy()
                print(f"Iteration {i}, Validation Accuracy: {accuracy}")

                if accuracy >= 0.972:  
                    break