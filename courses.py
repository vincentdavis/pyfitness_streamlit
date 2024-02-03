from dataclasses import dataclass

import numpy as np
import pandas as pd

from dynamics import Dynamics
from rider import Rider


@dataclass
class SpeedResult:
    pass


class RaceCourse:
    """All inputs are assumed to be in SI units.
    Meter, Watts, Celsius, m/s, kg/m^3, kg, m^2
    """

    riders = []

    def __init__(self, course_type: str, segments: list[dict] = None, fit_file=None):
        self.course_type = course_type
        self.segments = segments
        self.fit_file = fit_file
        try:
            assert not (self.segments and self.fit_file)
            assert self.segments or self.fit_file
        except AssertionError as e:
            raise e
        match self.course_type:
            case "SEGMENTS":
                self.course = self._segments_course()
            case "FIT":
                self.course = self._fit_course()

    def _segments_course(self):
        course_points = []
        for seg in self.segments:
            course_points += [seg] * seg["length"]
        df = pd.DataFrame(course_points)
        df["meter"] = 1
        df["distance"] = df["meter"].cumsum()
        self.course = df
        return df

    def _fit_course(self):
        return self.fit_file

    def add_riders(self, riders: list[Rider]):
        """Add the rider to the rider list and adds the rider name to the course dataframe"""
        for rider in riders:
            assert rider.name not in self.course.columns
            self.course[[f"{rider.name} [kg]"]] = rider.kg
            self.course[[f"{rider.name} [cm]"]] = rider.height
            self.course[[f"{rider.name} [ftp]"]] = rider.ftp
            self.course[[f"{rider.name} [power]"]] = rider.power
            self.course[[f"{rider.name} [frontal_area]"]] = rider.frontal_area
            self.course[[f"{rider.name} [bike_kg]"]] = rider.bike_kg
            self.course[[f"{rider.name} [rolling_resistance]"]] = rider.rolling_resistance
            self.course[[f"{rider.name} [drivetrain_loss]"]] = rider.drivetrain_loss
            self.course[[f"{rider.name} [drafting_effect]"]] = rider.drafting_effect
            self.course[[f"{rider.name} [speed]"]] = np.nan
            self.riders.append(rider)

    def race(self):
        rider_speed = []
        for rider in self.riders:
            d = Dynamics()

        self.course[[f"{rider.name}_speed" for rider in self.riders]] = self.course[rider.name].apply(rider.speed)


if __name__ == "__main__":
    c = RaceCourse(
        course_type="SEGMENTS",
        segments=[
            {
                "name": "Start",
                "length": 10,
                "slope": 0,
                "wind": 0,
                "wind_direction": 0,
                "surface_drag": 1,
                "drafting": True,
            },
            {
                "name": "Dirt Climb",
                "length": 5,
                "slope": 10,
                "wind": 10,
                "wind_direction": 0,
                "surface_drag": 10,
                "drafting": False,
            },
            {
                "name": "Cross_wind",
                "length": 10,
                "slope": -5,
                "wind": 20,
                "wind_direction": 90,
                "surface_drag": 10,
                "drafting": True,
            },
        ],
    )

if __name__ == "__main__":
    c = RaceCourse(course_type="segments")
    df = c._segments_course()
    rider_1 = Rider(name="Rider_1", power=250)
    rider_2 = Rider(name="Rider_2", power=300)
    c.add_riders([rider_1, rider_2])
