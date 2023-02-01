import pvlib

from pvlib.modelchain import ModelChain
from pvlib.location import Location
from pvlib.pvsystem import PVSystem
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS
import pandas as pd
import matplotlib.pyplot as plt

location = Location(latitude=40.2016504, longitude= -76.7354743, altitude=117.8531643, tz= 'America/New_York', name='Nittany Place')

sandia_modules = pvlib.pvsystem.retrieve_sam('SandiaMod')

cec_inverters = pvlib.pvsystem.retrieve_sam('CECInverter')

module = sandia_modules['Canadian_Solar_CS5P_220M___2009_']
# inverter = cec_inverters['ABB__MICRO_0_25_I_OUTD_US_208__208V_']

inverter = cec_inverters['ABB__PVI_3_0_OUTD_S_US__208V_']
temperature_parameters = TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass']

system = PVSystem(surface_tilt=45, surface_azimuth=180,
                    module_parameters=module, inverter_parameters=inverter,
                    temperature_model_parameters=temperature_parameters,
                    modules_per_string = 7, strings_per_inverter=2)

modelchain = ModelChain(system, location)
times = pd.date_range(start="2021-08-16", end="2021-08-23",
                        freq="1min", tz=location.tz)

clear_sky = location.get_clearsky(times)

# clear_sky.plot(figsize=(16,9))
# plt.show()

tmy = pd.read_csv('pvlib_nittany_place.csv', index_col=0)
tmy.index = pd.to_datetime(tmy.index)

modelchain.run_model(tmy)

# modelchain.results.ac.plot(figsize=(16,9)) # ac output of the PV system

# modelchain.results.ac.resample("M").sum().plot(figsize=(16,9))
# plt.show()

# print(inverter)

poa_data_2015 = pd.read_csv('poa_data_2015_io.csv', index_col=0)
poa_data_2015.index = pd.to_datetime(poa_data_2015.index)

modelchain.run_model_from_poa(poa_data_2015)

modelchain.results.ac.plot(figsize=(16,9))
# modelchain.results.ac.resample("M").sum().plot(figsize=(16,9))
plt.show()