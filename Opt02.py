from opentrons import protocol_api

# Metadados
metadata = {
    'protocolName': 'Transferencia de tubo para placa',
    'author': 'Equipe de bioinformática ACMELab Fiocruz CE - Cleber Aksenen e Pedro Miguel',
    'description': 'Preparo de mastermix de conversões para cDNA',
    'apiLevel': '2.13'
}

def run(protocol: protocol_api.ProtocolContext):
    tubo = protocol.load_labware('opentrons_10_tuberack_nest_4x50ml_6x15ml_conical', location='4')
    placa1 = protocol.load_labware('appliedbiosystems_96_wellplate_200ul', location='6')
    
    #tiprack_1000 = protocol.load_labware('opentrons_96_filtertiprack_1000ul', location='2')
    tiprack_20 = protocol.load_labware('opentrons_96_filtertiprack_20ul', location='7')

    # Pipetas
    #left_pipette = protocol.load_instrument(
         #'p1000_single_gen2', mount='left', tip_racks=[tiprack_1000])
    right_pipette = protocol.load_instrument(
         'p20_single_gen2', mount='right', tip_racks=[tiprack_20])
    
    
    #Comandos
    #Comandos
    pocos_volumes = {
    "A1": 10,
    "B1": 10,
    "C1": 10,
    "D1": 10,
    "E1": 10,
    "F1": 10,
    "G1": 10,
    "H1": 10}

    right_pipette.pick_up_tip()

    for poco, volume in pocos_volumes.items():
        right_pipette.aspirate(volume, tubo[poco])
        right_pipette.dispense(volume, placa1[poco])
    right_pipette.drop_tip()