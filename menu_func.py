from format_time import format_laptime
import fastf1
import fastf1.plotting
import seaborn as sns
from matplotlib import pyplot as plt

def load_race_event (searched_event):
    race = searched_event.get_race()
    quali = searched_event.get_qualifying()
    race.load()
    quali.load()
    winner = race.drivers[:1]
    pole = quali.drivers[:1]
    
    fastest_lap = format_laptime(race.laps.pick_fastest()["LapTime"])
    pole_lap = format_laptime(quali.laps.pick_drivers(pole).pick_fastest()["LapTime"])
    fastest_laps_delta = format_laptime(race.laps.pick_fastest()["LapTime"] - quali.laps.pick_drivers(pole).pick_fastest()["LapTime"])
    
    print()
    print(searched_event["OfficialEventName"])
    template = "Round {0}, {1}\n{2}\nWinner: {3} Car {4}, {5}\n\nFastest racing lap: {6} ({7})\nPole lap: {8} ({9})\nFastest Lap Delta: {10}"
    print(template.format(searched_event["RoundNumber"], searched_event["Location"], searched_event["Session5Date"],
                            race.results["BroadcastName"].iloc[0], winner[0], race.results["TeamName"].iloc[0], 
            fastest_lap, race.get_driver(race.laps.pick_fastest()["DriverNumber"])["LastName"], pole_lap, 
            race.get_driver(pole[0])["LastName"], fastest_laps_delta))



def plot_driver_race_laptime (race, driver):
    fastf1.plotting.setup_mpl(misc_mpl_mods=False)
    laps = race.laps.pick_driver(driver).pick_quicklaps().reset_index()
    fig, ax = plt.subplots(figsize=(8, 8))

    sns.scatterplot(data=laps,
                x="LapNumber",
                y="LapTime",
                ax=ax,
                hue="Compound",
                palette=fastf1.plotting.COMPOUND_COLORS,
                s=80,
                linewidth=0,
                legend='auto')
    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time")

    # The y-axis increases from bottom to top by default
    # Since we are plotting time, it makes sense to invert the axis
    ax.invert_yaxis()
    sub_title = race.get_driver(driver)["LastName"] + " laptimes, " + race.event["OfficialEventName"]
    plt.suptitle(sub_title)

    # Turn on major grid lines
    plt.grid(color='w', which='major', axis='both')
    sns.despine(left=True, bottom=True)

    plt.tight_layout()
    plt.show()
    
    
def inner_menu(index, event):
    if index == 1:
        driver = input("Enter driver name: ")
        race = event.get_race()
        race.load()
        plot_driver_race_laptime(race, driver)
    