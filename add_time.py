import xml.etree.ElementTree as ET
import sys
import os

def convert_mi(mi):
    return mi*1609.344

def convert_min(min):
    return min*60*1000

def changeXML(xmlfile, miles, minutes):
    # convert arg units
    miles = float(miles)
    minutes = float(minutes)

    # create element tree object
    tree = ET.parse(xmlfile)

    # get root element
    root = tree.getroot()

    meta_dict = {}
    for item in root.findall('./trk/extensions'):
        for child in item:
            for grandchild in child:
                if grandchild.tag == 'length':
                    # get original length
                    old_len = float(grandchild.text)
                    # convert additional length from miles to meters
                    new_len = str(old_len+convert_mi(miles))
                    # set new length
                    grandchild.text = new_len
                    print(new_len)
                elif grandchild.tag == 'duration':
                    # get original duration
                    old_dur = float(grandchild.text)
                    # convert additional duration from minutes to milliseconds
                    new_dur = str(old_dur+convert_min(minutes))
                    # set new duration
                    grandchild.text = new_dur
                    print(new_dur)
    
    # remove "New_"+filename
    os.remove(xmlfile)

    # overwrite original file
    tree.write(xmlfile[4:])

def cleanXML(filename):
    with open(filename) as fin, open('New_'+filename, "w+") as fout:
        for line in fin:
            line = line.replace("xmlns=\"http://www.topografix.com/GPX/1/1\" ", "")
            fout.write(line)
    return 'New_'+filename

params = sys.argv
file_input = params[1]
add_mi = params[2]
add_min = params[3]
print("Adding "+add_mi+" miles and "+add_min+" minutes to "+file_input+"...")

new_file = cleanXML(file_input)
changeXML(new_file, add_mi, add_min)