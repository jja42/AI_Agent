# from subdirectory.filename import function_name
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

### FILE INFO

#print(get_files_info("calculator", "."))

#print(get_files_info("calculator", "pkg"))

#print(get_files_info("calculator", "/bin"))

#print(get_files_info("calculator", "../"))


### FILE CONTENT

#print(get_file_content("calculator", "lorem.txt"))

#print(get_file_content("calculator", "main.py"))

#print(get_file_content("calculator", "pkg/calculator.py"))

#print(get_file_content("calculator", "/bin/cat"))


### WRITE FILES
 
#print(write_file("calculator", "lorems.txt", "wait, this isn't lorem ipsum"))

#print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))

#print(write_file("calculator", "notreal/text.txt", "this folder and file didn't exist earlier"))

#print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))


#### RUN FILES
print(run_python_file("calculator", "main.py", "3 + 5"))

print(run_python_file("calculator", "tests.py"))

print(run_python_file("calculator", "../main.py"))

print(run_python_file("calculator", "nonexistent.py"))