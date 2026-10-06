# cropyield/storage.py
"""Save and load records as plain JSON so data survives after the program closes."""

import json
from pathlib import Path

from cropyield.exceptions import DuplicateRecordError, StorageError
from cropyield.models import HarvestRecord
from cropyield.monitor import YieldMonitor


def save(monitor: YieldMonitor, path) -> None:
    """Write every record to a JSON file."""
    data = [record.to_dict() for record in monitor.all_records()]
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def load(path) -> YieldMonitor:
    """Read records from a JSON file. A missing file simply means a fresh start."""
    monitor = YieldMonitor()
    if not Path(path).exists():
        return monitor
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        for item in data:
            monitor.add_record(HarvestRecord.from_dict(item))
    except (json.JSONDecodeError, KeyError, TypeError, ValueError, DuplicateRecordError) as error:
        raise StorageError(f"The data file could not be read ({error}).") from error
    return monitor
