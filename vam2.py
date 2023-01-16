from math import exp, radians

import numpy as np
import pandas as pd

def max_climb(df, seconds):
    """Find the max elevation gain for the given time period"""
    end_time, end_distance= df.loc[df['altitude'].diff(seconds).idxmax(), ['seconds', 'distance']].values
    start_time = end_time - seconds
    start_distance = df.loc[df['seconds']==start_time, 'distance'].values

    p = ''
    p += f"{seconds / 60}min: {int(df['altitude'].diff(seconds).max())}m elevation gain over {int(end_distance - start_distance)}m\n"
    p += f"-- Starting at {int(end_time-seconds)}sec,  start_distance: {int(start_distance)}m\n"
    p += f"-- Ending at {int(end_time)}sec, end_distance: {int(end_distance)}m"
    return {'text': p, 'start_time': start_time, 'end_time': end_time}


def estimated_power(df: pd.DataFrame, start_time: int, end_time: int, rider_weight: float, bike_weight: float,
                    wind_speed: float, wind_direction: int, temperature: float, drag_coefficient: float,
                    frontal_area: float, rolling_resistance: float, roll: int) -> pd.DataFrame:
    # Use the best Alititude data.
    if 'enhanced_altitude' in df.columns:
        df['slope'] = df.enhanced_altitude.diff() / df.distance.diff()
    else:
        df['slope'] = df.altitude.diff() / df.distance.diff()
    # Use the best speed data
    if "enhanced_speed" in df.columns:
        df['speed'] = df.enhanced_speed
    elif "speed" in df.columns:
        pass
    else: # or calculate speed
        df['speed'] = df.distance.diff() / df.time.diff()

    # create a second based col starting at 0
    # This is used for to select the start and end time
    if 'seconds' not in df.columns:
        df['seconds'] = pd.to_datetime(df.index, unit='s', origin='unix').astype(int) // 10 ** 9
        df['seconds'] = df['seconds'] - df.seconds.min()

    df['vam'] = (df.altitude.diff() / df.seconds.diff()) * 3600
    df['vam_smoothed'] = df['vam'].rolling(roll).mean()

    # Constants
    CdA = drag_coefficient * frontal_area
    altitude = (df.altitude.max() - df.altitude.min()) / 2
    # intermediate calculations
    df['air_density'] = ((101325 / (287.05 * 273.15)) * (273.15 / (temperature + 273.15)) *
                         exp((-101325 / (287.05 * 273.15)) * 9.8067 * (altitude / 1013.25)))
    df['effective_wind_speed'] = np.cos(radians(wind_direction)) * wind_speed
    # Components of power, watts
    df['air_drag_watts'] = (0.5 * CdA * df.air_density * (df.speed / (3.6 + df.effective_wind_speed)) ** 2) * df.speed
    df['climbing_watts'] = (bike_weight + rider_weight * 9.0867 * np.sin(np.arctan(df.slope))) * df.speed
    df['rolling_watts'] = (np.cos(np.arctan(df.slope)) * 9.8067 * (
                bike_weight + rider_weight) * rolling_resistance) * df.speed
    df['acceleration_watts'] = (bike_weight + rider_weight) * (df.speed.diff() / df.seconds.diff()) * df.speed
    df['est_power'] = (df[['air_drag_watts', 'climbing_watts', 'rolling_watts', 'acceleration_watts']].sum(axis='columns'))
    return df

