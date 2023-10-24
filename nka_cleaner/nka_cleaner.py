#run the script with all .nka files that needs to be cleaned as arguments
#the script will remove all data from the .nka file and keep only the first line and the new line
import sys

txt_files = sys.argv[1:]

for txt_file in txt_files:
    with open(txt_file, 'r') as file:
        first_line = file.readlines()
        first_line = first_line[:1]
    with open(txt_file, 'w') as file:
        file.writelines(first_line)
