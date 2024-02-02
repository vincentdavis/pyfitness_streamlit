from random import randint


class Rider:
    def __init__(
        self,
        name: str = f"Rider_{randint(0, 1000)}",
        kg: float | int = 70,
        height: float | int = 175,
        ftp: float | int = 250,
        power: float | int = 250,
        frontal_area: float = 0.423,
        bike_kg: float | int = 10,
        rolling_resistance: float = 0.005,
        drivetrain_loss: float = 0.04,
    ):
        self.name = name
        self.kg = kg
        self.height = height
        self.ftp = ftp
        self.power = power
        self.frontal_area = frontal_area
        self.bike_kg = bike_kg
        self.rolling_resistance = rolling_resistance
        self.drivetrain_loss = drivetrain_loss
