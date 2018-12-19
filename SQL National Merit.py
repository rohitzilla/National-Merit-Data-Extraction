import csv
import PyPDF2
import re

femaleNameCount = {}
maleNameCount = {}

def readTextFiles(gender):
    list = []
    for i in range(2017, 2018):
        input = open("yob" + str(i) + ".txt", "r")  # Text file of census data of names
        for line in input:
            text = line.split(",")
            if text[1] == gender:
                list.append(text[0])
                if gender == "M":
                    maleNameCount[text[0]] = maleNameCount.get(text[0], 0) + int(text[2])
                else:
                    femaleNameCount[text[0]] = femaleNameCount.get(text[0], 0) + int(text[2])
    return list


years = [2017, 2018, 2019]

maleNames = readTextFiles("M")
femaleNames = readTextFiles("F")

with open("national_merit.csv", mode="w") as csv_file:  # csv file that data will be written to
    writer = csv.writer(csv_file, delimiter = ",")
    writer.writerow(["Last Name", "First Name", "Gender", "Year", "School"])
    for year in years:
        currentSchool = ""
        nextSchool = ""
        file = open("nationalmerit" + str(year) + ".pdf", 'rb')  # Pdfs of names
        fileReader = PyPDF2.PdfFileReader(file)
        for i in range(2, fileReader.getNumPages()):
            page = fileReader.getPage(i)
            text = page.extractText()
            text = re.sub("[0123456789]", "\n", text)
            text = re.sub(r"([A-Z]+[A-Z]+ *)", r" \1", text)
            text = re.sub(" +", " ", text)
            text = re.sub(r"\n+", "\n", text)
            for full_name in text.split("\n"):
                name = ""
                if ("," in full_name or text.split("\n").index(full_name) == 2) and len(full_name) > 2:
                    school = re.search("[A-Z]+[A-Z]+", full_name)
                    if i == 2 and text.split("\n").index(full_name) == 2:
                        currentSchool = re.sub(r"\b([A-Z]+)\s*\1\b", r"\1", full_name.lstrip(" "))
                    elif school != None:
                        nextSchool = str(full_name[full_name.find(school.group(0)):])
                        nextSchool = re.sub(r"\b([A-Z]+)\s*\1\b", r"\1", nextSchool)
                        name = full_name[:full_name.find(currentSchool)]
                    else:
                        currentSchool = nextSchool
                    name = full_name[full_name.find(",") + 2:]
                    name = re.sub(r" [A-Za-z]+[.]*", "", name)
                    name = re.sub(r"['-.&:]", " ", name)
                    name = name.rstrip(" ")
                    if name in maleNames and (name not in femaleNames or maleNameCount[name] > femaleNameCount.get(name, 0)):
                        writer.writerow([full_name[:full_name.find(",")], name] + ["M", year, currentSchool])
                    elif name in femaleNames and (name not in maleNames or femaleNameCount[name] > maleNameCount.get(name, 0)):
                        writer.writerow([full_name[:full_name.find(",")], name] + ["F", year, currentSchool])
                    elif "," in full_name:
                        writer.writerow(
                            [full_name[:full_name.find(",")], name] + ["N/A", year, currentSchool])
