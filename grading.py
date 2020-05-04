import tarfile
import os
import argparse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def parse_cmd_line():
  parser = argparse.ArgumentParser(add_help=False)
  parser.add_argument('--mode', type=str, default="c")
  parser.add_argument('--points', type=int, default="60")
  parser.add_argument('--questions', type=int, default="10")
  parser.add_argument('--path', type=str, default=None)
  args = parser.parse_args()
  if ((args.mode != "c") & (args.mode != "s") & (args.mode != "d")):
    print("Please select either \"c\", \"s\" or \"d\" when setting --mode. Aborting.")
    return -1
  if (args.points <= 0):
    print("Please select a nonzero integer when setting --points. Aborting.")
    return -1
  if (args.questions <= 0):
    print("Please select a nonzero integer when setting --questions. Aborting.")
    return -1
  if args.path:
    if not os.path.isdir(args.path):
      print("Your --path does not represent a valid directory. Aborting.")
      return -1
  return [args.mode, args.points, args.questions, args.path]

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

def delete_pdfs():
  num_files = 0
  for file in os.listdir("."):
    if file[-4:] == ".pdf":
      os.remove(file)
      num_files += 1
  print("Number of deletions performed: " + str(num_files) + ".")

def generate_template_feedback_file(num_questions = 10, names_perms_file = "names_perms.txt"):
  if os.access("feedback.txt", os.F_OK):
    print("File \"feedback.txt\" already exists. Aborting.")
    return
  if os.access(names_perms_file, os.F_OK) != True:
    print("File \"" + names_perms_file + "\" does not exist. Aborting.")
    return
  write_file_feedback = open("feedback.txt", "w+")
  print("File \"feedback.txt\" was created.")
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

def create_pdf(name, perm, assignment_number, feedback):
    pdf_document = SimpleDocTemplate("Homework_" + str(assignment_number) + "_" + perm + ".pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    flowables = []
    flowables.append(Paragraph("<b>PHYS129L Homework " + str(assignment_number) + " Feedback</b>", style=styles["Title"]))
    flowables.append(Paragraph("<b>" + name + "</b>", style=styles["Title"]))
    for paragraph in feedback:
      flowables.append(Paragraph(paragraph, style=styles["Normal"]))
    pdf_document.build(flowables)

def write_scores_feedback_pdf(possible_points, assignment_number=5):
  if (os.access("feedback.txt", os.F_OK) == False):
    print("File \"feedback.txt\" does not exist. Aborting.")
    return
  read_file = open("feedback.txt", "r+")
  write_file = open("grades.txt", "w+")
  write_file_2 = open("feedback_2.txt", "w+")
  print("Files \"grades.txt\" and \"feedback_2.txt\" were created.")
  name_perm = read_file.readline()
  while name_perm:
    feedback_list = []
    write_file_2.write(name_perm)
    total_score = 0
    read_file.readline()
    while True:
      score_line = read_file.readline()
      if score_line[:8] != "Question":
        break
      feedback = read_file.readline() # Feedback
      if (feedback.split(":")[1] != "\n"):
        line_1 = (" ").join(score_line.split(" ")[0:2]) + ":"
        line_2 = (":").join(feedback.split(":")[1:])
        write_file_2.write(line_1)
        write_file_2.write(line_2)
        feedback_list.append("<b>" + line_1 + "</b> " + line_2)
      read_file.readline() # Blank
      total_score += int(score_line.split(": ")[-1])
    write_file.write(name_perm.split(" ")[0] + " " + str(total_score) + " " + str(possible_points) + " " + (" ").join(name_perm.split(" ")[1:]))
    write_file_2.write("Total: " + str(total_score) + "/" + str(possible_points) + "\n\n")
    if total_score == 0:
      print("It appears that " + name_perm[:-1] + " did not submit.")
    elif total_score == possible_points:
      print("It appears that " + name_perm[:-1] + " got a perfect score.")
    if feedback_list:
      create_pdf((" ").join(name_perm.split(" ")[1:]), name_perm.split(" ")[0], assignment_number, feedback_list)
    name_perm = read_file.readline()

if __name__ == '__main__':
  [mode, possible_points, number_of_questions, path] = parse_cmd_line()
  if mode == "c":
    set_working_dir(path)
    print("Create mode.")
    mass_extract()
    generate_template_feedback_file(number_of_questions)
  elif mode == "s":
    set_working_dir(path)
    print("Score mode.")
    write_scores_feedback_pdf(possible_points)
  elif mode == "d":
    set_working_dir(path)
    print("Delete mode.")
    delete_pdfs()
