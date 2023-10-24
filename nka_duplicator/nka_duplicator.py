#This script let's you duplicate a section in the .nka files as many times as you want
#The section starts after the first line and ends at main_part

import sys

main_part       = 3 #number of lines of the main part that you want to duplicate
duplication     = 200 #how many times do you want to duplicate the main part
nka_files       = sys.argv[1:]

for nka_file in nka_files:
    with open(nka_file, 'r') as file:
        all_content = file.readlines()
        first_line = all_content[0:1]
        after_first_line = all_content[1:main_part + 1]
    with open(nka_file, 'w') as file:
        file.writelines(first_line)
        for _ in range(duplication):
            file.writelines(after_first_line)
