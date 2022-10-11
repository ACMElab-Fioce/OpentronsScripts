def get_values(*names):
    import json
    _all_values = json.loads("""{"num":1, "p20_mount":"right"}""")
    return [_all_values[n] for n in names]

from opentrons import protocol_api
import math


# metadata
metadata = {
    'protocolName': 'Teste mix',
    'author': 'Suzana Almeida <suzana.almeida@fiocruz.br>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.7'
}


def run(ctx: protocol_api.ProtocolContext):

    [num, p20_mount] = get_values(  # noqa: F821
        'num', 'p20_mount')
   

    # Variables; these are injected when downloaded from the protocol
    # Library. Listed here for ease of access.
    
    num_samps = int(num)  # should be int, 1
    
    
        
    # labware

    temperature_module = ctx.load_module('Temperature Module', 3)
    source_plate = temperature_module.load_labware('opentrons_24_aluminumblock_generic_2ml_screwcap', 'Reagents')
    
    tc_module = ctx.load_module('Thermocycler Module')
    destination_plate = tc_module.load_labware(
        'nest_96_wellplate_100ul_pcr_full_skirt','Final Plate')
    
    # samples_plate = ctx.load_labware ('nest_96_wellplate_200ul_flat', 5, 'Normalized samples')

    tiprack20 = [
        ctx.load_labware('opentrons_96_tiprack_20ul', slot, '20ul tiprack')
        for slot in ['4']
    ]
    # pipettes
    p20 = ctx.load_instrument(
        'p20_single_gen2', p20_mount, tip_racks=tiprack20)

 

    # parse

    agua = source_plate['A1']
    ctx.comment('Place the Agua in position 3 of the deck in well A1')
    buffer = source_plate['B1']
    ctx.comment('Place the Buffer in position 3 of the deck in well B1')

    # set temperatures
    temperature_module.set_temperature(4)
    temperature_module.status
    
    tc_module.open_lid()
    tc_module.set_block_temperature(4)
    tc_module.lid_position
    tc_module.block_temperature_status


    # Create variables based on the number of samples
    num_cols = math.ceil(int(num_samps/8))

    source_plate_wells = source_plate.wells()[:num_samps]
    source_plate_cols = source_plate.rows()[0][:num_cols]

    destination_plate_wells = destination_plate.wells()[:num_samps]
    destination_plate_cols = destination_plate.rows()[0][:num_cols]

    #samples_plate_wells= samples_plate.wells()[:num_samps]
    #samples_plate_cols = samples_plate.rows()[0][:num_cols]

    
    volenzymaticmix= 15
    p20.pick_up_tip()
    # p20.mix(10, 20, agua)
    p20.blow_out()
    p20.drop_tip()
    p20.transfer(volenzymaticmix,agua,destination_plate_wells, new_tip='always')

    volfinal= 20
    p20.pick_up_tip()
    p20.blow_out()
    p20.drop_tip()
    p20.transfer(volfinal,buffer,destination_plate_wells, new_tip='always')
    
    # ctx.comment('Seal the plate on the Thermocycler')

    tc_module.close_lid()
    tc_module.open_lid()

    print("AAAAA")
    
    ctx.comment('Hello World')
    ctx.comment('Você conseguiu!')