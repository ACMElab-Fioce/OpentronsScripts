# %%
from opentrons import protocol_api
import pandas as pd

# %%
# Falta incluir qual o número de placa
df = pd.read_csv("../rendimento_primers_idt.csv", sep=';')
df_filtrado = df[['Sequence Name', 'nmoles','Well Position']]
df_filtrado['nmoles_numero'] = df_filtrado['nmoles'].apply(lambda x: x.strip("nmoles"))
df_filtrado['volume_normalizar'] = df_filtrado['nmoles_numero'].apply(lambda x: float(x)*10)
df_filtrado['well_position_opentrons'] = df_filtrado['Well Position'].apply(lambda x: x if list(x)[1] != '0' else "".join([list(x)[0], list(x)[2]]))
df_filtrado

# %%
# Metadados
metadata = {
    'protocolName': 'Transferencia de tubo para placa',
    'author': 'Equipe de bioinformática ACMELab Fiocruz CE - Cleber Aksenen e Pedro Miguel',
    'description': 'Preparo de mastermix de conversões para cDNA',
    'apiLevel': '2.13'
}

def run(protocol: protocol_api.ProtocolContext):
    tubo = protocol.load_labware('opentrons_10_tuberack_nest_4x50ml_6x15ml_conical', location='4')
    # placa1 = protocol.load_labware('appliedbiosystems_96_wellplate_200ul', location='6')
    placa1 = protocol.load_labware('biorad_96_wellplate_200ul_pcr', location='6')
    
    tiprack_1000 = protocol.load_labware('opentrons_96_filtertiprack_1000ul', location='7')
    #tiprack_20 = protocol.load_labware('opentrons_96_filtertiprack_20ul', location='7')

    # Pipetas
    left_pipette = protocol.load_instrument(
         'p1000_single_gen2', mount='left', tip_racks=[tiprack_1000])
    #right_pipette = protocol.load_instrument(
         #'p20_single_gen2', mount='right', tip_racks=[tiprack_20])
    
    #Comandos
    pocos = df_filtrado['well_position_opentrons'].tolist()
    volumes = df_filtrado['volume_normalizar'].tolist()


    for poco, volume in zip(pocos[:96], volumes[:96]):
        left_pipette.pick_up_tip()
        left_pipette.aspirate(volume, tubo["A3"], )
        left_pipette.dispense(volume, placa1[poco])
        left_pipette.drop_tip()
# %%
