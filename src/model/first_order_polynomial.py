from model import Model


class FirstOrderPolynomial(Model):

    def __init__(self, *fit_points):
        if len(fit_points) != 2:
            raise RuntimeError(f"FirstOrderPolynomial expects 2 fit points, but received {len(fit_points)}.")
        self.m, self.t = self._get_parameters(*fit_points)

    def _get_parameters(self, *fit_points):
        x0, y0 = fit_points[0]
        x1, y1 = fit_points[1]
        m = (y1 - y0) / (x1 - x0)
        t = y0 - m * x0
        return (m, t)
    
    def parameters(self):
        return {
            "m": self.m,
            "t": self.t,
        }

    def model(self):
        return lambda x: self.m * x + self.t
    
    def reset_model(self, params):
        if 'm' not in params:
            raise RuntimeError(f"FirstOrderPolynomial expects m parameter.")
        if 't' not in params:
            raise RuntimeError(f"FirstOrderPolynomial expects t parameter.")
        self.m = params['m']
        self.t = params['t']
    
    def offset_parameter(self) -> str:
        return 't'
    