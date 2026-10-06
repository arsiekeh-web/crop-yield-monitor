# tests/test_crop_yield.py
import json

import pytest

from cropyield import storage
from cropyield.exceptions import (
    DuplicateRecordError,
    RecordNotFoundError,
    StorageError,
)
from cropyield.models import HarvestRecord, Plot
from cropyield.monitor import YieldMonitor


def make_record(record_id="REC-001", crop="Cassava", area=2.0, qty=1000):
    return HarvestRecord(record_id, Plot("PLT-001", crop, area), (2026, "Rainy"), qty)


def test_plot_rejects_zero_or_negative_area():
    with pytest.raises(ValueError):
        Plot("PLT-001", "Rice", 0)
    with pytest.raises(ValueError):
        Plot("PLT-001", "Rice", -1)


def test_record_rejects_negative_quantity():
    with pytest.raises(ValueError):
        make_record(qty=-5)


def test_record_rejects_bad_season():
    with pytest.raises(ValueError):
        HarvestRecord("REC-001", Plot("PLT-001", "Rice", 1), (2026, "Summer"), 10)


def test_yield_per_hectare():
    assert make_record(area=2.0, qty=1000).yield_per_hectare() == 500


def test_update_quantity():
    record = make_record()
    record.update_quantity(2000)
    assert record.quantity_kg == 2000


def test_static_method_converts_kg_to_tonnes():
    assert HarvestRecord.convert_kg_to_tonnes(2500) == 2.5


def test_class_method_builds_plot_from_dict():
    plot = Plot.from_dict({"plot_id": "PLT-009", "crop": "Maize", "area_ha": 3})
    assert plot.crop == "Maize"
    assert Plot.total_plots_created() >= 1


def test_duplicate_record_is_refused():
    monitor = YieldMonitor()
    monitor.add_record(make_record())
    with pytest.raises(DuplicateRecordError):
        monitor.add_record(make_record())


def test_missing_record_raises():
    with pytest.raises(RecordNotFoundError):
        YieldMonitor().get_record("NOPE")


def test_average_yield_for_crop_is_case_insensitive():
    monitor = YieldMonitor()
    monitor.add_record(make_record("REC-001", "Cassava", 2.0, 1000))  # 500 kg/ha
    monitor.add_record(make_record("REC-002", "cassava", 1.0, 1500))  # 1500 kg/ha
    assert monitor.average_yield_for_crop("CASSAVA") == 1000
    assert monitor.average_yield_for_crop("Rice") == 0.0


def test_save_and_load_round_trip(tmp_path):
    monitor = YieldMonitor()
    monitor.add_record(make_record())
    path = tmp_path / "records.json"
    storage.save(monitor, path)
    loaded = storage.load(path)
    assert loaded.get_record("REC-001").quantity_kg == 1000
    assert loaded.get_record("REC-001").season == (2026, "Rainy")


def test_load_missing_file_gives_empty_monitor(tmp_path):
    assert list(storage.load(tmp_path / "nothing.json").all_records()) == []


def test_load_corrupt_file_raises_storage_error(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{ this is not valid json", encoding="utf-8")
    with pytest.raises(StorageError):
        storage.load(path)


def test_load_file_with_missing_fields_raises_storage_error(tmp_path):
    path = tmp_path / "incomplete.json"
    path.write_text(json.dumps([{"record_id": "REC-001"}]), encoding="utf-8")
    with pytest.raises(StorageError):
        storage.load(path)
