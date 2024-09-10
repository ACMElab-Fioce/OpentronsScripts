# %%
from opentrons import protocol_api
import pandas as pd

# %%
# Falta incluir qual o número de placa
df = pd.read_excel("Plate Specs SO 20466258.xlsx")
codigo_placa = int(input("Digite o código da placa a ser preenchida: "))
while not df['Plate Barcode'].isin([codigo_placa]).any():
    print("Código inválido, tente novamente")
    codigo_placa = int(input("Digite o código da placa a ser preenchida: "))
tmp_df = df[df['Plate Barcode'] == codigo_placa].copy()
df_filtrado = tmp_df[['Sequence Name', 'nmoles','Well Position', 'Plate Barcode']].copy()
df_filtrado['volume_normalizar'] = df_filtrado['nmoles'].apply(lambda x: round(float(x)*10, 1))
df_filtrado['well_position_opentrons'] = df_filtrado['Well Position'].apply(lambda x: x if list(x)[1] != '0' else "".join([list(x)[0], list(x)[2]]))

# %%
# Metadados
metadata = {
    'protocolName': 'Transferencia de tubo para placa',
    'author': 'Equipe de bioinformática ACMELab Fiocruz CE - Cleber Aksenen e Pedro Miguel',
    'description': 'Preparo de mastermix de conversões para cDNA',
    'apiLevel': '2.13'
}

def run(protocol: protocol_api.ProtocolContext):
    # Cheque a posição das placas e o nome das placas
    # Execute antes a simulação
    
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


    for poco, volume in zip(pocos, volumes):
        left_pipette.pick_up_tip()
        left_pipette.aspirate(volume, tubo["A3"], )
        left_pipette.dispense(volume, placa1[poco])
        left_pipette.drop_tip()

