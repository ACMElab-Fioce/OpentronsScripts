from opentrons import protocol_api

# Metadados
metadata = {
    'protocolName': 'Transferencia de placa para placa',
    'author': 'Equipe de bioinformática ACMELab Fiocruz CE - Cleber Aksenen e Pedro Miguel',
    'description': 'Preparo de mastermix de conversões para cDNA',
    'apiLevel': '2.13'
}

def run(protocol: protocol_api.ProtocolContext):
    placa1 = protocol.load_labware('biorad_96_wellplate_200ul_pcr', location='4')

    placa2 = protocol.load_labware('appliedbiosystems_96_wellplate_200ul', location='6')
    
    #tiprack_1000 = protocol.load_labware('opentrons_96_filtertiprack_1000ul', location='2')
    tiprack_20 = protocol.load_labware('opentrons_96_filtertiprack_20ul', location='10')

    # Pipetas
    #left_pipette = protocol.load_instrument(
         #'p1000_single_gen2', mount='left', tip_racks=[tiprack_1000])
    right_pipette = protocol.load_instrument(
         'p20_multi_gen2', mount='right', tip_racks=[tiprack_20])
    
    
    #Comandos
    pocos_volumes = {
    "A1": 10,
    "A2": 10,
    "A3": 10,}

    right_pipette.pick_up_tip()

    for poco, volume in pocos_volumes.items():
        right_pipette.aspirate(volume, placa1[poco], )
        right_pipette.dispense(volume, placa2[poco])
        #right_pipette.drop_tip()
        #right_pipette.pick_up_tip()