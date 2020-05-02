import tarfile
import os
import argparse

def parse_cmd_line():
  parser = argparse.ArgumentParser(add_help=False, usage=None)
  parser.add_argument('--mode', type=str, default="c")
  args = parser.parse_args()
  if ((args.mode != "c") & (args.mode != "s")):
    print("Please select either \"c\" or \"s\" when setting --mode. Aborting.")
    return -1
  return args.mode

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
  write_file_2 = open("feedback_2.txt", "w+")
  print("Files \"grades.txt\" and \"feedback_2.txt\" were created.")
  name_perm = read_file.readline()
  while name_perm:
    write_file_2.write(name_perm)
    total_score = 0
    read_file.readline()
    while True:
      score_line = read_file.readline()
      if score_line[:8] != "Question":
        break
      feedback = read_file.readline() # Feedback
      if (feedback.split(":")[1] != "\n"):
        write_file_2.write((" ").join(score_line.split(" ")[0:2]) + ":")
        write_file_2.write((":").join(feedback.split(":")[1:]))
      read_file.readline() # Blank
      total_score += int(score_line.split(": ")[-1])
    write_file.write(name_perm.split(" ")[0] + " " + str(total_score) + " " + str(possible_points) + " " + (" ").join(name_perm.split(" ")[1:]))
    write_file_2.write("Total: " + str(total_score) + "/" + str(possible_points) + "\n\n")
    if total_score == 0:
      print("It appears that " + name_perm[:-1] + " did not submit.")
    name_perm = read_file.readline()

if __name__ == '__main__':
  mode = parse_cmd_line()
  if mode == "c":
    set_working_dir()
    print("Create mode.")
    mass_extract()
    generate_template_feedback_file(10)
  elif mode == "s":
    set_working_dir()
    print("Score mode.")
    calculate_write_scores(100)
