import pvlib
import pandas as pd
from pvlib.location import Location
import matplotlib.pyplot as plt

nittany_place = Location(latitude=40.2016504, longitude= -76.7354743, altitude=117.8531643, tz= 'America/New_York', name='Nittany Place')

celltype = 'monoSi'
pdc0 = 400
v_mp = 44.1
i_mp = 9.08
v_oc = 53.4
i_sc = 9.60
alpha_sc = 0.0005 * i_sc
beta_voc = -0.0029 * v_oc
gamma_pdc = -0.37
cells_in_series = 6*27
temp_ref = 25

surface_tilt=45

surface_azimuth=180

start="2015-08-16 00:00"
end="2015-08-23 23:00"

poa_data_2015 = pd.read_csv('poa_data.csv', index_col=0)
poa_data_2015.index = pd.date_range(start= "2015-01-01 00:00",
                                    periods = len(poa_data_2015.index),
                                    freq='h')

poa_data = poa_data_2015[start:end]

solar_position = nittany_place.get_solarposition(times=pd.date_range(start= start, end= end, freq='h'))

angle_of_incidence = pvlib.irradiance.aoi(
    surface_tilt, surface_azimuth, solar_position.apparent_zenith, solar_position.azimuth)

# incident angle modifier
iam = pvlib.iam.ashrae(angle_of_incidence)

effective_irradiance = poa_data['poa_direct'] * iam + poa_data['poa_diffuse']

temp_cell = pvlib.temperature.faiman(poa_data['poa_global'], poa_data['temp_air'],
                                        poa_data['wind_speed'])

# calculate dc output of module
result_dc = pvlib.pvsystem.pvwatts_dc(effective_irradiance,
                                        temp_cell,
                                        pdc0,
                                        gamma_pdc,
                                        temp_ref)

result_dc.plot(figsize=(16,9))
plt.title('DC Output Power')
plt.show()

results_ac = pvlib.inverter.pvwatts(pdc = result_dc,
                                    pdc0=500,
                                    eta_inv_nom=0.961,
                                    eta_inv_ref=0.9637)

results_ac.plot(figsize=(16,9))
plt.title('AC Output Power')
plt.show()