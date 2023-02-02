import pandas as pd
import pvlib


poa_data_2015, meta, inputs = pvlib.iotools.get_pvgis_hourly(latitude=40.2016504, longitude=-76.7354743, 
                    start=2015, end=2015, raddatabase="PVGIS-NSRDB", components=True,
                    surface_tilt=45, surface_azimuth=0, outputformat='json',
                    usehorizon=True, userhorizon=None, pvcalculation=False, 
                    peakpower=None, pvtechchoice='crystSi', mountingplace='free',
                    loss=0, trackingtype=0, optimal_surface_tilt=False, optimalangles=False,
                    url='https://re.jrc.ec.europa.eu/api/', map_variables=True, timeout=30)


poa_data_2015['poa_diffuse'] =  poa_data_2015['poa_sky_diffuse'] + poa_data_2015['poa_ground_diffuse']
poa_data_2015['poa_global'] = poa_data_2015['poa_diffuse'] + poa_data_2015['poa_direct']

# poa_data_2015.index = pd.to_datetime(poa_data_2015.index, format='%Y%m%d:%H%M')

# print(poa_data_2015)
poa_data_2015.to_csv('poa_data_2015_io.csv')