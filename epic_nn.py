import random
import math
import json

import names
import sets


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


class NeuralNetwork:
    def __init__(self, num_input, num_hidden, num_output, training_sets, learning_rate=0.05, weights_biases=None):
        self.num_input = num_input
        self.hidden_layer = NeuronLayer(num_hidden)
        self.output_layer = NeuronLayer(num_output)
        self.learning_rate = learning_rate
        if weights_biases == None:
            self.init_weights()
            print('Training...')
            self.train(training_sets)
            print('Done Training.')
        else:
            self.read_weights(weights_biases)

    def init_weights(self):
        for neuron in self.hidden_layer.neurons:
            neuron.weights = [
                random.random()-0.5 for _ in range(self.num_input)]

        for neuron in self.output_layer.neurons:
            neuron.weights = [random.random()-0.5
                              for _ in self.hidden_layer.neurons]

    def read_weights(self, weights_biases):
        for i, n in enumerate(self.hidden_layer.neurons):
            n.weights = weights_biases['hidden']['weights'][i]

        for i, n in enumerate(self.output_layer.neurons):
            n.weights = weights_biases['output']['weights'][i]

        self.hidden_layer.bias = weights_biases['hidden']['bias']
        self.output_layer.bias = weights_biases['output']['bias']

    def write_weights(self):
        with open(f'Snakes/{names.get_full_name().replace(" ", "")}.txt', 'a') as past_nns:
            nn = ''
            for i in range(len(self.hidden_layer.neurons)):
                for weight in self.hidden_layer.neurons[i].weights:
                    nn += str(weight) + '|'
                nn += '+'
            nn += '\n' + str(self.hidden_layer.bias) + '\n\n\n'

            for i in range(len(self.output_layer.neurons)):
                for weight in self.output_layer.neurons[i].weights:
                    nn += str(weight) + '|'
                nn += '+'
            nn += '\n' + str(self.hidden_layer.bias) + '\n\n\n'

            past_nns.write(nn)

    def feed_forward(self, inputs):
        hidden_layer_output = self.hidden_layer.feed_forward(inputs)
        return self.output_layer.feed_forward(hidden_layer_output)

    def backprop(self, training_inputs, training_outputs):
        self.feed_forward(training_inputs)  # updates outputs of each neuron

        output_neuron_deltas = []
        for o in range(len(self.output_layer.neurons)):
            output_neuron_deltas.append(
                self.output_layer.neurons[o].calc_pd_error(training_outputs[o]))

        hidden_neuron_deltas = []
        for h in range(len(self.hidden_layer.neurons)):
            delta_error = 0
            for o in range(len(self.output_layer.neurons)):
                delta_error += output_neuron_deltas[o] * \
                    self.output_layer.neurons[o].weights[h]
            hidden_neuron_deltas.append(delta_error *
                                        self.hidden_layer.neurons[h].calc_pd_total())

        for o in range(len(self.output_layer.neurons)):
            for ho in range(len(self.output_layer.neurons[o].weights)):
                pd_error = output_neuron_deltas[o] * \
                    self.output_layer.neurons[o].inputs[ho]

                self.output_layer.neurons[o].weights[ho] -= self.learning_rate * \
                    pd_error

        for h in range(len(self.hidden_layer.neurons)):
            for ih in range(len(self.hidden_layer.neurons[h].weights)):
                pd_error = hidden_neuron_deltas[h] * \
                    self.hidden_layer.neurons[h].inputs[ih]
                self.hidden_layer.neurons[h].weights[ih] -= self.learning_rate * \
                    pd_error

    def calc_total_error(self, training_sets):
        total_error = 0
        for t in range(len(training_sets)):
            training_inputs, training_outputs = training_sets[t]
            self.feed_forward(training_inputs)
            for o in range(len(training_outputs)):
                total_error += self.output_layer.neurons[o].calc_error(
                    training_outputs[o])
        return total_error

    def train(self, training_sets):
        try:
            count = 1
            while True:
                for _ in range(5000):
                    ts = random.choice(training_sets)
                    self.backprop(ts[0], ts[1])
                print(
                    count, f'{100-round(self.calc_total_error(training_sets)/len(training_sets), 3)*100}% Correct')
                count += 1
        except KeyboardInterrupt:
            pass


class NeuronLayer:
    def __init__(self, num_neurons):
        self.bias = random.random()-0.5
        self.neurons = [Neuron(self.bias) for _ in range(num_neurons)]

    def feed_forward(self, inputs):
        return [neuron.calc_output(inputs) for neuron in self.neurons]


class Neuron:
    def __init__(self, bias):
        self.bias = bias
        self.weights = []

    def calc_output(self, inputs):
        self.inputs = inputs
        self.output = sigmoid(
            sum([_input * weight for _input, weight in zip(inputs, self.weights)]))
        return self.output

    def calc_error(self, target_output):
        return 0.5 * (target_output - self.output) ** 2

    def calc_pd_error(self, target_output):
        return -(target_output - self.output) * (self.output * (1 - self.output))

    def calc_pd_total(self):
        return self.output * (1 - self.output)


def read_file(snake_name):
    data_dict = {}
    with open(f'Snakes/{snake_name}.txt') as snake_brain:
        data = snake_brain.read()
        data = data.split('\n\n\n')[:2]

        hidden_neurons = data[0].split('\n')[0].split('+')[:-1]
        hidden_weights = [list(map(float, neuron.split('|')[:-1]))
                          for neuron in hidden_neurons]
        hidden_bias = float(data[0].split('\n')[1])
        data_dict['hidden'] = {'weights': hidden_weights, 'bias': hidden_bias}

        output_neurons = data[1].split('\n')[0].split('+')[:-1]
        output_weights = [list(map(float, neuron.split('|')[:-1]))
                          for neuron in output_neurons]
        output_bias = float(data[1].split('\n')[1])
        data_dict['output'] = {'weights': output_weights, 'bias': output_bias}
    return data_dict
    
if __name__ == '__main__':
    nn = NeuralNetwork(12, 24, 4, sets.sets, 0.05)
    try:
        input('Press enter to save the neural net, Ctrl+C to abort.\n>>>')
    except KeyboardInterrupt:
        print('Fine then. Be that way.')
    else:
        nn.write_weights()