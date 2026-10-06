# cropyield/cli.py
"""Plain-language, text-based menu. Works offline on any low-spec computer."""

from cropyield import storage
from cropyield.exceptions import CropYieldError
from cropyield.models import HarvestRecord, Plot
from cropyield.monitor import YieldMonitor

MENU = """
=== Crop Yield Monitor ===
1) Add harvest record
2) View all records
3) Update a quantity
4) Average yield for a crop
5) Save and exit
"""


def ask_text(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Please type something.")


def ask_number(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a number, for example 2.5")


def ask_season() -> tuple:
    while True:
        year = ask_number("Year (e.g. 2026): ")
        if year == int(year) and 1900 <= year <= 2100:
            year = int(year)
            break
        print("Please enter a whole year, for example 2026.")
    while True:
        name = ask_text("Season (Rainy or Dry): ").capitalize()
        if name in ("Rainy", "Dry"):
            return year, name
        print("Please type Rainy or Dry.")


def add_record_flow(monitor: YieldMonitor) -> None:
    record_id = ask_text("Record ID (e.g. REC-006): ")
    plot_id = ask_text("Plot code (e.g. PLT-006, no personal names): ")
    crop = ask_text("Crop (e.g. Cassava): ")
    area = ask_number("Plot area in hectares: ")
    season = ask_season()
    quantity = ask_number("Quantity harvested in kg: ")

    plot = Plot(plot_id, crop, area)
    monitor.add_record(HarvestRecord(record_id, plot, season, quantity))
    print("Record added.")


def update_flow(monitor: YieldMonitor) -> None:
    record = monitor.get_record(ask_text("Record ID to update: "))
    record.update_quantity(ask_number("New quantity in kg: "))
    print("Quantity updated.")


def average_flow(monitor: YieldMonitor) -> None:
    crop = ask_text("Crop name: ")
    average = monitor.average_yield_for_crop(crop)
    if average == 0:
        print(f"No records found for {crop}.")
    else:
        print(f"Average yield for {crop}: {average:.1f} kg per hectare")


def run_menu(monitor: YieldMonitor, data_path) -> None:
    while True:
        print(MENU)
        choice = input("Choose 1-5: ").strip()
        try:
            if choice == "1":
                add_record_flow(monitor)
            elif choice == "2":
                monitor.display_records()
            elif choice == "3":
                update_flow(monitor)
            elif choice == "4":
                average_flow(monitor)
            elif choice == "5":
                storage.save(monitor, data_path)
                print("Saved. Goodbye!")
                break
            else:
                print("Please choose a number from 1 to 5.")
        except (CropYieldError, ValueError) as error:
            print(f"Sorry, that didn't work: {error}")
