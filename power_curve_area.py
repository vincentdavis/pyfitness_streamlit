import numpy as np


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


def power_area_calc(points):
    y = np.array([y[1] for y in points])  # Extract the y values'
    dx = np.diff([x[0] for x in points])  # Calculate differences between x values
    print(y)
    return np.sum(y[:-1] * dx + 0.5 * dx * (y[1:] - y[:-1]))  # Calculate the area under the curve
