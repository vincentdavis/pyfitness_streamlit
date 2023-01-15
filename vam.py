from math import exp, cos, sin, radians, atan

import pandas as pd


class FitVam(object):
    """
    Referances:
    https://www.researchgate.net/publication/23986705_New_Method_to_Estimate_the_Cycling_Frontal_Area
    https://link.springer.com/content/pdf/10.1007/s12283-017-0234-1.pdf?pdf=button%20sticky
    https://core.ac.uk/download/pdf/29823669.pdf
    https://www.sciencedirect.com/science/article/pii/S0165232X2100063X
    User set parameters for the fit:
    - dataframe: with start and end time
    The following as a dictionary:
    - bike_weight in kg
    - wind speed in m/s: Default 0
    - wind direction in degrees: Default 0
    - temperature in degrees celcius: Default 20

    Calculated parameters from data points:
    - AirDensity
    - effective_wind_speed

    Estimate the following parameters:
    - rider_weight in kg
    - frontal_area in m^2
    - drag_coefficient"""

    def __init__(self, df: pd.DataFrame, start_time: int, end_time: int, rider_weight: float, bike_weight: float,
                 wind_speed: float, wind_direction: float, temperature: int, drag_coefficient: float,
                 frontal_area: float, rolling_resistance: float):
        self.df = df
        self.start_time = start_time
        self.end_time = end_time
        self.rider_weight = rider_weight
        self.bike_weight = bike_weight
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.temperature = temperature
        self.drag_coefficient = drag_coefficient
        self.frontal_area = frontal_area
        self.rolling_resistance = rolling_resistance
        self.CdA = self.drag_coefficient * self.frontal_area
        self.altitude = (self.df.altitude.max() - self.df.altitude.min()) / 2
        # self.air_density = self.air_density()
        # self.effective_wind_speed = self.effective_wind_speed()
        self.rider_weight = rider_weight
        if 'enhanced_altitude' in df.columns:
            df['slope'] = df.enhanced_altitude.diff() / df.enhanced_altitude.diff()
        else:
            df['slope'] = df.altitude.diff() / df.distance.diff()
        if "enhanced_speed" in df.columns:
            df['speed'] = df.enhanced_speed
        elif "speed" in df.columns:
            pass
        else:
            df['speed'] = df.distance.diff() / df.time.diff()
        # df['seconds'] = pd.to_datetime(df.index, unit='s', origin='unix').astype(int) // 10 ** 9
        # df['seconds'] = df['seconds']
        df['vam'] = (df.altitude.diff() / df.seconds.diff()) * 3600
        df['rvam'] = df['vam'].rolling(5).mean()

    def climbing_force(self):
        self.df['climb_force'] = self.bike_weight + self.rider_weight * 9.0867 * sin(atan(self.df.slope))

    def calc_forces_on_rider(self):
        """Forces on rider times speed"""
        # air_density
        self.df['air_density'] = ((101325 / (287.05 * 273.15)) * (273.15 / (self.temperature + 273.15)) *
                                  exp(-101325 / (287.05 * 273.15) * 9.8067 * (self.altitude / 1013.25)))
        # effective_wind_speed
        self.df['effective_wind_speed'] = cos(radians(self.wind_direction)) * self.wind_speed
        # air_drag
        # self.df['air_drag'] = 0.5 * self.CdA * self.df.air_density * (self.df.speed / (3.6 + self.df.effective_wind_speed)) ^ 2
        self.df['air_drag'] = 0.5 * self.CdA * self.df.air_density # * (self.df.speed / (3.6 + self.df.effective_wind_speed)) ^ 2

        # climbing_force
        self.df['climb_force'] = self.bike_weight + self.rider_weight * 9.0867 * sin(atan(self.df.slope))
        self.df['vpower'] = (self.df[['air_drag', 'climbing_force']].sum(axis='columns')) * self.df.speed

