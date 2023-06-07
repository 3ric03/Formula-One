from format_time import format_laptime
from format_time import format_time_delta
import fastf1
import fastf1.plotting
import seaborn as sns
from matplotlib import pyplot as plt
from fastf1.core import Laps
from fastf1.core import Lap
import pandas as pd
from timple.timedelta import strftimedelta

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

    
def is_wet(race, driver):
    tyre_series = race.laps.pick_driver(driver)["Compound"]
    for tyre in tyre_series:
        if tyre == "Wet" or tyre == "Intermediate":
            return True
    return False

def plot_driver_race_laptime (race, driver):
    wet = False

    fastf1.plotting.setup_mpl(misc_mpl_mods=False)
    wet = is_wet(race, driver)
    
    if wet:
        laps = race.laps.pick_driver(driver).pick_quicklaps(1.08).reset_index()
    else:
        laps = race.laps.pick_driver(driver).pick_quicklaps(1.40).reset_index()
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
    
    
def plot_laptimes_comparison (race, driver1, driver2):
    wet = False
    wet = is_wet(race, driver1)
    fastf1.plotting.setup_mpl(misc_mpl_mods=False)
    
    if wet:
        laps1 = race.laps.pick_driver(driver1).pick_quicklaps(1.08).reset_index()
        laps2 = race.laps.pick_driver(driver2).pick_quicklaps(1.08).reset_index()
    else:
        laps1 = race.laps.pick_driver(driver1).pick_quicklaps(1.40).reset_index()
        laps2 = race.laps.pick_driver(driver2).pick_quicklaps(1.40).reset_index()
        
    print(laps1.head(5))
    fig, ax = plt.subplots(figsize=(8, 8))
    
    lap_list1 = list()
    lap_list2 = list()
    
    for lap in laps1.iterlaps():
        lap_list1.append(lap[1])
    for lap in laps2.iterlaps():
        lap_list2.append(lap[1])
    
    lap_df_1 = pd.concat(lap_list1)
    lap_df_2 = pd.concat(lap_list2)
    
    merge_list = [lap_df_1, lap_df_2] #lap dataframe for driver 1 and driver 2
    merge_df = pd.concat(merge_list) #merge into one dataframe
    
    fig, ax = plt.subplots(figsize=(8, 8))
    print(type(merge_df))
    sns.scatterplot(data=merge_df,
                x="LapNumber",
                y="LapTime",
                ax=ax,
                linewidth=0,
                legend='auto')


    plt.show()
    
def plot_q3_flying_laps(quali):
    fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme=None, misc_mpl_mods=False)
    
    font1 = {'family':'serif','color':'black','size':17}
    q1, q2, q3 = quali.laps.split_qualifying_sessions()
    pole = quali.laps.pick_fastest()["LapTime"]
    top_drivers = quali.drivers[:6] #change back to 8
    
    hot_lap_list = list()
    for driver in top_drivers:
        hot_laps = q3.pick_driver(driver).pick_quicklaps()
        index = 1
        
        for lap in hot_laps.iterlaps():
            lap[1]['Flying_Index'] = lap[1]['Driver'] + " Lap " + str(index)
            lap[1]["LapTimeDelta"] = format_time_delta(lap[1]["LapTime"] - pole)
            index+=1
            hot_lap_list.append(lap[1])
            
    sorted_hot_laps = Laps(hot_lap_list).sort_values(by='LapTime').reset_index(drop=True)
    pole_lap = sorted_hot_laps.pick_fastest()
    #sorted_hot_laps['LapTimeDelta'] =  sorted_hot_laps['LapTime'] - pole_lap['LapTime']
    team_colors = list()

    for index, lap in sorted_hot_laps.iterlaps():
        color = fastf1.plotting.team_color(lap['Team'])
        team_colors.append(color)
    
    fig, ax = plt.subplots()
    horizontal_bars = ax.barh(sorted_hot_laps.index, sorted_hot_laps['LapTimeDelta'],
    color=team_colors, edgecolor='grey')
    ax.set_yticks(sorted_hot_laps.index)
    ax.set_yticklabels(sorted_hot_laps['Flying_Index'])

    # show fastest at the top
    ax.invert_yaxis()

    # draw vertical lines behind the bars
    ax.set_axisbelow(True)
    ax.xaxis.grid(True, which='major', linestyle='--', color='black', zorder=-1000)
    
    pole_time = strftimedelta(pole_lap['LapTime'], '%m:%s.%ms')

    plt.title(f"{quali.event['EventName']} {quali.event.year} Qualifying\n"
             f"Pole Lap Time: {pole_time} ({pole_lap['Driver']})", fontdict=font1)
    
    plt.xlabel("Time Delta (Seconds)")
    plt.ylabel("Flying Laps")
    
    for i, value in enumerate(sorted_hot_laps['LapTimeDelta']):
        if i == 0:
            plt.text(value, i, " " + str(pole_time), ha='left', va='center')
            continue
        plt.text(value, i, " +" + str(value), ha='left', va='center')

    plt.show()
   

    
    
def inner_menu(index, event):
    if index == 1:
        driver = input("Enter driver name: ")
        race = event.get_race()
        race.load()
        plot_driver_race_laptime(race, driver)
    if index == 2:
        driver1 = input("Enter driver 1 number: ")
        driver2 = input("Enter driver 2 number: ")
        race = event.get_race()
        race.load()
        plot_laptimes_comparison(race, driver1, driver2)
    if index == 3:
        quali = event.get_qualifying()
        quali.load()
        plot_q3_flying_laps(quali)
        
        
    