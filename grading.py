import tarfile
import os

def mass_extract(directory_with_compressed = "."):
  for file in os.listdir(directory_with_compressed):
    if ((file[-3:] == ".gz") | (file[-4:] == ".tar")):
      tar = tarfile.open(file)
      tar.extractall()
      tar.close()
      os.remove(file)

if __name__ == '__main__':
  mass_extract()
