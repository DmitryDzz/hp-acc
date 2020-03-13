from math import sqrt


class AccFigure:
    def __init__(self, alpha):
        self.alpha = alpha
        self.rate = 0.0

        self.t_values = []
        self.x_values = []
        self.y_values = []
        self.z_values = []
        self.m_values = []

        self._start_t = None
        self._prev_x = None
        self._prev_y = None
        self._prev_z = None
        self._iterations = 0

    @staticmethod
    def _lerp(v0, v1, alpha):
        return v0 + alpha * (v1 - v0)

    def feed_acc(self, t, x, y, z):
        if self._start_t is None:
            self._start_t = t
        t = t - self._start_t
        self.rate = 0 if t < 0.001 else self._iterations / t
        self._iterations += 1

        x = x if self._prev_x is None else AccFigure._lerp(self._prev_x, x, self.alpha)
        y = y if self._prev_y is None else AccFigure._lerp(self._prev_y, y, self.alpha)
        z = z if self._prev_z is None else AccFigure._lerp(self._prev_z, z, self.alpha)
        self._prev_x = x
        self._prev_y = y
        self._prev_z = z
        m = sqrt(x * x + y * y + z * z)

        self.t_values.append(t)
        self.x_values.append(x)
        self.y_values.append(y)
        self.z_values.append(z)
        self.m_values.append(m)
