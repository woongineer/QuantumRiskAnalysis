import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import Sampler
from qiskit_algorithms import EstimationProblem, AmplitudeEstimation


class BernoulliA(QuantumCircuit):
    """A circuit representing the Bernoulli A operator."""

    def __init__(self, probability):
        super().__init__(1)  # circuit on 1 qubit

        theta_p = 2 * np.arcsin(np.sqrt(probability))
        self.ry(theta_p, 0)


class BernoulliQ(QuantumCircuit):
    """A circuit representing the Bernoulli Q operator."""

    def __init__(self, probability):
        super().__init__(1)  # circuit on 1 qubit

        self._theta_p = 2 * np.arcsin(np.sqrt(probability))
        self.ry(2 * self._theta_p, 0)

    def power(self, k):
        # implement the efficient power of Q
        q_k = QuantumCircuit(1)
        q_k.ry(2 * k * self._theta_p, 0)
        return q_k

if __name__ == '__main__':
    p = 0.34
    A = BernoulliA(p)
    Q = BernoulliQ(p)

    problem = EstimationProblem(state_preparation=A,
                                grover_operator=Q,
                                objective_qubits=[0])

    ae = AmplitudeEstimation(num_eval_qubits=4, sampler=Sampler())

    trial = ae.construct_circuit(problem)

    trial.decompose(reps=1)