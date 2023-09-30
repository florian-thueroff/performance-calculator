from model import Model


class SecondOrderPolynomial(Model):

    def __init__(self, *fit_points):
        if len(fit_points) != 3:
            raise RuntimeError(f"SecondOrderPolynomial expects 3 fit points, but received {len(fit_points)}.")
        self.a, self.b, self.c = self._get_parameters(*fit_points)

    def _get_parameters(self, *fit_points):
        x0, y0 = fit_points[0]
        x1, y1 = fit_points[1]
        x2, y2 = fit_points[2]
        a = (x0*(y2-y1)+x1*(y0-y2)+x2*(y1-y0))/((x0-x1)*(x0-x2)*(x1-x2))
        b = (x0**2*(y1-y2)+x1**2*(y2-y0)+x2**2*(y0-y1))/((x0-x1)*(x0-x2)*(x1-x2))
        c = (x1*(x0**2*y2-x2**2*y0)+x1**2*(x2*y0-x0*y2)+x0*x2*y1*(x2-x0))/((x0-x1)*(x0-x2)*(x1-x2))
        return (a, b, c)
    
    def parameters(self):
        return {
            "a": self.a,
            "b": self.b,
            "c": self.c,
        }

    def model(self):
        return lambda x: self.a * x**2 + self.b * x + self.c
    
    def reset_model(self, params):
        if 'a' not in params:
            raise RuntimeError(f"SecondOrderPolynomial expects a parameter.")
        if 'b' not in params:
            raise RuntimeError(f"SecondOrderPolynomial expects b parameter.")
        if 'c' not in params:
            raise RuntimeError(f"SecondOrderPolynomial expects c parameter.")
        self.a = params['a']
        self.b = params['b']
        self.c = params['c']
    
    def offset_parameter(self) -> str:
        return 'c'
    