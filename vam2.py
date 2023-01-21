from math import exp, radians

import numpy as np
import pandas as pd


def max_climb(df, seconds):
    """Find the max elevation gain for the given time period"""
    end_time, end_distance = df.loc[df['altitude'].diff(seconds).idxmax(), ['seconds', 'distance']].values
    start_time = end_time - seconds
    start_distance = df.loc[df['seconds'] == start_time, 'distance'].values

    p = ''
    p += f"{seconds / 60}min: {int(df['altitude'].diff(seconds).max())}m elevation gain over {int(end_distance - start_distance)}m\n"
    p += f"-- Starting at {int(end_time - seconds)}sec,  start_distance: {int(start_distance)}m\n"
    p += f"-- Ending at {int(end_time)}sec, end_distance: {int(end_distance)}m"
    return {'text': p, 'start_time': start_time, 'end_time': end_time}


def estimated_power(df: pd.DataFrame, rider_weight: float, bike_weight: float, wind_speed: float, wind_direction: int,
                    temperature: float, drag_coefficient: float, frontal_area: float, rolling_resistance: float,
                    efficiency_loss: float) -> pd.DataFrame:
    # Use the best Altitude data.
    if 'enhanced_altitude' in df.columns:
        df['slope'] = df.enhanced_altitude.diff() / df.distance.diff()
    else:
        df['slope'] = df.altitude.diff() / df.distance.diff()
    # Use the best speed data
    if "enhanced_speed" in df.columns:
        df['speed'] = df.enhanced_speed
    elif "speed" in df.columns:
        pass
    else:  # or calculate speed
        df['speed'] = df.distance.diff() / df.time.diff()

    # # create a seconds based col starting at 0
    # # This is used for to select the start and end time
    if 'seconds' not in df.columns:
        df['seconds'] = pd.to_datetime(df.index, unit='s', origin='unix').astype(int) // 10 ** 9
        df['seconds'] = df['seconds'] - df.seconds.min()

    df['vam'] = (df.altitude.diff() / df.seconds.diff()) * 3600

    # # Constants
    CdA = drag_coefficient * frontal_area
    altitude = (df.altitude.max() - df.altitude.min()) / 2
    # intermediate calculations
    df['air_density'] = ((101325 / (287.05 * 273.15)) * (273.15 / (temperature + 273.15)) *
                         exp((-101325 / (287.05 * 273.15)) * 9.8067 * (altitude / 101325)))
    df['effective_wind_speed'] = np.cos(radians(wind_direction)) * wind_speed
    # # Components of power, watts
    df['air_drag_watts'] = 0.5 * CdA * df.air_density * np.square(df.speed + df.effective_wind_speed) * df.speed
    df['climbing_watts'] = (bike_weight + rider_weight) * 9.8067 * np.sin(np.arctan(df.slope)) * df.speed
    df['rolling_watts'] = np.cos(np.arctan(df.slope)) * 9.8067 * (
            bike_weight + rider_weight) * rolling_resistance * df.speed
    df['acceleration_watts'] = (bike_weight + rider_weight) * (df.speed.diff() / df.seconds.diff()) * df.speed
    df['est_power_no_loss'] = df[['air_drag_watts', 'climbing_watts', 'rolling_watts', 'acceleration_watts']].sum(
        axis='columns')
    df['est_power'] = df['est_power_no_loss'] / (1 - efficiency_loss)
    df['est_power_no_acc'] = (df['est_power_no_loss'] - df['acceleration_watts']) / (1 - efficiency_loss)
    return df


def average_estimated_power(df: pd.DataFrame, rider_weight: float, bike_weight: float, wind_speed: float,
                            wind_direction: int,
                            temperature: float, drag_coefficient: float, frontal_area: float, rolling_resistance: float,
                            efficiency_loss: float) -> dict:
    """Find the average estimated power for the given time period
    We assume the df is filtered to the area of interest"""
    elpased_time = df.seconds.max() - df.seconds.min()
    distance = df.distance.max() - df.distance.min()
    accent = df.altitude.max() - df.altitude.min()
    slope = accent / distance
    speed = distance / elpased_time
    speed_kph = speed * 3.6
    avg_elevation = df.altitude.mean()
    CdA = drag_coefficient * frontal_area

    air_density = ((101325 / (287.05 * 273.15)) * (273.15 / (temperature + 273.15)) *
                   exp((-101325 / (287.05 * 273.15)) * 9.8067 * (avg_elevation / 101325)))
    effective_wind_speed = np.cos(radians(wind_direction)) * wind_speed
    # # Components of power, watts
    air_drag_watts = 0.5 * CdA * air_density * (speed + effective_wind_speed) ** 2 * speed
    climbing_watts = (bike_weight + rider_weight) * 9.8067 * np.sin(np.arctan(slope)) * speed
    rolling_watts = np.cos(np.arctan(slope)) * 9.8067 * (
            bike_weight + rider_weight) * rolling_resistance * speed
    est_power_no_loss = sum([air_drag_watts, climbing_watts, rolling_watts])
    est_power = est_power_no_loss / (1 - efficiency_loss)
    vam_mhr = (accent / elpased_time) * 3600

    return {'elpased_time': elpased_time, 'distance': distance, 'accent': accent, 'slope': slope, 'speed': speed,
            'speed_kph': speed_kph, 'avg_elevation': avg_elevation, 'frontal_area': frontal_area,
            'drag_coefficient': drag_coefficient, 'CdA': CdA, 'air_density': air_density,
            'effective_wind_speed': effective_wind_speed,
            'air_drag_watts': air_drag_watts, 'climbing_watts': climbing_watts, 'rolling_watts': rolling_watts,
            'vam_mhr': vam_mhr, 'est_power_no_loss': est_power_no_loss, 'est_power': est_power}
