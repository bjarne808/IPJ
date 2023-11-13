import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import time

start_time = time.time()

file_renewable = 'Realisierte_Erzeugung_202001010000_202212312359_Viertelstunde.csv'
file_consumption = 'Realisierter_Stromverbrauch_202001010000_202212312359_Viertelstunde.csv'

renewable_energy_data = pd.read_csv(file_renewable, delimiter=';')
energy_consumption_data = pd.read_csv(file_consumption, delimiter=';')


renewable_energy_data['Datum'] = pd.to_datetime(renewable_energy_data['Datum'], format='%d.%m.%Y')
energy_consumption_data['Datum'] = pd.to_datetime(energy_consumption_data['Datum'], format='%d.%m.%Y')

columns_to_clean = ['Wasserkraft [MWh] Originalauflösungen', 'Biomasse [MWh] Originalauflösungen', 'Wind Offshore [MWh] Originalauflösungen', 'Wind Onshore [MWh] Originalauflösungen', 'Photovoltaik [MWh] Originalauflösungen', 'Sonstige Erneuerbare [MWh] Originalauflösungen']
for column in columns_to_clean:
    renewable_energy_data[column] = renewable_energy_data[column].str.replace(".", "").str.replace(",", ".").replace('-', 0).astype(float)

energy_consumption_data['Gesamt (Netzlast) [MWh] Originalauflösungen'] = energy_consumption_data['Gesamt (Netzlast) [MWh] Originalauflösungen'].str.replace(".", "").str.replace(",", ".").astype(float)

renewable_energy_data['Total Production'] = renewable_energy_data[columns_to_clean].sum(axis=1)
production_by_year = renewable_energy_data.groupby(renewable_energy_data['Datum'].dt.year)['Total Production'].sum()
consumption_by_year = energy_consumption_data.groupby(energy_consumption_data['Datum'].dt.year)['Gesamt (Netzlast) [MWh] Originalauflösungen'].sum()

production_by_type_and_year = renewable_energy_data.groupby(renewable_energy_data['Datum'].dt.year)[columns_to_clean].sum()

pd.options.display.float_format = '{:.2f}'.format

data_by_year = {}

for year, data in renewable_energy_data.groupby(renewable_energy_data['Datum'].dt.year):
    production_data = data[columns_to_clean].sum()
    consumption_data = energy_consumption_data[energy_consumption_data['Datum'].dt.year == year]['Gesamt (Netzlast) [MWh] Originalauflösungen']
    total_consumption = consumption_data.sum()
    data_by_year[year] = {'Production': production_data.sum(), 'Consumption': total_consumption, 'Biomasse': production_data['Biomasse [MWh] Originalauflösungen'], 'Wasserkraft': production_data['Wasserkraft [MWh] Originalauflösungen'], 'Wind Offshore': production_data['Wind Offshore [MWh] Originalauflösungen'], 'Wind Onshore': production_data['Wind Onshore [MWh] Originalauflösungen'], 'Photovoltaik': production_data['Photovoltaik [MWh] Originalauflösungen'], 'Sonstige Erneuerbare': production_data['Sonstige Erneuerbare [MWh] Originalauflösungen']}


for year, data in data_by_year.items():
    print(f"Year: {year}")
    print(f"Total Renewable Energy Production: {data['Production']} MWh")
    print(f"Total Consumption: {data['Consumption']} MWh")
    print(f"Biomasse: {data['Biomasse']} MWh")
    print(f"Wasserkraft: {data['Wasserkraft']} MWh")
    print(f"Wind Offshore: {data['Wind Offshore']} MWh")
    print(f"Wind Onshore: {data['Wind Onshore']} MWh")
    print(f"Photovoltaik: {data['Photovoltaik']} MWh")
    print(f"Sonstige Erneuerbare: {data['Sonstige Erneuerbare']} MWh")
    print()



total_renewable_production = renewable_energy_data[columns_to_clean].sum(axis=1)
total_consumption = energy_consumption_data['Gesamt (Netzlast) [MWh] Originalauflösungen']

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






"""
# Wie kann man zu den Daten oben zugreifen
consumption_2021 = data_by_year[2021]['Consumption']
print(f"Total energy consumption in 2021: {consumption_2021} MWh")
"""

end_time = time.time()                         # The time at the end of the program is stored
duration = end_time - start_time               # Duration of the program is calculated
print("Duration", duration)