from math import exp, pi, radians

import numpy as np
import pandas as pd
from scipy.optimize import fsolve

LONG_NAMES = {
    "power": "Power output [watts]",
    "kg": "Rider weight [kg]",
    "ftp_wkg": "Watts per kg at FTP, rider only [w/kg]",
    "total_ftp_wkg": "Watts per kg at FTP, total [w/kg]",
    "bkg": "Bike weight [kg]",
    "total_kg": "Total weight [kg]",
    "height": "Rider height [cm]",
    "frontal_area": "Rider Frontal srea [m^3]",
    "cd": "Air Drag Coefficent [Cd]",
    "cda": "Coefficient of Drag (CdA [m^2]",
    "air_density": "Air density [kg/m^3]",
    "slope": "Slope [%]",
    "altitude": "Starting altitude [m]",
    "temperature": "Temperature [c]",
    "wind_speed": "Wind speed [kph]",
    "wind_direction": "Wind Direction 0=headwind [deg]",
    "effective_wind_speed": "Effective wind speed [m/s]",
    "crr": "Coefficient of Rolling Resistance",
    "crr_force": "Rolling Resistance force [N]",
    "crr_watts": "Rolling Resistance power [watts]",
    "climbing_force": "Climbing force [N]",
    "climbing_watts": "Climbing power [watts]",
    "air_drag_force": "Air Drag force [N]",
    "air_drag_watts": "Air Drag power [watts]",
    "total_watts": "Total power used [watts]",
    "dt_loss": "Drivetrain, other Efficiency Losses [%]",
    "dt_watts": "Drivetrain power loss [watts]",
    "drafting_effect": "Drafting effect [%]",
    "drafting_watts": "Drafting power [watts]",
    "surface": "surface_drag (rr X surface) [%]",
}


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


class speed_result:
    pass


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
        wind_speed: float = 10,
        wind_direction: float = 0,
        cd: float = 0.8,
        crr: float = 0.005,
        dt_loss: float = 0.04,
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
        self.cd = cd
        self.crr = crr
        self.dt_loss = dt_loss / 100
        self.drafting_effect = drafting_effect / 100
        self.total_kg = self.kg + self.bike_kg
        self.wkg = self.power / self.kg
        self.total_wkg = self.power / self.total_kg
        self.cdA = self.cd * self.frontal_area
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
        drivetrain_loss_watts = self.power * self.dt_loss
        rolling_force = np.cos(np.arctan(self.slope)) * 9.8067 * self.total_kg * self.crr
        rolling_watts = rolling_force * speed
        climbing_force = self.total_kg * 9.8067 * np.sin(np.arctan(self.slope))
        climbing_watts = climbing_force * speed

        air_drag_force = 0.5 * self.cdA * self.air_density * np.square(speed + effective_wind_speed)
        air_drag_watts = air_drag_force * speed
        total_watts = climbing_watts + rolling_watts + air_drag_watts + drivetrain_loss_watts
        self.climbing_watts = climbing_watts
        self.rolling_watts = rolling_watts
        self.air_drag_watts = air_drag_watts
        self.drafting_watts = air_drag_watts * (1 - self.drafting_effect)
        self.dt_loss_watts = drivetrain_loss_watts
        self.total_watts = total_watts
        balance = self.power - total_watts

        return balance

    def calc_speed_exact(self) -> float:
        """
        power - power * drivetrain_loss - (climbing_force + rolling_force)*speed + air_drag_force*speed = 0
        z^3 + az^2 + bz + c = 0
        Defining
        P = (3b - a^2)/3
        Q = (9ab - 27c + 2a^3)/27

        a = 2 * effective_wind_speed
        b = (climbing_force+ rolling_force)/(0.5 * self.CdA * self.air_density) + effective_wind_speed ** 2
        c = drivetrain_loss_watts/(0.5 * self.CdA * self.air_density)
        """

        effective_wind_speed = np.cos(radians(self.wind_direction)) * self.wind_speed
        rolling_force = np.cos(np.arctan(self.slope)) * 9.8067 * self.total_kg * self.crr
        climbing_force = self.total_kg * 9.8067 * np.sin(np.arctan(self.slope))
        drivetrain_loss_watts = self.power * self.dt_loss

        a = 2 * effective_wind_speed
        # print(f"a: {a}")
        b = (climbing_force + rolling_force) / (0.5 * self.cdA * self.air_density) + effective_wind_speed**2
        # print(f"b: {b}")
        c = (drivetrain_loss_watts - self.power) / (0.5 * self.cdA * self.air_density)
        # print(f"c: {c}")
        P = (3 * b - a**2) / 3
        # print(f"P: {P}")
        Q = (9 * a * b - 27 * c - 2 * a**3) / 27
        # print(f"Q: {Q}")
        # print(f"w^3 +: {(0.5 * Q + (0.25 * (Q ** 2) + (P ** 3) / 27))}")
        # print(f"w^3 -: {(0.5 * Q - (0.25 * (Q ** 2) + (P ** 3) / 27))}")
        s1 = (0.5 * Q + (0.25 * (Q**2) + (P**3) / 27) ** 0.5) ** (1 / 3)
        # s2 = (0.5 * Q - (0.25 * (Q**2) + (P**3) / 27) ** 0.5) ** (1 / 3)
        return s1

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


def calc_speed_exact(
    kg: float,
    power: float,
    bike_kg: float,
    height: float,
    frontal_area: float = 0.423,
    slope: float = 0,
    altitude: float = 0,
    temperature: float = 20,
    wind_speed: float = 0,
    wind_direction: float = 0,
    drag_coefficient: float = 0.8,
    rolling_resistance: float = 0.005,
    drivetrain_loss: float = 0.04,
    drafting_effect: float = 15,
) -> dict:
    """
    power - power * drivetrain_loss - (climbing_force + rolling_force)*speed + air_drag_force*speed = 0
    z^3 + az^2 + bz + c = 0
    Defining
    P = (3b - a^2)/3
    Q = (9ab - 27c + 2a^3)/27

    a = 2 * effective_wind_speed
    b = (climbing_force+ rolling_force)/(0.5 * self.CdA * self.air_density) + effective_wind_speed ** 2
    c = drivetrain_loss_watts/(0.5 * self.CdA * self.air_density)
    """
    slope = slope / 100
    drafting_effect = drafting_effect / 100
    total_kg = kg + bike_kg
    wkg = power / kg
    total_wkg = power / total_kg
    CdA = drag_coefficient * frontal_area
    air_density = (
        (101325 / (287.05 * 273.15))
        * (273.15 / (temperature + 273.15))
        * exp((-101325 / (287.05 * 273.15)) * 9.8067 * (altitude / 101325))
    )
    drivetrain_loss = drivetrain_loss / 100
    effective_wind_speed = np.cos(radians(wind_direction)) * wind_speed

    rolling_force = np.cos(np.arctan(slope)) * 9.8067 * total_kg * rolling_resistance
    climbing_force = total_kg * 9.8067 * np.sin(np.arctan(slope))
    drivetrain_loss_watts = power * drivetrain_loss

    a = 2 * effective_wind_speed
    # print(f"a: {a}")
    b = (climbing_force + rolling_force) / (0.5 * CdA * air_density) + effective_wind_speed**2
    # print(f"b: {b}")
    c = (drivetrain_loss_watts - power) / (0.5 * CdA * air_density)
    # print(f"c: {c}")
    P = (3 * b - a**2) / 3
    # print(f"P: {P}")
    Q = (9 * a * b - 27 * c - 2 * a**3) / 27
    # print(f"Q: {Q}")
    # print(f"w^3 +: {(0.5 * Q + (0.25 * (Q ** 2) + (P ** 3) / 27))}")
    # print(f"w^3 -: {(0.5 * Q - (0.25 * (Q ** 2) + (P ** 3) / 27))}")
    s1 = (0.5 * Q + (0.25 * (Q**2) + (P**3) / 27) ** 0.5) ** (1 / 3)
    # s2 = (0.5 * Q - (0.25 * (Q**2) + (P**3) / 27) ** 0.5) ** (1 / 3)
    return s1


if __name__ == "__main__":
    d = Dynamics()
    # df = d.race_course(10, 0, 10, 10, 10, -10, 10, 0, 10, 5)
    s1 = d.calc_speed_exact()
    print(s1)
