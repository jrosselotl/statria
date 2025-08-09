UNIT_CONVERSION = {
    "resistance": {
        "µΩ": 1e-6,
        "mΩ": 1e-3,
        "Ω": 1,
        "kΩ": 1e3,
        "MΩ": 1e6,
        "GΩ": 1e9
    },
    "voltage": {
        "µV": 1e-6,
        "mV": 1e-3,
        "V": 1,
        "kV": 1e3
    },
    "current": {
        "µA": 1e-6,
        "mA": 1e-3,
        "A": 1,
        "kA": 1e3
    },
    "torque": {
        "Nmm": 1e-3,
        "Nm": 1,
        "kNm": 1e3
    },
    "time": {
        "ms": 1e-3,
        "s": 1,
        "min": 60,
        "h": 3600
    }
}


def get_unit_by_test(test_type: str):
    units = {
        "continuity": ["Ω", "mΩ"],
        "insulation": ["kΩ", "MΩ", "GΩ"],
        "contact_resistance": ["Ω", "mΩ", "µΩ"],
        "torque": ["Nm", "kgf·cm", "lbf·in"]
    }
    return units.get(test_type, [])


def convert(value: float, from_unit: str, to_unit: str, category: str) -> float:
    if category not in UNIT_CONVERSION:
        raise ValueError(f"Unknown category: {category}")
    units = UNIT_CONVERSION[category]
    if from_unit not in units or to_unit not in units:
        raise ValueError(f"Unknown unit in {category}: {from_unit} or {to_unit}")
    base_value = value * units[from_unit]
    return base_value / units[to_unit]
