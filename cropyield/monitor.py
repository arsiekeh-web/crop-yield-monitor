# cropyield/monitor.py
"""YieldMonitor: manages all harvest records in ONE dictionary (record_id -> record)."""

from cropyield.exceptions import DuplicateRecordError, RecordNotFoundError


class YieldMonitor:
    def __init__(self):
        self._records = {}  # THE one data structure used by this program

    def add_record(self, record) -> None:
        """Add a HarvestRecord. Refuses duplicate IDs."""
        if record.record_id in self._records:
            raise DuplicateRecordError(f"{record.record_id} already exists.")
        self._records[record.record_id] = record

    def get_record(self, record_id: str):
        """Return the record with this ID, or raise RecordNotFoundError."""
        try:
            return self._records[record_id]
        except KeyError:
            raise RecordNotFoundError(f"No record {record_id}.") from None

    def display_records(self) -> None:
        """Print every record, or a friendly message if there are none."""
        if not self._records:
            print("No records yet.")
        for record in self._records.values():
            print(record.display_info())

    def all_records(self):
        """Read-only view for other modules (e.g. storage)."""
        return self._records.values()

    def average_yield_for_crop(self, crop: str) -> float:
        """Average kg per hectare for one crop; 0.0 if there are no records."""
        yields = [
            r.yield_per_hectare()
            for r in self._records.values()
            if r.plot.crop.lower() == crop.lower()
        ]
        return sum(yields) / len(yields) if yields else 0.0
