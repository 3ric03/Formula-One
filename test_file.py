import fastf1
import fastf1.plotting
from matplotlib import pyplot as plt
def race_tyre_types (race, drivers: list[int]):
    compounds = []
    for driver in drivers:
        driver_laps = race.laps.pick_driver(str(driver))
        stint = driver_laps[["Stint", "Compound", "LapNumber"]]
        stint = stint.groupby(["Stint", "Compound"]).count().reset_index()
        stint = stint.rename(columns={"LapNumber": "StintLength"})
        print(stint)
        compounds.append(stint["Compound"].tolist())
    return compounds
###############################################################################
# Load the race session

session = fastf1.get_session(2019, "Monza", 'R')
session.load()
print(race_tyre_types(session, [16, 55]))
