# used to parse the xml file and edit it
import xml.etree.ElementTree as ET
import os
import json
from pathlib import Path


class XML_Parser:

    def __init__(self, repo_path, branch_name):
        self._repo_path = repo_path
        self._branch_name = branch_name
        self._config = self.fetch_config()

    @property
    def repo_path(self):
        return self._repo_path

    @repo_path.setter
    def repo_path(self, repo_path):
        self._repo_path = repo_path

    @property
    def branch_name(self):
        return self._branch_name

    @branch_name.setter
    def branch_name(self, branch_name):
        self._branch_name = branch_name

    def fetch_config(self):
        path_to_parent = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        print(f"{path_to_parent}")
        path_to_config = os.path.join(
            path_to_parent, 'Config_Files', 'xml_config.json')
        return path_to_config

    @property
    def config(self):
        return self._config

    # gets the files to be edited from the current directory and returns them

    def get_files(self):
        print(f"Repo Path: {self.repo_path}")
        files_to_edit = []

        # lists the files located in the current directory (repo_path)
        files = os.listdir(self.repo_path)

        # opens the json configuration file and loads it to be checked against the files in repo_path
        with open(self.config) as json_data_file:
            json_data = json.load(json_data_file)

        # for each file in the repo_path, the script compares it to each file located in the json file. If they are equal, the file in repo_path
        # is stored and passed to the calling function to be edited
        for file in files:
            for json_file in json_data["files"]:
                if(file == json_file):
                    files_to_edit.append(os.path.join(self.repo_path, file))

        # the directory is changed to to check for more files that need to be edited located deeper in the repo's directory
        # in the "include" subdirectory
        print("Changing Directories: ")
        new_path_string = "include"
        new_path = os.path.join(self.repo_path, new_path_string)
        os.chdir(new_path)

        print(f"New Repo Path: {new_path}")
        new_path_files = os.listdir(new_path)

        # the script compares each file located in the json configuration file to each file in the "include" subdirectory of the repo.
        # if they are equal, the file in the "include" folder is stored and passed to the calling function for editing
        for file in new_path_files:
            for json_file in json_data["files"]:
                if(file == json_file):
                    files_to_edit.append(os.path.join(new_path, file))

        return files_to_edit

    # edits the xml file (if needed) and prints the resulting xml file

    def edit_xml(self, file_name, file_path):
        doc = ET.parse(file_name)
        print(f"File being edited: {file_name}")
        print("Printing from element tree ")
        for project in doc.findall('project'):
            print(project.attrib)

        print("Attempting to edit xml file using argparse and element tree: ")
        for project in doc.findall('project'):
            name = project.get('name')
            if(name == "acm" or name == "corelockr" or name == "Edge2_Web" or name == "extraFiles" or name == "G2_Keys_And_Certs" or name == "iSTAR_App"
                    or name == "iSTAR_Web" or name == "iSTAR-EdgeG2-M4" or name == "jci_data" or name == "Manifests" or name == "meta-jci-app-edge2"
                    or name == "meta-jci-ate-edge2" or name == "meta-jci-bsp-edge2" or name == "meta-jci-distro-edge2" or name == "meta-jci-startup"
                    or name == "meta-jci-web-edge2" or name == "optee_client" or name == "provisioning" or name == "provSD12-uboot" or name == "provSign"
                    or name == "sli_resources" or name == "u-boot-fslc" or name == "Ubuntu_Build" or name == "Ubuntu_OS_Utils"):
                project.set('revision', self.branch_name)
                doc.write(file_path)
            print(project.attrib)

    def make_edits(self):
        files = self.get_files()
        for file in files:
            self.edit_xml(file, Path(file))


class TextParser:
    def test(self):
        file_to_edit = open(r'test_document_to_edit.txt', 'r')
        to_be_changed = "A Storm of Swords"
        change = "Game of Thrones"
        lines = file_to_edit.read()

        lines = lines.replace(to_be_changed, change)

        with open(r'test_document_to_edit.txt', 'w') as file:
            file.write(lines)
            print(f"Replaced {to_be_changed} with {change} in {file_to_edit.name}")

        file_to_edit.close()

    """
    def test(self):
        file_to_edit = open("test_document_to_edit.txt", "r+")
        change = "A Storm of Swords"
        to_be_changed = "Game of Thrones"
        lines = file_to_edit.readlines()

        for line in lines:
            if to_be_changed in line:
                file_to_edit.write(line.replace(to_be_changed, change))
                print(f"Line changed from {to_be_changed} to {change} in {file_to_edit.name}")

        file_to_edit.close()
    """

def main():
    text_parser = TextParser()
    text_parser.test()

if __name__ == "__main__":
    main()



    """
    Below is based on code at bottom, does not work, I think it looks weird
    file_to_edit = open("test_document_to_edit.txt", "r+")
    change = "A Storm of Swords"
    to_be_changed = "Game of Thrones"
    lines = file_to_edit.readlines()

    c = 0
    for line in lines:
        if to_be_changed in line:
            replacement = line.replace(to_be_changed, change)
            lines = replacement
        c += 1

    file_to_edit.truncate(0)
    file_to_edit.writelines(lines)
    print(file_to_edit)
    file_to_edit.close()
    """


"""
One way to accomplish this goal (the way I found to be the most efficient from my quick research on different methods to edit text files in Python):
# Python program to replace text in a file
x = input("enter text to be replaced:")
y = input("enter text that will replace:")
 
# file.txt should be replaced with
# the actual text file name
f = open("file.txt", "r+")
 
# each sentence becomes an element in the list l
l = f.readlines()
 
# acts as a counter to know the
# index of the element to be replaced
c = 0
for i in l:
    if x in i:
 
        # Replacement carries the value
        # of the text to be replaced
        Replacement = i.replace(x, y)
 
        # changes are made in the list
        l = Replacement
    c += 1
 
# The pre existing text in the file is erased
f.truncate(0)
 
# the modified list is written into
# the file thereby replacing the old text
f.writelines(l)
f.close()
print("Text successfully replaced")

"""
