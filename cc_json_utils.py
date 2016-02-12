import json
import sys
import cc_data
import cc_dat_utils


default_input_json_file = "data/kchhibbe_cc1.json"
default_output_dat_file = "data/kchhibbe_cc1.dat"

# Reading the JSON data in from the input file
with open(default_input_json_file) as json_file:
    json_data = json.load(json_file)
    #print (json_data)

finalData = cc_data.CCDataFile()



for json_game in json_data:
    level = cc_data.CCLevel()
    level.level_number = json_game["level_number"]
    level.time = json_game["time"]
    level.num_chips = json_game["num_chips"]
    level.upper_layer = json_game["upper_layer"]
    level.lower_layer = json_game["lower_layer"]
    optional_fields = json_game["Optional Fields"]

    for json_field in optional_fields:
        if json_field["type_val"] == 3:
            title = json_field["title"]
            cc_field = cc_data.CCMapTitleField(title)
            level.add_field(cc_field)
        elif json_field["type_val"] == 7:
            hint = json_field["hint"]
            cc_field = cc_data.CCMapHintField(hint)
            level.add_field(cc_field)
        elif json_field["type_val"] == 6:
            password = json_field["password"]
            cc_field = cc_data.CCEncodedPasswordField(password)
            level.add_field(cc_field)
        elif json_field["type_val"] == 10:
            json_monsters = json_field["monsters"]
            cc_monsters = []
            for json_monster in json_monsters:
                x = json_monster[0]
                y = json_monster[1]
                monster_coord = cc_data.CCCoordinate(x,y)
                cc_monsters.append(monster_coord)
                cc_field = cc_data.CCMonsterMovementField(cc_monsters)
            level.add_field(cc_field)
        elif json_field["type_val"] == 5:
            json_machines = json_field["machine"]
            cc_machines = []
            for json_machine in json_machines:
                c = json_machine["button_coord"][0]
                d = json_machine["button_coord"][1]
                a = json_machine["machine_coord"][0]
                b = json_machine["machine_coord"][1]
                machine_control = cc_data.CCCloningMachineControl(c,d,a,b)
                cc_machines.append(machine_control)
                cc_field = cc_data.CCCloningMachineControlsField(cc_machines)
            level.add_field(cc_field)
        elif json_field["type_val"] == 4:
            json_traps = json_field["traps"]
            cc_traps = []
            for json_trap in json_traps:
                c = json_trap["button_coord"][0]
                d = json_trap["button_coord"][1]
                a = json_trap["trap_coord"][0]
                b = json_trap["trap_coord"][1]
                trap_control = cc_data.CCTrapControl(c,d,a,b)
                cc_traps.append(trap_control)
                cc_field = cc_data.CCTrapControlsField(cc_traps)
            level.add_field(cc_field)
    finalData.add_level(level)

print(level)

if len(sys.argv) == 3:
    input_json_file = sys.argv[1]
    output_dat_file = sys.argv[2]
    print("Using command line args:", input_json_file, output_dat_file)
else:
    input_json_file = default_input_json_file
    output_dat_file = default_output_dat_file
    print("Unknown command line options. Using default values:", input_json_file, output_dat_file)


cc_dat_utils.write_cc_data_to_dat(finalData,output_dat_file)
