import xml.etree.ElementTree as ET
import sys
import requests

def parseXML(xmlfile, splunk_ip, token, srctype):
    trip_name = xmlfile[4:-4]
    trip_name = trip_name[0:trip_name.index(',')+6].replace('_','-').replace(',','') + ' ' + trip_name[trip_name.index(',')+7:-3].replace('_',':') + trip_name[-2:]
  
    # create element tree object
    tree = ET.parse(xmlfile)
  
    # get root element
    root = tree.getroot()
  
    # iterate news items
    for item in root.findall('./trk/trkseg/trkpt'):
  
        # empty news dictionary
        news = {}
    
        # iterate child elements of item
        for child in item:
  
            # special checking for namespace object content:media
            if child.tag == 'extensions':
                for grandchild in child:
                    news['s'] = grandchild.attrib['s']
                    try:
                        news['c'] = grandchild.attrib['c']
                    except:
                        news['c'] = '0'
            else:
                news[child.tag] = child.text

        news['trip'] = trip_name
  
        requests.post('http://'+splunk_ip+':8088/services/collector/raw?sourcetype='+srctype, headers={'Authorization': 'Splunk '+token}, json=news)

    meta_dict = {}
    for item in root.findall('./trk/extensions'):
        for child in item:
            for grandchild in child:
                if grandchild.tag == 'creationtime':
                    meta_dict['time'] = grandchild.text
                else:    
                    meta_dict[grandchild.tag] = grandchild.text
    meta_dict['trip'] = trip_name
    requests.post('http://'+splunk_ip+':8088/services/collector/raw?sourcetype='+srctype, headers={'Authorization': 'Splunk '+token}, json=meta_dict)
    print(meta_dict)

def cleanXML(filename):
    with open(filename) as fin, open('New_'+filename, "w+") as fout:
        for line in fin:
            line = line.replace("xmlns=\"http://www.topografix.com/GPX/1/1\" ", "")
            fout.write(line)
    return 'New_'+filename

      
file_inputs = sys.argv
for file_input in file_inputs[1:]:
    # clean xml file
    new_file = cleanXML(file_input)
    # parse xml file
    parseXML(new_file, 'SPLUNK_IP', 'HEC_TOKEN', 'geotracker')