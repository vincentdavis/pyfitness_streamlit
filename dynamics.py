from math import exp, pi, radians

import numpy as np
import pandas as pd
from scipy.optimize import fsolve


def estimate_frontal_area(kg, height, tt=False):
    """
    Estimate frontal area based on rider weight and height.
    """
    h = height / 100  # to get meters

    if tt:
        a = 0.006447910106426458
    else:
        a = 0.006894270128795239

    r = a * kg / h
    fa = h * pi * r**2
    return fa


class Dynamics:
    """
    Calculate missing value.
    """

    def __init__(
        self,
        # speed: float = 5,
        kg: float = 60,
        power: float = 250,
        bike_kg: float = 10,
        height: float = 172,
        frontal_area: float = 0.423,
        slope: float = 0,
        altitude: float = 0,
        temperature: float = 20,
        wind_speed: float = 0,
        wind_direction: float = 0,
        drag_coefficient: float = 0.8,
        rolling_resistance: float = 0.005,
        drivetrain_loss: float = 0.04,
        drafting_effect: float = 0.0,  # no drafting
    ):
        # self.solve_for = speed
        self.kg = kg
        self.power = power
        self.bike_kg = bike_kg
        self.height = height
        self.frontal_area = frontal_area
        self.slope = slope / 100
        self.altitude = altitude
        self.temperature = temperature
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.drag_coefficient = drag_coefficient
        self.rolling_resistance = rolling_resistance
        self.drivetrain_loss = drivetrain_loss / 100
        self.drafting_effect = drafting_effect / 100
        self.total_kg = self.kg + self.bike_kg
        self.wkg = self.power / self.kg
        self.total_wkg = self.power / self.total_kg
        self.CdA = self.drag_coefficient * self.frontal_area
        self.air_density = (
            (101325 / (287.05 * 273.15))
            * (273.15 / (self.temperature + 273.15))
            * exp((-101325 / (287.05 * 273.15)) * 9.8067 * (self.altitude / 101325))
        )

    def calc_speed(self, speed) -> float:
        """
        Calculate speed for a given rider
        """
        effective_wind_speed = np.cos(radians(self.wind_direction)) * self.wind_speed
        drivetrain_loss_watts = self.power * self.drivetrain_loss
        rolling_force = np.cos(np.arctan(self.slope)) * 9.8067 * self.total_kg * self.rolling_resistance
        climbing_force = self.total_kg * 9.8067 * np.sin(np.arctan(self.slope))
        climbing_watts = climbing_force * speed
        rolling_watts = rolling_force * speed
        air_drag_force = 0.5 * self.CdA * self.air_density * np.square(speed + effective_wind_speed)
        air_drag_watts = air_drag_force * speed
        total_watts = climbing_watts + rolling_watts + air_drag_watts + drivetrain_loss_watts
        self.climbing_watts = climbing_watts
        self.rolling_watts = rolling_watts
        self.air_drag_watts = air_drag_watts
        self.drafting_watts = air_drag_watts * (1 - self.drafting_effect)
        self.drivetrain_loss_watts = drivetrain_loss_watts
        self.total_watts = total_watts
        balance = self.power - total_watts

        return balance

    def race_course(
        self,
        seg_1: float = 0,
        seg_1_slope: float = 0,
        seg_2: float = 0,
        seg_2_slope: float = 0,
        seg_3: float = 0,
        seg_3_slope: float = 0,
        seg_4: float = 0,
        seg_4_slope: float = 0,
        seg_5: float = 0,
        seg_5_slope: float = 0,
    ) -> pd.DataFrame:
        """
        - Define course Each segment can be 0km in length
            1. Segment 1 [km]
            2. Segment 1 slope [%] (negative to decend)
            3. segment 2 [km]
            4. segment 2 slope [%] (negative to decend)
            5. segment 3 [km]
            6. segment 3 slope [%] (negative to decend)
            7. segment 4 [km]
            8. segment 4 slope [%] (negative to decend)
            9. segment 5 [km]
            10. segment 5 slope [%] (negative to decend)
        - If you set the drafting effect > 0, this is like assuming the rider is drafting another rider.
        - This is a static model, ignores energy to change speed
        - The speed is calculated every 1 meter.
        - Calculated speed is used to calculate the time to travel the next meter.
        """
        distance = seg_1 + seg_2 + seg_3 + seg_4 + seg_5
        print(f"Total distance: {distance}km")
        course = []
        start = 0
        for i, seg in enumerate(
            (
                (seg_1, seg_1_slope),
                (seg_2, seg_2_slope),
                (seg_3, seg_3_slope),
                (seg_4, seg_4_slope),
                (seg_5, seg_5_slope),
            )
        ):
            end = start + int(seg[0] * 1000)
            n = i + 1
            point = [(f"seg_{n}", p / 1000, seg[1]) for p in range(start, end)]
            print(1, i, seg, start, end)
            start = end
            # print(2, i, seg, start, end)
            course += point

        def _calc_speed_with_slope(slope):
            self.slope = slope / 100
            return fsolve(self.calc_speed, 5)[0] * 3.6

        df = pd.DataFrame(course, columns=["segment", "distance", "slope"])
        df["speed"] = df.slope.apply(_calc_speed_with_slope)
        df["segment_time"] = df.speed / 3.6
        df["elapsed_time"] = df.segment_time.cumsum()
        return df


# d = Dynamics()
# df = d.race_course(10, 0, 10, 10, 10, -10, 10, 0, 10, 5)
