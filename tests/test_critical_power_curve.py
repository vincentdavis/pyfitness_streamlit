import numpy as np
import pandas as pd

from ramp_test import _calculate_ramp_power


def test_critical_power_calulation():
    df = pd.read_csv("Critical_Power_Curve.csv")
    df = _calculate_ramp_power(df)
    df["ramp_power"].astype(float)
    df["result_1"].astype(float)
    assert np.allclose(df["ramp_power"], df["result_1"], equal_nan=True)


if __name__ == "__main__":
    test_critical_power_calulation()
