from control.buildcavity import Cavity_2Pi_3
SPEED_OF_LIGHT = 299792458
class Cavity_Optimizer:
    def __init__(self):
        self.target_frequency = 2998.8  # MHz, target frequency for the cavity
        pass
    def wave_length(self):
        return SPEED_OF_LIGHT / (self.target_frequency * 1e6)  # Convert MHz to Hz
    def cavity_2pi_3_beta_1(self):
        """
        Creates a 2Pi/3 cavity with beta=1.
        """
        