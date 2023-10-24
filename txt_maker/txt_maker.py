import os
import sys
import glob
import csv

#--------------------------------------GLOBAL-------------------------------------
script_directory    = os.path.dirname(os.path.realpath(__file__))
txt_folder          = os.path.join(script_directory, '../Resources/pictures/')
success_files       = 0
delimiter_char      = ';'

#--------------------------------------CLASSES------------------------------------
#a class that holds info about the .txt file 
class TxtFile:
    def __init__(self):
        self.txt_filename = ''
        self.alpha = ''
        self.animation_num = 0
        self.horizontal_animation = ''
        self.vertical_resize = ''
        self.horizontal_resize = ''
        self.fix_top = 0
        self.fix_bott = 0
        self.fix_left = 0
        self.fix_right = 0
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
def populate_objs(txt_obj_list, columns_data_list):
    for i in range (1, len(txt_obj_list) + 1):
        for j in range(0, 10):
            if j == 0:
                txt_obj_list[i - 1].txt_filename = columns_data_list[j][i]
            elif j == 1:
                txt_obj_list[i - 1].alpha = columns_data_list[j][i]
            elif j == 2:
                txt_obj_list[i - 1].animation_num = columns_data_list[j][i]
            elif j == 3:
                txt_obj_list[i - 1].horizontal_animation = columns_data_list[j][i]
            elif j == 4:
                txt_obj_list[i - 1].vertical_resize = columns_data_list[j][i]
            elif j == 5:
                txt_obj_list[i - 1].horizontal_resize = columns_data_list[j][i]
            elif j == 6:
                txt_obj_list[i - 1].fix_top = columns_data_list[j][i]
            elif j == 7:
                txt_obj_list[i - 1].fix_bott = columns_data_list[j][i]
            elif j == 8:
                txt_obj_list[i - 1].fix_left = columns_data_list[j][i]
            elif j == 9:
                txt_obj_list[i - 1].fix_right = columns_data_list[j][i]
    return(txt_obj_list)

#creates an object for each .txt file to be generated
def txt_obj_list_maker(file, columns_data_list):
    txt_obj_list = []
    with open(file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        num_rows = 0
        for row in csv_reader:
            num_rows += 1
        for _ in range(num_rows - 1):
            new_txt_obj = TxtFile()
            txt_obj_list.append(new_txt_obj)
    txt_obj_list = populate_objs(txt_obj_list, columns_data_list)
    return (txt_obj_list)

# generates the txt files
def generate_txt_files(txt_obj_list):
    for obj in txt_obj_list:
        with open(txt_folder + obj.txt_filename + ".txt", 'w') as file:
            file.write("Has Alpha Channel: ")
            file.write((obj.alpha).replace(" ", "").lower())
            file.write('\n')

            file.write("Number of Animations: ")
            file.write((obj.animation_num).replace(" ", "").lower())
            file.write('\n')

            file.write("Horizontal Animation: ")
            file.write((obj.horizontal_animation).replace(" ", "").lower())
            file.write('\n')

            file.write("Vertical Resizable: ")
            file.write((obj.vertical_resize).replace(" ", "").lower())
            file.write('\n')

            file.write("Horizontal Resizable: ")
            file.write((obj.horizontal_resize).replace(" ", "").lower())
            file.write('\n')

            file.write("Fixed Top: ")
            file.write((obj.fix_top).replace(" ", "").lower())
            file.write('\n')

            file.write("Fixed Bottom: ")
            file.write((obj.fix_bott).replace(" ", "").lower())
            file.write('\n')

            file.write("Fixed Left: ")
            file.write((obj.fix_left).replace(" ", "").lower())
            file.write('\n')

            file.write("Fixed Right: ")
            file.write((obj.fix_right).replace(" ", "").lower())
            file.write('\n')       

 
#--------------------------------------Main-------------------------------------

csv_files_list = process_arguments()
for file in csv_files_list:
    columns_data_list = csv_data_list_maker(file)
    txt_obj_list = txt_obj_list_maker(file, columns_data_list)
    generate_txt_files(txt_obj_list)
    success_files += len(txt_obj_list)

exit_message_status(f'*** {success_files} .txt files generated succesfully ***', 1)

#-------------------------------------------------------------------------------

