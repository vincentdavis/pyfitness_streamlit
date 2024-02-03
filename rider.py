from dataclasses import dataclass

import numpy as np
from scipy.optimize import curve_fit


def interpolate_y(points, x):
    """
    Interpolates the y value for a given x in a set of (x, y) points.

    Args:
        points: A list of (x, y) tuples.
        x: The x value for which to interpolate the y value.

    Returns:
        The interpolated y value, or None if x is outside the range of the data points.
    """

    # Sort the points by x-value
    points.sort(key=lambda p: p[0])

    # Find the two points between which x lies
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        if x1 <= x <= x2:
            # Perform linear interpolation
            slope = (y2 - y1) / (x2 - x1)
            y = y1 + slope * (x - x1)
            return y
        elif x < points[0]:  # less than 1 second
            return points[0][1]  # return the first value
        elif x > points[-1]:  # x is outside the range of the data points
            return points[-1][1]  # return the last value which should be 2600 sec, ftp
        else:
            raise ValueError("The value of x has a problem")


@dataclass
class Rider:
    name: str
    kg: float | int = 70
    height: float | int = 175
    power_curve: tuple[tuple] = (
        (1, 1000),
        (5, 900),
        (10, 750),
        (30, 500),
        (60, 400),
        (120, 275),
        (300, 250),
        (600, 250),
        (1200, 250),
        (2600, 250),
    )
    power: float | int = 250
    frontal_area: float = 0.423
    bike_kg: float | int = 10
    rolling_resistance: float = 0.005
    drivetrain_loss: float = 0.04
    drafting_effect: float = 0.15

    def __post_init__(self):
        self.ftp = self.w2600
        self.total_kg = self.kg + self.bike_kg
        self.ftp_wkg = self.ftp / self.kg
        self.total_ftp_wkg = self.ftp / self.total_kg
        self.power_curve_area = self.power_area()

    def power_area_calc(self):
        dx = np.diff([x[0] for x in self.power_profile])  # Calculate differences between x values
        return np.sum(y[:-1] * dx + 0.5 * dx * (y[1:] - y[:-1]))  # Calculate the area under the curve


if __name__ == "__main__":
    x = np.array([1, 60, 2600])
    y = np.array([1000, 500, 250])
    from scipy.optimize import curve_fit

    # Define the function to fit
    def func(x, a, b, c):
        return a + b * x + c / x**0.5

    # Fit the function using curve_fit
    popt, pcov = curve_fit(func, x, y)

    # Print the fitted parameters
    print(f"Fitted parameters: a = {popt[0]}, b = {popt[1]}, c = {popt[2]}")

    # Evaluate the fitted function at specific points
    x_new = np.linspace(x.min(), x.max(), 100)
    y_new = func(x_new, *popt)

    # Plot the data and the fitted function
    import matplotlib.pyplot as plt

    plt.plot(x, y, "o", label="Data points")
    plt.plot(x_new, y_new, "-", label="Fitted function")
    plt.legend()
    plt.show()
