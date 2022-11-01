from opentrons import protocol_api

# Metadados
metadata = {
    'protocolName': 'Preparo_mix_cDNA_automatizado',
    'author': 'Equipe de bioinformática ACMELab Fiocruz CE - Cleber Aksenen, Pedro Miguel e Suzana Almeida',
    'description': 'Preparo de mastermix de conversões para cDNA',
    'apiLevel': '2.13'
}

# -----------------------------------------------------------------------------------------------------------
# Protocolo e funções
def run(protocol: protocol_api.ProtocolContext):
    plate = protocol.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', location='7')
    tiprack_20 = protocol.load_labware('opentrons_96_filtertiprack_20ul', location='8')
    
    tiprack_1000 = protocol.load_labware('opentrons_96_filtertiprack_1000ul', location='2')
    temperature_module = protocol.load_module('Temperature Module', location = '3')
    eppendorf = temperature_module.load_labware('opentrons_24_aluminumblock_nest_2ml_screwcap')

    # Pipetas
    right_pipette = protocol.load_instrument(
         'p20_single_gen2', mount='right', tip_racks=[tiprack_20])
    right_pipette.flow_rate.aspirate = 15
    right_pipette.flow_rate.dispense = 15
    left_pipette = protocol.load_instrument(
         'p1000_single_gen2', mount='left', tip_racks=[tiprack_1000])


    # -------------------------------------------------------------------------------------------------------
    # Comandos
    #Distribuição do eph3 (primer) para 96 poços
    right_pipette.pick_up_tip()
    pocos = ["A1","B1","C1","D1","E1","F1","G1","H1","A2","B2","C2","D2","E2","F2","G2","H2",
    "A3","B3","C3","D3","E3","F3","G3","H3","A4","B4","C4","D4","E4","F4","G4","H4","A5","B5",
    "C5","D5","E5","F5","G5","H5","A6","B6","C6","D6","E6","F6","G6","H6"]
    #,"A7","B7","C7","D7",
    # "E7","F7","G7","H7","A8","B8","C8","D8","E8","F8","G8","H8","A9","B9","C9","D9","E9","F9",
    # "G9","H9","A10","B10","C10","D10","E10","F10","G10","H10","A11","B11","C11","D11","E11","F11",
    # "G11","H11","A12","B12","C12","D12","E12","F12","G12","H12"]
    for poco in pocos:
        right_pipette.aspirate(8.5, eppendorf["A1"], )
        right_pipette.dispense(8.5, plate[poco])
    right_pipette.drop_tip()

    #Início do módulo de temperatura
    temperature_module.set_temperature(4)
    temperature_module.status

    #Preparo do mix
    # Pegar o fsm
    left_pipette.pick_up_tip()
    left_pipette.aspirate(864, eppendorf['A3'])
    left_pipette.dispense(864, eppendorf['A6'])
    left_pipette.drop_tip()

    # Pegar o rvt
    left_pipette.pick_up_tip()
    left_pipette.aspirate(96, eppendorf['A4'])
    left_pipette.dispense(96, eppendorf['A6'])
    left_pipette.drop_tip()

    # Homogeneizar
    left_pipette.pick_up_tip()
    for c in range (3):
        left_pipette.aspirate(20, eppendorf['A6'])
        left_pipette.dispense(20, eppendorf['A6'])
    left_pipette.drop_tip()

    #Fim do módulo de temperatura
    temperature_module.deactivate()
    temperature_module.status

    protocol.comment("Processo foi finalizado!")