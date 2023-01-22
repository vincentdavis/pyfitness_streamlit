from math import exp, radians

import numpy as np
import pandas as pd


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
