import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import time
import numpy as np

# Interaktiver Benutzereingabe für das Datum
selected_date_str = input("Bitte geben Sie das Datum im Format TT.MM.JJJJ ein: ")
selected_date = datetime.strptime(selected_date_str, "%d.%m.%Y")

start_time = time.time()                      #Startzeit des Programms


# Pfad der Dateien
# CSV-Dateien müssen im gleichen Ordner wie das Python-Skript liegen
import os
print(os.getcwd())

# Dateinamen
file_production = 'Realisierte_Erzeugung_.csv'
file_consumption = 'Realisierter_Stromverbrauch_.csv'

# Einlesen der Daten aus CSV-Dateien
production_df = pd.read_csv(file_production, delimiter=';')
consumption_df = pd.read_csv(file_consumption, delimiter=';')

# Spaltenbezeichnungen
DATE = 'Datum'
STARTTIME = 'Anfang'
BIOMAS = 'Biomasse [MWh] Originalauflösungen'
HYDROELECTRIC = 'Wasserkraft [MWh] Originalauflösungen'
WIND_OFFSHORE = 'Wind Offshore [MWh] Originalauflösungen'
WIND_ONSHORE = 'Wind Onshore [MWh] Originalauflösungen'
PHOTOVOLTAIC = 'Photovoltaik [MWh] Originalauflösungen'
OTHER_RENEWABLE = 'Sonstige Erneuerbare [MWh] Originalauflösungen'
CONSUMPTION = 'Gesamt (Netzlast) [MWh] Originalauflösungen'

# Umwandlung von Datumsspalten in DateTime-Objekte
production_df[DATE] = pd.to_datetime(production_df[DATE], format='%d.%m.%Y')
production_df[STARTTIME] = pd.to_datetime(production_df[STARTTIME], format='%H:%M')
consumption_df[DATE] = pd.to_datetime(consumption_df[DATE], format='%d.%m.%Y')
consumption_df[STARTTIME] = pd.to_datetime(consumption_df[STARTTIME], format='%H:%M')

# Bereinigung von Datenformaten der erneubaren Energien
columns_to_clean = [HYDROELECTRIC, BIOMAS, WIND_OFFSHORE, WIND_ONSHORE, PHOTOVOLTAIC, OTHER_RENEWABLE]
for column in columns_to_clean:
    production_df[column] = production_df[column].str.replace(".", "").str.replace(",", ".").replace('-', 0).astype(float)

# Bereinigung von Datenformaten des Gesamtenstromverbrauches
consumption_df[CONSUMPTION] = consumption_df[CONSUMPTION].str.replace(".", "").str.replace(",", ".").astype(float)

production_df['Total Production'] = production_df[columns_to_clean].sum(axis=1)
production_by_year = production_df.groupby(production_df[DATE].dt.year)['Total Production'].sum()
consumption_by_year = consumption_df.groupby(consumption_df[DATE].dt.year)[CONSUMPTION].sum()

production_by_type_and_year = production_df.groupby(production_df[DATE].dt.year)[columns_to_clean].sum()

pd.options.display.float_format = '{:.2f}'.format  # Set Pandas to display floating-point numbers with two decimal places

data_by_year = {}                                  # Aggregation der Daten nach Jahren und Speicherung in einem Dictionary

for year, data in production_df.groupby(production_df[DATE].dt.year):
    production_data = data[columns_to_clean].sum()
    consumption_data = consumption_df[consumption_df[DATE].dt.year == year][CONSUMPTION]
    total_consumption = consumption_data.sum()
    data_by_year[year] = {'Production': production_data.sum(), 'Consumption': total_consumption, BIOMAS: production_data[BIOMAS], HYDROELECTRIC: production_data[HYDROELECTRIC], WIND_OFFSHORE: production_data[WIND_OFFSHORE], WIND_ONSHORE: production_data[WIND_ONSHORE], PHOTOVOLTAIC: production_data[PHOTOVOLTAIC], OTHER_RENEWABLE: production_data[OTHER_RENEWABLE]}


for year, data in data_by_year.items():             # Ausgabe der aggregierten Daten pro Jahr
    print(f"Year: {year}")
    print(f"Total Renewable Energy Production: {data['Production']} MWh")
    print(f"Total Consumption: {data['Consumption']} MWh")
    print(f"Biomasse: {data[BIOMAS]} MWh")
    print(f"Wasserkraft: {data[HYDROELECTRIC]} MWh")
    print(f"Wind Offshore: {data[WIND_OFFSHORE]} MWh")
    print(f"Wind Onshore: {data[WIND_ONSHORE]} MWh")
    print(f"Photovoltaik: {data[PHOTOVOLTAIC]} MWh")
    print(f"Sonstige Erneuerbare: {data[OTHER_RENEWABLE]} MWh")
    print()


total_renewable_production = production_df[columns_to_clean].sum(axis=1)
total_consumption = consumption_df[CONSUMPTION]


def range1(array1, array2):               # Berechnung der prozentualen Anteile der erneuerbaren Energieerzeugung am Gesamtverbrauch
    if len(array1) != len(array2):
        raise ValueError("Arrays must be the same length")
    
    counts = [0] * 111

    for val1, val2 in zip(array1, array2):
        ratio = val1 / val2
        percent = int(ratio * 100)

        if percent == 100:
            counts[percent] += 1
        elif 0 <= percent < 110:
            counts[percent] += 1

    return counts

counts = range1(total_renewable_production, total_consumption)
n = range(111) # Anzahl der Prozenten

# Ausgabe von Anteilen
def get_result(array1, array2):
    print("Anteile in %:")
    if len(array1) != len(array2):
        raise ValueError("Arrays must be the same length")
    
    for val1, val2 in zip(array1, array2):
        print( val1, "% :"   , val2)

get_result(n, counts)
print("Anzahl der Viertelstunden in 3 Jahren:", sum(counts))
print()

# Filtern der Daten für das ausgewählte Datum
selected_production = production_df[production_df[DATE] == selected_date]
selected_consumption = consumption_df[consumption_df[DATE] == selected_date]

end_time = time.time()                         # The time at the end of the program is stored
duration = end_time - start_time               # Duration of the program is calculated
print("Duration of the program: ", round(duration, 2))

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(selected_production[STARTTIME], selected_production['Total Production'], label='Total Renewable Production')
plt.plot(selected_consumption[STARTTIME], selected_consumption[CONSUMPTION], label='Total Consumption')

plt.title(f'Renewable Energy Production and Total Consumption on {selected_date_str}')
plt.xlabel('Time (hours)')
plt.ylabel('Energy (MWh)')
plt.legend()
plt.grid(True)

# Format x-axis ticks and labels
unique_hours = sorted(selected_production[STARTTIME].dt.hour.unique())
plt.xticks(selected_production[STARTTIME], selected_production[STARTTIME].dt.strftime('%H:%M'), rotation=45)
plt.gca().set_xticks(selected_production[STARTTIME][::4])
plt.gca().set_xticklabels(selected_production[STARTTIME].dt.strftime('%H')[::4])

plt.show()



"""
# Ein Beispiel für die Berechnung der Gesamtsumme einer bestimmten Art
selected_energy_type = WIND_ONSHORE

# Für einen Tag
selected_production_day = selected_production[selected_energy_type].sum()
print(f"{selected_energy_type} Production on {selected_date}: {selected_production_day} MWh")

# Für ein Jahr
selected_production_year = production_by_type_and_year.loc[selected_date.year, selected_energy_type]
print(f"{selected_energy_type} Production for {selected_date.year}: {selected_production_year} MWh")

# Ein Beispiel für die Arbeit mit Listen einer bestimmten Art
selected_energy_type = WIND_ONSHORE

# Für einen Tag
selected_production_day_list = selected_production[selected_energy_type].astype(float).tolist()
print(f"{selected_energy_type} Production List on {selected_date}: {selected_production_day_list}")

# Für ein Jahr
selected_production_year_list = production_by_type_and_year.loc[selected_date.year, selected_energy_type].tolist()
print(f"{selected_energy_type} Production List for {selected_date.year}: {selected_production_year_list}")

"""

# function that multiplies Windonshore, Windoffshore and PV  with 2030 "Ausbaufaktoren"

def scale_2030_factors(df, windonshore_factor, windoffshore_factor, pv_factor):
    df_copy = df.copy()
    df_copy[WIND_ONSHORE] *= windonshore_factor
    df_copy[WIND_OFFSHORE] *= windoffshore_factor
    df_copy[PHOTOVOLTAIC] *= pv_factor
    df_copy['Total Production'] = df_copy[columns_to_clean].sum(axis=1)
    return df_copy


# Define the factors
windonshore_2030_factor = 2.03563  # assuming Wind Onshore will increase by 203%
windoffshore_2030_factor = 3.76979  # assuming Wind Offshore will 376% increase
pv_2030_factor = 3.5593  # assuming PV will increase by 350%

# Scale the data by the factors
scaled_production_df = scale_2030_factors(production_df, windonshore_2030_factor, windoffshore_2030_factor, pv_2030_factor)

# Filter scaled data for the selected date
scaled_selected_production = scaled_production_df[scaled_production_df[DATE] == selected_date]

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(scaled_selected_production[STARTTIME], scaled_selected_production['Total Production'], label='Total Renewable Production - Scaled')
plt.plot(selected_consumption[STARTTIME], selected_consumption[CONSUMPTION], label='Total Consumption')

plt.title(f'Scaled Renewable Energy Production and Total Consumption on {selected_date_str}')
plt.xlabel('Time (hours)')
plt.ylabel('Energy (MWh)')
plt.legend()
plt.grid(True)

# Format x-axis ticks and labels
unique_hours = sorted(scaled_selected_production[STARTTIME].dt.hour.unique())
plt.xticks(scaled_selected_production[STARTTIME], scaled_selected_production[STARTTIME].dt.strftime('%H:%M'), rotation=45)
plt.gca().set_xticks(scaled_selected_production[STARTTIME][::4])
plt.gca().set_xticklabels(scaled_selected_production[STARTTIME].dt.strftime('%H')[::4])

plt.show()


counts = range1(total_renewable_production, total_consumption)
n = range(111) # Anzahl der Prozenten
# Ausgabe von Anteilen
def get_result(array1, array2):
    print("Anteile in %:")
    if len(array1) != len(array2):
        raise ValueError("Arrays must be the same length")
    
    for val1, val2 in zip(array1, array2):
        print( val1, "% :"   , val2)

get_result(n, counts)
print("Anzahl der Viertelstunden in 2030 (prognostiziert):", sum(counts))
print()

# Calculate total renewable production for scaled data
total_renewable_scaled_production = scaled_production_df[columns_to_clean].sum(axis=1)

# get the counts for scaled data
scaled_counts = range1(total_renewable_scaled_production, total_consumption)

# Ausgabe von Anteilen for scaled data
get_result(n, scaled_counts)
print("Anzahl der Viertelstunden in 2030 (mit erreichen der 2030 Ausbauzielen des BMWK):", sum(scaled_counts))
print()

# Generate the plot for scaled data
fig, ax = plt.subplots(figsize=(10, 6))  # Adjust size as needed
x = range(111)  # For percentages 0-110
ax.bar(x, scaled_counts, width=1)  # width=1 for contiguous bars
ax.set_title('Anzahl der Viertelstunden mit 1-100 % EE-Anteil in 2030 (prognostiziert)')
ax.set_xlabel('Percentage of Total Consumption (%)')
ax.set_ylabel('Anzahl der Viertelstunden')
ax.set_xticks(x[::10])
ax.set_xticklabels([f'{i}%' for i in range(0, 111, 10)])
plt.show()

# assuming quarter_hour_scaled_production and quarter_hour_consumption are your quarter-hourly production and consumption data
# Calculate the ratio for each quarter-hour
ratio_quarter_hour = quarter_hour_scaled_production / quarter_hour_consumption

# Check if any ratio is greater than 1.11 (111%)
higher_share_quarter_hour = any(ratio_quarter_hour > 1.11)

print("The renewables have a higher share than 111% in any quarter-hour:", higher_share_quarter_hour)
