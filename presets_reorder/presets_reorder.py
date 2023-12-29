
# A script to alphabeticaly reorder presets
# *** use this script after removing all empty presets ***
# change presets_num according to the number of presets
# change prefix according to the prefix of the nka preset data files

import os

#Gloval variables
script_dir = os.path.dirname(os.path.abspath(__file__))
Data_folder_path = os.path.join(script_dir, 'Data')
prefix = 'preset'
presets_num = 5
mandatory_nkas = ['presets_names.nka', 'presets_tags.nka']
mandatory_nkas_path = [Data_folder_path + '/' + item for item in mandatory_nkas]

#Classes
class Preset:
    def __init__(self):
        self.position = 0
        self.name = ''
        self.tag = 0
        self.data = []
        self.filename = ''

#Functions
def create_objects():
    objects_list = []
    for i in range(presets_num):
        object = Preset()
        objects_list.append(object)
    return objects_list

def extract_data_from_nka(nka_file):
    lines = []
    with open(nka_file, 'r') as file:
        lines = file.readlines()[1:]
    return lines

def collect_data():
    presets_names = extract_data_from_nka(mandatory_nkas_path[0])
    presets_tags = extract_data_from_nka(mandatory_nkas_path[1])
    return presets_names, presets_tags


def populate_objects(objects_list, presets_names, presets_tags):
    for i in range(presets_num):
        objects_list[i].position = i
        objects_list[i].name = presets_names[i]
        objects_list[i].tag = presets_tags[i]
        objects_list[i].filename = prefix + str(i) + '.nka'
        objects_list[i].data = extract_data_from_nka(Data_folder_path + '/' + objects_list[i].filename)


def sort_presets(objects_list, presets_names, presets_tags):
    sorted_objects_list = sorted(objects_list, key=lambda x: x.name)
    for i, object in enumerate(sorted_objects_list):
        object.position = i
        object.filename = prefix + str(i) + '.nka'
    return sorted_objects_list

def fill_mandatory_nkas(sorted_objects_list):
    with open(mandatory_nkas_path[0], 'w') as file:
        file.write('!presets_names\n')
        for object in sorted_objects_list:
            file.write(object.name)

    with open(mandatory_nkas_path[1], 'w') as file:
        file.write('%presets_tags\n')
        for object in sorted_objects_list:
            file.write(object.tag)

def fill_presets_data_nkas(sorted_objects_list):
    for object in sorted_objects_list:
        with open(Data_folder_path + '/' + object.filename, 'w') as file:
            file.write(f'%{prefix + str(object.position)}\n')
            for line in object.data:
                file.write(line)

def generate_new_nkas(sorted_objects_list):
    fill_mandatory_nkas(sorted_objects_list)
    fill_presets_data_nkas(sorted_objects_list)
    

#Main
def main():
    presets_names, presets_tags = collect_data()
    objects_list = create_objects()
    populate_objects(objects_list, presets_names, presets_tags)
    sorted_objects_list = sort_presets(objects_list, presets_names, presets_tags)
    generate_new_nkas(sorted_objects_list)


if __name__ == "__main__":
    main()