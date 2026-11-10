# energy_tracker.py - Milestone 5: file handling + exception handling
import time
from energy_utils import calculate_kwh, calculate_cost, classify_usage

FILE = "energy_records.txt"
TARIFF = 6.50
CATALOGUE = {"LED Bulb": 12, "Ceiling Fan": 75, "Television": 120,
             "Refrigerator": 180, "AC": 1500}
LOOKUP = {k.lower(): k for k in CATALOGUE}


def read_number(prompt, cast=float):
    """Keep asking until the input can be converted (handles ValueError)."""
    while True:
        try:
            return cast(input(prompt))
        except ValueError:
            print("  Error (ValueError): please enter a valid number.")


def read_hours():
    """Prevent impossible usage values."""
    while True:
        h = read_number("Enter hours/day: ")
        if 0 < h <= 24:
            return h
        print("  Error: hours must be greater than 0 and at most 24.")


def add_record():
    name = input("Enter appliance name: ").strip()
    key = LOOKUP.get(name.lower())
    if key is None:
        print(f"  Rejected: '{name}' is not in the catalogue.")
        return
    units = read_number("Enter number of units: ", int)
    if units <= 0:
        print("  Rejected: units must be at least 1.")
        return
    hours = read_hours()
    kwh = calculate_kwh(CATALOGUE[key], hours, units)
    cost = calculate_cost(kwh, TARIFF)
    with open(FILE, "a") as f:                       # append mode
        f.write(f"{time.strftime('%d-%m-%Y')},{key},{units},{hours},{kwh:.2f},{cost:.2f}\n")
    print(f"  Saved: {key} -> {kwh:.2f} kWh, Rs. {cost:.2f}")


def view_records():
    try:
        with open(FILE, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"  Error (FileNotFoundError): '{FILE}' not found. Add a record first.")
        return
    print(f"\n{'Date':<12}{'Appliance':<13}{'Units':>5}{'Hrs':>6}{'kWh':>9}{'Cost(Rs.)':>11}")
    total = 0.0
    for line in lines:
        d, n, u, h, k, c = line.strip().split(",")
        print(f"{d:<12}{n:<13}{u:>5}{h:>6}{float(k):>9.2f}{float(c):>11.2f}")
        total += float(k)
    print(f"Total saved usage: {total:.2f} kWh ({classify_usage(total)})")


while True:
    print("\n1. Add record  2. View records  3. Exit")
    choice = input("Choose: ").strip()
    if choice == "1":
        add_record()
    elif choice == "2":
        view_records()
    elif choice == "3":
        print("Goodbye!")
        break
    else:
        print("  Invalid choice.")