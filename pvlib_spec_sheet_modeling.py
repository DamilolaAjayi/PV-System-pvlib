import pvlib
import pandas as pd
from pvlib.location import Location
from pvlib.pvsystem import PVSystem
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



I_L_ref, I_o_ref, R_s, R_sh_ref, a_ref, Adjust =  pvlib.ivtools.sdm.fit_cec_sam(
        celltype= celltype,
        v_mp = v_mp,
        i_mp = i_mp,
        v_oc = v_oc,
        i_sc = i_sc,
        alpha_sc = alpha_sc,
        beta_voc = beta_voc,
        gamma_pmp = gamma_pdc,
        cells_in_series =  cells_in_series,
        temp_ref = temp_ref)

cec_params = pvlib.pvsystem.calcparams_cec(effective_irradiance, 
                                temp_cell,
                                alpha_sc,
                                a_ref,
                                I_L_ref,
                                I_o_ref,
                                R_sh_ref,
                                R_s,
                                Adjust)

mpp = pvlib.pvsystem.max_power_point(*cec_params, method='newton')

# print(mpp)

# mpp.plot(figsize=(9,4))
# plt.show()

system = PVSystem(modules_per_string=5, strings_per_inverter=1)

dc_scaled = system.scale_voltage_current_power(mpp)
# dc_scaled.plot(figsize=(9,4))
# plt.show()
# calculate dc output of module
# result_dc = pvlib.pvsystem.pvwatts_dc(effective_irradiance,
#                                         temp_cell,
#                                         pdc0,
#                                         gamma_pdc,
#                                         temp_ref)

# result_dc.plot(figsize=(16,9))
# plt.title('DC Output Power')
# plt.show()

results_ac = pvlib.inverter.pvwatts(pdc = dc_scaled.p_mp,
                                    pdc0=2000,
                                    eta_inv_nom=0.961,
                                    eta_inv_ref=0.9637)

# results_ac.plot(figsize=(9,4))
# plt.title('AC Output Power')
# plt.show()
cec_inverters = pvlib.pvsystem.retrieve_sam('CECInverter')

inverter = cec_inverters['ABB__PVI_3_0_OUTD_S_US__208V_']

ac_results = pvlib.inverter.sandia(
                            v_dc = dc_scaled.v_mp,
                            p_dc = dc_scaled.p_mp,
                            inverter = inverter)


ac_results.plot(figsize=(9,4))
plt.title('AC Output Power')
plt.show()