from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': 'Mix cDNA',
    'author': 'Equipe de bioinformática ACMELab Fiocruz CE',
    'description': 'Preparo de mastermix de conversões para cDNA',
    'apiLevel': '2.13'
}

row_poco = ["A", "B", "C", "D", "E", "F", "G", "H"]
coluna_poco = list(range(1,13))
pocos = [x + str(i) for i in coluna_poco for x in row_poco]

# protocol run function
def run(protocol: protocol_api.ProtocolContext):
    plate = protocol.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', location='2')
    tiprack = protocol.load_labware('opentrons_96_tiprack_20ul', location='6')
    eppendorf = protocol.load_labware('opentrons_24_aluminumblock_nest_2ml_screwcap', location='3')

    # pipettes
    left_pipette = protocol.load_instrument(
         'p20_single_gen2', mount='right', tip_racks=[tiprack])

    # commands
    #Preparo do mix
    left_pipette.pick_up_tip()
    # pocos = ["A1","B1","C1","D1","E1","F1","G1","H1","A2","B2","C2","D2","E2","F2","G2","H2",
    # "A3","B3","C3","D3","E3","F3","G3","H3","A4","B4","C4","D4","E4","F4","G4","H4","A5","B5",
    # "C5","D5","E5","F5","G5","H5","A6","B6","C6","D6","E6","F6","G6","H6","A7","B7","C7","D7",
    # "E7","F7","G7","H7","A8","B8","C8","D8","E8","F8","G8","H8","A9","B9","C9","D9","E9","F9",
    # "G9","H9","A10","B10","C10","D10","E10","F10","G10","H10","A11","B11","C11","D11","E11","F11",
    # "G11","H11","A12","B12","C12","D12","E12","F12","G12","H12"]
    for poco in pocos:
        left_pipette.aspirate(8.5, eppendorf["A1"])
        left_pipette.dispense(8.5, plate[poco])
    left_pipette.drop_tip()
