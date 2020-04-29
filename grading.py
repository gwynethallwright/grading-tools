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

def generate_template_files(possible_points = 50, num_questions = 10, names_perms_file = "names_perms.txt"):
  for file_name in ["grades.txt", "feedback.txt"]:
    if os.access(file_name, os.F_OK):
      print("File \"" + file_name + "\" already exists. Aborting.")
      return
  if os.access(names_perms_file, os.F_OK) != True:
    print("File \"" + names_perms_file + "\" does not exist. Aborting.")
    return
  write_file_grades = open("grades.txt", "w+")
  write_file_feedback = open("feedback.txt", "w+")
  read_file = open(names_perms_file, "r+")
  for line in read_file:
    line = line.split(" ")
    write_file_grades.write(line[0] + " " + str(possible_points) + " " + (" ").join(line[1:]))
    write_file_feedback.write(line[0] + " " + (" ").join(line[1:]) + "\n")
    for num in range(1, num_questions+1):
      write_file_feedback.write("Question " + str(num) + " Score:\n")
      write_file_feedback.write("Feedback:\n\n")
    write_file_feedback.write("\n")
  write_file_grades.close()
  write_file_feedback.close()
  read_file.close()

if __name__ == '__main__':
  set_working_dir()
  mass_extract()
  generate_template_files(40, 10)
