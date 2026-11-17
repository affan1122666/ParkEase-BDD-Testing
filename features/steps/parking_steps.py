import re
from datetime import timedelta
import parse
from behave import given, when, then, register_type
from parkease import today_at

@parse.with_pattern(r"Rs\. \d{1,3}(?:,\d{3})*")
def parse_rupees(value):
    return int(value.replace("Rs. ", "").replace(",", ""))

@parse.with_pattern(r"\d+ (?:h|min|s)(?: \d+ (?:min|s))*")
def parse_duration(value):
    units = {"h": "hours", "min": "minutes", "s": "seconds"}
    parts = {units[unit]: int(number)
             for number, unit in re.findall(r"(\d+) (h|min|s)", value)}
    return timedelta(**parts)

@parse.with_pattern(r"\d{2}:\d{2}")
def parse_clock(value):
    return today_at(value)

@parse.with_pattern(r"electric|petrol")
def parse_vehicle_kind(value):
    return value == "electric"

register_type(Rupees=parse_rupees, Duration=parse_duration,
              Clock=parse_clock, Kind=parse_vehicle_kind)

TEST_EXIT = today_at("23:00")

def money(value):
    return f"Rs. {value:,}"

def check_money(label, expected, actual):
    assert actual == expected, (
        f"{label}: expected {money(expected)}, but actual value was {money(actual)}"
    )

@given('driver "{name}" has an active ParkEase session')
def active_session(context, name):
    context.app.login(name)

@given('the {kind:Kind} vehicle "{plate}" belongs to this driver')
def linked_vehicle(context, kind, plate):
    context.app.link_vehicle(plate, kind)
    context.plate = plate

@given("the wallet contains {amount:Rupees}")
def wallet_funded(context, amount):
    context.app.set_wallet(amount)
    context.initial_balance = amount

@given("the vehicle entered at {entry:Clock}")
def entry_recorded(context, entry):
    context.app.record_entry(context.plate, entry)

@given("the vehicle has stayed for {duration:Duration}")
def duration_recorded(context, duration):
    context.app.record_duration(context.plate, duration, TEST_EXIT)

@when("the vehicle exits at {exit_time:Clock}")
def exit_at_time(context, exit_time):
    context.result = context.app.exit_at(context.plate, exit_time)

@when("the vehicle exits the plaza")
def exit_now(context):
    context.result = context.app.exit_at(context.plate, TEST_EXIT)

@then('the driver should receive the message "{message}"')
def message_is(context, message):
    assert context.result.message == message, (
        f"Message: expected '{message}', got '{context.result.message}'"
    )

@then("the parking fee should be {amount:Rupees}")
def parking_fee_is(context, amount):
    check_money("Parking fee", amount, context.result.parking_fee)

@then("the EV reduction should be {amount:Rupees}")
def ev_discount_is(context, amount):
    check_money("EV reduction", amount, context.result.ev_discount)

@then("the service fee should be {amount:Rupees}")
def service_fee_is(context, amount):
    check_money("Service fee", amount, context.result.service_charge)

@then("the total charge should be {amount:Rupees}")
def total_is(context, amount):
    check_money("Total charge", amount, context.result.total_paid)

@then("the remaining wallet should be {amount:Rupees}")
def remaining_wallet_is(context, amount):
    check_money("Wallet balance", amount, context.app.wallet_balance())

@then("the wallet amount should remain unchanged")
def wallet_unchanged(context):
    check_money("Unchanged wallet", context.initial_balance,
                context.app.wallet_balance())

@then("the exit barrier should open")
def barrier_opens(context):
    assert context.result.gate_open, "Expected exit barrier OPEN, but it remained CLOSED"

@then("the exit barrier should remain closed")
def barrier_stays_closed(context):
    assert not context.result.gate_open, "Expected exit barrier CLOSED, but it OPENED"
