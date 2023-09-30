from abc import ABC

class Model(ABC):
    
    def __init__(self, *fit_points):
        pass

    def _get_parameters(self, *fit_points):
        pass

    def parameters(self):
        pass

    def model(self):
        pass

    def reset_model(self, *params):
        pass

    def offset_parameter(self) -> str:
        pass
