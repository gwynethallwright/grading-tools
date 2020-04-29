import tarfile
import os

def set_working_dir(absolute_path = None):
  if absolute_path:
    if os.getcwd() != absolute_path:
      os.chdir(absolute_path)

def mass_extract():
  for file in os.listdir("."):
    if ((file[-3:] == ".gz") | (file[-4:] == ".tar")):
      tar = tarfile.open(file)
      tar.extractall()
      tar.close()
      os.remove(file)

def generate_blank_grading_file(possible_points = 50, names_perms_file = "names_perms.txt"):
  if os.access(names_perms_file, os.F_OK) != True:
    print("File \"" + names_perms_file + "\" does not exist. Aborting.")
    return
  if os.access("grades.txt", os.F_OK):
    print("File \"grades.txt\" already exists. Aborting.")
    return
  write_file = open("grades.txt", "w+")
  read_file = open(names_perms_file, "r+")
  for line in read_file:
    line = line.split(" ")
    write_file.write(line[0] + " " + str(possible_points) + " " + (" ").join(line[1:]))
  write_file.close()
  read_file.close()

if __name__ == '__main__':
  set_working_dir()
  mass_extract()
  generate_blank_grading_file()
