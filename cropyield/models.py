# cropyield/models.py
class Plot:
    """A piece of farmland, identified by a code (never by a person's name)."""
    _plot_count = 0  # class attribute

    def __init__(self, plot_id: str, crop: str, area_ha: float):
        self.plot_id = plot_id
        self.crop = crop
        self.area_ha = area_ha          # validated by the property below
        Plot._plot_count += 1
    def __repr__(self) -> str:
        return f"Plot(plot_id={self.plot_id!r}, crop={self.crop!r}, area_ha={self.area_ha})"
    @property
    def area_ha(self) -> float:
        return self._area_ha

    @area_ha.setter
    def area_ha(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Area must be greater than zero.")
        self._area_ha = float(value)

    @classmethod
    def from_dict(cls, data: dict) -> "Plot":          # CLASS METHOD (alt constructor)
        return cls(data["plot_id"], data["crop"], data["area_ha"])

    @classmethod
    def total_plots_created(cls) -> int:               # CLASS METHOD (uses class state)
        return cls._plot_count

    def to_dict(self) -> dict:
        return {"plot_id": self.plot_id, "crop": self.crop, "area_ha": self.area_ha}

    def display_info(self) -> str:                      # INSTANCE METHOD
        return f"{self.plot_id} | {self.crop} | {self.area_ha} ha"


class HarvestRecord:
    def __init__(self, record_id: str, plot: Plot, season: tuple, quantity_kg: float):
        self.record_id = record_id
        self.plot = plot                                # object interaction
        self.season = season                            # tuple: (year, "Rainy"/"Dry")
        self.quantity_kg = quantity_kg
    def __repr__(self) -> str:
        return (f"HarvestRecord(record_id={self.record_id!r}, plot={self.plot!r}, "
                f"season={self.season!r}, quantity_kg={self.quantity_kg})")
    @property
    def quantity_kg(self) -> float:
        return self._quantity_kg

    @quantity_kg.setter
    def quantity_kg(self, value: float) -> None:
        if value < 0:
            raise ValueError("Quantity cannot be negative.")
        self._quantity_kg = float(value)

    def yield_per_hectare(self) -> float:               # INSTANCE METHOD (uses Plot)
        return self.quantity_kg / self.plot.area_ha

    def update_quantity(self, new_quantity_kg: float) -> None:   # INSTANCE METHOD
        self.quantity_kg = new_quantity_kg

    @staticmethod
    def convert_kg_to_tonnes(kg: float) -> float:       # STATIC METHOD
        return kg / 1000

    def to_dict(self) -> dict:
        return {"record_id": self.record_id, "plot": self.plot.to_dict(),
                "season": list(self.season), "quantity_kg": self.quantity_kg}

    @classmethod
    def from_dict(cls, data: dict) -> "HarvestRecord":
        return cls(data["record_id"], Plot.from_dict(data["plot"]),
                   tuple(data["season"]), data["quantity_kg"])

    def display_info(self) -> str:
        return (f"{self.record_id} | {self.plot.display_info()} | {self.season} | "
                f"{self.quantity_kg} kg | {self.yield_per_hectare():.1f} kg/ha")