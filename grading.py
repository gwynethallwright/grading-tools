import tarfile
import os

def set_working_dir(absolute_path = None):
  if absolute_path:
    if os.getcwd() != absolute_path:
      os.chdir(absolute_path)

def mass_extract():
  num_files = 0
  for file in os.listdir("."):
    if ((file[-3:] == ".gz") | (file[-4:] == ".tar")):
      tar = tarfile.open(file)
      tar.extractall()
      tar.close()
      num_files += 1
      os.remove(file)
  print("Number of extractions performed: " + str(num_files) + ".")

def generate_template_feedback_file(num_questions = 10, names_perms_file = "names_perms.txt"):
  if os.access("feedback.txt", os.F_OK):
    print("File \"feedback.txt\" already exists. Aborting.")
    return
  if os.access(names_perms_file, os.F_OK) != True:
    print("File \"" + names_perms_file + "\" does not exist. Aborting.")
    return
  write_file_feedback = open("feedback.txt", "w+")
  read_file = open(names_perms_file, "r+")
  for line in read_file:
    line = line.split(" ")
    write_file_feedback.write(line[0] + " " + (" ").join(line[1:]) + "\n")
    for num in range(1, num_questions+1):
      write_file_feedback.write("Question " + str(num) + " Score:\n")
      write_file_feedback.write("Feedback:\n\n")
    write_file_feedback.write("\n")
  write_file_feedback.close()
  read_file.close()

def calculate_write_scores(possible_points):
  if (os.access("feedback.txt", os.F_OK) == False):
    print("File \"feedback.txt\" does not exist. Aborting.")
    return
  read_file = open("feedback.txt", "r+")
  write_file = open("grades.txt", "w+")
  name_perm = read_file.readline()
  while name_perm:
    total_score = 0
    read_file.readline()
    while True:
      score_line = read_file.readline()
      if score_line[:8] != "Question":
        break
      read_file.readline() # Feedback
      read_file.readline() # Blank
      total_score += int(score_line.split(": ")[-1])
    write_file.write(name_perm.split(" ")[0] + " " + str(total_score) + " " + str(possible_points) + " " + (" ").join(name_perm.split(" ")[1:]))
    name_perm = read_file.readline()
  print("File \"grades.txt\" with scores created.")

if __name__ == '__main__':
  set_working_dir()
  mass_extract()
  generate_template_feedback_file(10)
  # calculate_write_scores(60)
