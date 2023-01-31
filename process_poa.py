import pandas as pd

global_2015 = pd.read_csv('pvgis_2015_global.csv', skiprows=8, nrows=8760,
                            index_col=0)

components_2015 = pd.read_csv('pvgis_2015_components.csv', skiprows=8, nrows=8760,
                                index_col=0)

# print(components_2015)

poa_data_2015 = pd.DataFrame(columns=['poa_global', 'poa_direct', 'poa_diffuse', 'temp_air', 'wind_speed'],
                            index=global_2015.index)


poa_data_2015['poa_global'] = global_2015['G(i)']
poa_data_2015['poa_direct'] =  components_2015['Gb(i)']
poa_data_2015['poa_diffuse'] =  components_2015['Gd(i)'] + components_2015['Gr(i)']
poa_data_2015['temp_air'] =  components_2015['T2m']
poa_data_2015['wind_speed'] =  components_2015['WS10m']

poa_data_2015.index = pd.to_datetime(poa_data_2015.index, format='%Y%m%d:%H%M')

poa_data_2015.to_csv('poa_data.csv')