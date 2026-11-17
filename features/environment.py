from parkease import ParkEase

def before_scenario(context, scenario):
    context.app = ParkEase()
    context.plate = None
    context.initial_balance = None
    context.result = None
