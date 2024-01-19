def race_tyre_types (race, drivers: list[int]):
    compounds = []
    for driver in drivers:
        driver_laps = race.laps.pick_driver(str(driver))
        stint = driver_laps[["Stint", "Compound", "LapNumber"]]
        stint = stint.groupby(["Stint", "Compound"]).count().reset_index()
        stint = stint.rename(columns={"LapNumber": "StintLength"})
        compounds.append(stint["Compound"].tolist())
    return compounds
        