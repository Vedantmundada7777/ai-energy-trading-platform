from dataclasses import dataclass

@dataclass
class BatteryState:
    soc: float              # State of Charge (0–1)
    capacity_kwh: float     # Battery capacity
    max_charge_kw: float
    max_discharge_kw: float
    