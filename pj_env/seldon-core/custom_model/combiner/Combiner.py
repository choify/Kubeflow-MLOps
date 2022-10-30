from seldon_core.user_model import SeldonComponent
import numpy as np


class Combiner(SeldonComponent):
    def __init__(self):
        super(Combiner, self).__init__()

    def aggregate(self, Xs, features_names=None):
        x = np.stack(Xs, axis=0)
        return np.mean(x, axis=0)
