from epics.epic019_networked_trust.convergence import (
    NetworkConvergence
)


checker = NetworkConvergence()


valid_network = {
    "node-A": "state123",
    "node-B": "state123",
    "node-C": "state123"
}


split_network = {
    "node-A": "state123",
    "node-B": "state999",
    "node-C": "state123"
}


print(
    checker.verify(
        valid_network
    )["converged"]
)


print(
    checker.verify(
        split_network
    )["converged"]
)
