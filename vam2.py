from math import exp, cos, sin, radians, atan

import pandas as pd
import numpy as np

def estimated_power(df: pd.DataFrame, start_time: int, end_time: int, rider_weight: float, bike_weight: float,
                    wind_speed: float, wind_direction: int, temperature: float, drag_coefficient: float,
                    frontal_area: float, rolling_resistance: float, roll: int) -> pd.DataFrame:

    CdA = drag_coefficient * frontal_area
    altitude = (df.altitude.max() - df.altitude.min()) / 2
    if 'enhanced_altitude' in df.columns:
        df['slope'] = df.enhanced_altitude.diff() / df.distance.diff()
    else:
        df['slope'] = df.altitude.diff() / df.distance.diff()
    if "enhanced_speed" in df.columns:
        df['speed'] = df.enhanced_speed
    elif "speed" in df.columns:
        pass
    else:
        df['speed'] = df.distance.diff() / df.time.diff()
    if 'seconds' not in df.columns :
        df['seconds'] = pd.to_datetime(df.index, unit='s', origin='unix').astype(int) // 10 ** 9
        df['seconds'] = df['seconds'] - df.seconds.min()
    df['vam'] = (df.altitude.diff() / df.seconds.diff()) * 3600
    df['roll_vam'] = df['vam'].rolling(roll).mean()
    df['climb_force'] = bike_weight + rider_weight * 9.0867 * np.sin(np.arctan(df.slope))
    df['air_density'] = ((101325 / (287.05 * 273.15)) * (273.15 / (temperature + 273.15)) *
                                  exp((-101325 / (287.05 * 273.15)) * 9.8067 * (altitude / 1013.25)))
    df['effective_wind_speed'] = np.cos(radians(wind_direction)) * wind_speed
    df['air_drag'] = (0.5 * CdA * df.air_density * (df.speed / (3.6 + df.effective_wind_speed)) ** 2) * df.speed
    df['climbing_force'] = (bike_weight + rider_weight * 9.0867 * np.sin(np.arctan(df.slope))) * df.speed
    df['rolling_force'] = (np.cos(np.arctan(df.slope)) * 9.8067 * (bike_weight + rider_weight) * rolling_resistance) * df.speed
    df['vam_power'] = (df[['air_drag', 'climbing_force', 'rolling_force']].sum(axis='columns'))
    return df

