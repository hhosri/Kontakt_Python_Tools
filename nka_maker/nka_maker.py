import os
import sys
import glob
import csv

#--------------------------------------GLOBAL-------------------------------------
script_directory    = os.path.dirname(os.path.realpath(__file__))
nka_folder          = os.path.join(script_directory, '../Resources/data/')
success_files       = 0
delimiter_char      = ';'

#--------------------------------------CLASSES------------------------------------
#a class that holds info about the .nka file (name, type, content...)
class NkaFile:
    def __init__(self, csv_filename):
        self.csv_filename = csv_filename
        self.column_title = ''
        self.column_type = ''

        self.nka_arr_name = ''
        self.nka_file_name = ''
        self.first_line = ''

        self.values = []

    def generate_nka_arr_name(self):
        return (self.csv_filename + '_' + self.column_title)
    
    def generate_nka_file_name(self):
        return (self.nka_arr_name + '.nka')
    
    def generate_first_line(self):
        if self.column_type == "#text":
            return "!" + self.nka_arr_name
        elif self.column_type == "#numbers":
            return "%" + self.nka_arr_name
        else:
            return ""

#--------------------------------------FUNCTIONS----------------------------------
#handles error/success messages
def exit_message_status(message, success):
    RESET = "\033[0m"
    GREEN = "\033[32m"
    RED = "\033[31m"
    if success == 1:
        print(GREEN + message + RESET)
    else:
        print(RED + message + RESET)
        sys.exit()

#checks if column type is valid or not
def type_checker(type, column_text, file):
    if type not in ["#numbers", "#text", "#none"]:
        exit_message_status(f'The type: "{type}" of the "{column_text}" column, in the file "{file}.csv" is not a valid type, please use one of the following types:\n- #text \n- #numbers \n- #none', 0)

#checks if entered command line arguments are valid and existing .csv files
def check_args_format_existence(csv_files_list):
    existing_csv_files = []
    for csv_file in csv_files_list:
        if os.path.isfile(csv_file) and csv_file.lower().endswith(".csv"):
            existing_csv_files.append(csv_file)
        else:
            exit_message_status(f"{csv_file} is either not a .csv file, or doesn't exist in the current directory", 0)

#collects all .csv files needed and stores them in a list after validation
def process_arguments():
    if len(sys.argv) <= 1:
        exit_message_status("No .csv files entered as arguments to process", 0)
    elif sys.argv[1] == "all":
        csv_files_with_path = glob.glob(os.path.join(script_directory, '*.csv'))
        if len(csv_files_with_path) == 0:
            exit_message_status("No .csv files found in the current folder to process", 0)
        else:
            csv_files_list = [os.path.basename(csv_file) for csv_file in csv_files_with_path]
    else:
        csv_files_list = sys.argv[1:]
        check_args_format_existence(csv_files_list)
    return (csv_files_list)

#extracts data from .csv file and stores it in a list of lists
def csv_data_list_maker(file):
    with open(file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = delimiter_char)
        num_columns = len(next(csv_reader))
        csv_file.seek(0)

        columns_data_list = [[] for _ in range(num_columns)]
        for line in csv_reader:
            for i in range(num_columns):
                columns_data_list[i].append(line[i])
    return(columns_data_list)

#assigns to each object the corresponing information extracted from the .csv
def populate_objs(nka_obj_list, columns_data_list):
    for i, column in enumerate(columns_data_list):
        column_text = column[0].split()
        nka_obj_list[i].column_title = column_text[0]
        nka_obj_list[i].column_type = column_text[1]
        type_checker(nka_obj_list[i].column_type, column[0], nka_obj_list[i].csv_filename)

        nka_obj_list[i].values = column[1:]

        nka_obj_list[i].nka_arr_name = nka_obj_list[i].generate_nka_arr_name()
        nka_obj_list[i].nka_file_name = nka_obj_list[i].generate_nka_file_name()
        nka_obj_list[i].first_line = nka_obj_list[i].generate_first_line()

    return(nka_obj_list)

#creates an object for each .nka file to be generated
def nka_obj_list_maker(file, columns_data_list):
    nka_obj_list = []
    with open(file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        num_columns = len(next(csv_reader))
        csv_file.seek(0)
        for _ in range(num_columns):
            new_nka_obj = NkaFile(csv_filename=os.path.splitext(file)[0])
            nka_obj_list.append(new_nka_obj)
    nka_obj_list = populate_objs(nka_obj_list, columns_data_list)
    return (nka_obj_list)

#generates the nka files
def generate_nka_files(nka_obj_list):
    for obj in nka_obj_list:
        if obj.column_type != "#none":
            with open(nka_folder + obj.nka_file_name, 'w') as file:
                file.write(obj.first_line)
            with open(nka_folder + obj.nka_file_name, 'a') as file:
                for value in obj.values:
                    file.write('\n')
                    file.write(value)
                file.write('\n')

#--------------------------------------Main-------------------------------------

csv_files_list = process_arguments()
for file in csv_files_list:
    columns_data_list = csv_data_list_maker(file)
    nka_obj_list = nka_obj_list_maker(file, columns_data_list)
    generate_nka_files(nka_obj_list)
    success_files += 1

exit_message_status(f'*** {success_files} .CSV files converted succesfully ***', 1)

#-------------------------------------------------------------------------------

