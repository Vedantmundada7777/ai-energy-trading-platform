from src.state import BatteryState

def step(state: BatteryState, action_kw: float, dt_hours: float = 1.0):
    """
    action_kw > 0  → charging
    action_kw < 0  → discharging
    """

    # Enforce power limits
    action_kw = max(
        -state.max_discharge_kw,
        min(state.max_charge_kw, action_kw)
    )

    # Energy change (kWh)
    delta_energy = action_kw * dt_hours

    # Convert SOC → energy
    energy = state.soc * state.capacity_kwh
    energy_next = energy + delta_energy

    # Clamp energy within bounds
    energy_next = max(0, min(state.capacity_kwh, energy_next))

    # Update SOC
    soc_next = energy_next / state.capacity_kwh

    return BatteryState(
        soc=soc_next,
        capacity_kwh=state.capacity_kwh,
        max_charge_kw=state.max_charge_kw,
        max_discharge_kw=state.max_discharge_kw
    )