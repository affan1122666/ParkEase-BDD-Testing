"""Small in-memory implementation of the ParkEase exit-payment rules."""
import math
from dataclasses import dataclass
from datetime import datetime

GRACE_SECONDS = 15 * 60
FIRST_HOUR_RATE = 100
LATER_HOUR_RATE = 60
MAX_PARKING_FEE = 800
EV_DISCOUNT = 25
SERVICE_FEE = 20

@dataclass
class ExitResult:
    message: str
    parking_fee: int = 0
    ev_discount: int = 0
    service_charge: int = 0
    total_paid: int = 0
    gate_open: bool = False

class ParkEase:
    def __init__(self):
        self.driver = None
        self.vehicles = {}
        self.entry_times = {}
        self.balance = 0
        self.last_receipt = None

    def login(self, driver):
        self.driver = driver

    def link_vehicle(self, plate, is_ev):
        self.vehicles[plate] = is_ev

    def set_wallet(self, amount):
        self.balance = amount

    def wallet_balance(self):
        return self.balance

    def record_entry(self, plate, entry_time):
        self.entry_times[plate] = entry_time

    def record_duration(self, plate, duration, exit_time):
        self.entry_times[plate] = exit_time - duration

    @staticmethod
    def started_hours(seconds):
        return math.ceil(seconds / 3600)

    def calculate_parking_fee(self, seconds):
        hours = self.started_hours(seconds)
        raw = FIRST_HOUR_RATE + max(0, hours - 1) * LATER_HOUR_RATE
        return min(raw, MAX_PARKING_FEE)

    def exit_after(self, plate, seconds):
        if self.driver is None:
            return ExitResult("Please log in to pay by wallet")
        if plate not in self.vehicles:
            return ExitResult("Vehicle is not linked to your account")
        if seconds <= GRACE_SECONDS:
            result = ExitResult("Free exit, gate opening", gate_open=True)
            self.last_receipt = result
            return result

        hours = self.started_hours(seconds)
        fee = self.calculate_parking_fee(seconds)

        discount = fee * EV_DISCOUNT // 100 if self.vehicles[plate] else 0

        service = SERVICE_FEE

        total = fee - discount + service

        if self.balance < total:
            return ExitResult("Insufficient wallet balance", fee, discount, service, 0, False)

        self.balance -= total
        result = ExitResult("Payment successful – gate opening",
                            fee, discount, service, total, True)
        self.last_receipt = result
        return result

    def exit_at(self, plate, exit_time):
        seconds = int((exit_time - self.entry_times[plate]).total_seconds())
        return self.exit_after(plate, seconds)

def today_at(value):
    parsed = datetime.strptime(value, "%H:%M")
    return datetime(2026, 11, 17, parsed.hour, parsed.minute)
