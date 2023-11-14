import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import time

start_time = time.time()

file_renewable = 'Realisierte_Erzeugung_202001010000_202212312359_Viertelstunde.csv'
file_consumption = 'Realisierter_Stromverbrauch_202001010000_202212312359_Viertelstunde.csv'

renewable_energy_data = pd.read_csv(file_renewable, delimiter=';')
energy_consumption_data = pd.read_csv(file_consumption, delimiter=';')

DATE = 'Datum'
BIOMAS = 'Biomasse [MWh] Originalauflösungen'
HYDROELECTRIC = 'Wasserkraft [MWh] Originalauflösungen'
WIND_OFFSHORE = 'Wind Offshore [MWh] Originalauflösungen'
WIND_ONSHORE = 'Wind Onshore [MWh] Originalauflösungen'
PHOTOVOLTAIC = 'Photovoltaik [MWh] Originalauflösungen'
OTHER_RENEWABLE = 'Sonstige Erneuerbare [MWh] Originalauflösungen'
CONSUMPTION = 'Gesamt (Netzlast) [MWh] Originalauflösungen'


renewable_energy_data[DATE] = pd.to_datetime(renewable_energy_data[DATE], format='%d.%m.%Y')
energy_consumption_data[DATE] = pd.to_datetime(energy_consumption_data[DATE], format='%d.%m.%Y')

columns_to_clean = [HYDROELECTRIC, BIOMAS, WIND_OFFSHORE, WIND_ONSHORE, PHOTOVOLTAIC, OTHER_RENEWABLE]
for column in columns_to_clean:
    renewable_energy_data[column] = renewable_energy_data[column].str.replace(".", "").str.replace(",", ".").replace('-', 0).astype(float)

energy_consumption_data[CONSUMPTION] = energy_consumption_data[CONSUMPTION].str.replace(".", "").str.replace(",", ".").astype(float)

renewable_energy_data['Total Production'] = renewable_energy_data[columns_to_clean].sum(axis=1)
production_by_year = renewable_energy_data.groupby(renewable_energy_data[DATE].dt.year)['Total Production'].sum()
consumption_by_year = energy_consumption_data.groupby(energy_consumption_data[DATE].dt.year)[CONSUMPTION].sum()

production_by_type_and_year = renewable_energy_data.groupby(renewable_energy_data[DATE].dt.year)[columns_to_clean].sum()

pd.options.display.float_format = '{:.2f}'.format

data_by_year = {}

for year, data in renewable_energy_data.groupby(renewable_energy_data[DATE].dt.year):
    production_data = data[columns_to_clean].sum()
    consumption_data = energy_consumption_data[energy_consumption_data[DATE].dt.year == year][CONSUMPTION]
    total_consumption = consumption_data.sum()
    data_by_year[year] = {'Production': production_data.sum(), 'Consumption': total_consumption, BIOMAS: production_data[BIOMAS], HYDROELECTRIC: production_data[HYDROELECTRIC], WIND_OFFSHORE: production_data[WIND_OFFSHORE], WIND_ONSHORE: production_data[WIND_ONSHORE], PHOTOVOLTAIC: production_data[PHOTOVOLTAIC], OTHER_RENEWABLE: production_data[OTHER_RENEWABLE]}


for year, data in data_by_year.items():
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


total_renewable_production = renewable_energy_data[columns_to_clean].sum(axis=1)
total_consumption = energy_consumption_data[CONSUMPTION]

def range1(array1, array2):
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

counts =[]
counts = range1(total_renewable_production, total_consumption)
n = []
n = range(111)

def get_result(array1, array2):
    print("Anteile in %:")
    if len(array1) != len(array2):
        raise ValueError("Arrays must be the same length")
    
    for val1, val2 in zip(array1, array2):
        print( val1, "% :"   , val2)

get_result(n, counts)
print("Anzahl der Viertelstunden in 3 Jahren:", sum(counts))
print()


end_time = time.time()                         # The time at the end of the program is stored
duration = end_time - start_time               # Duration of the program is calculated
print("Duration", duration)


"""
# Wie kann man zu den Daten oben zugreifen
consumption_2021 = data_by_year[2021]['Consumption']
print(f"Total energy consumption in 2021: {consumption_2021} MWh")
"""
