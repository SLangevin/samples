import os
import json
import parameters
import pusher
import config
import datetime

SCRAPER_PARAM = parameters.SCRAPER_PARAM()
SCRAPER = config.SCRAPER()

class Scraper():
    # Loop through all the .json files of a local folder    
    def pushAllDocs(self):
        root = SCRAPER.FOLDER
        filetype = SCRAPER_PARAM.FILE_TYPE
        for filename in os.listdir(root):
            if filename.endswith(filetype):
                file = open(root + filename, encoding = SCRAPER_PARAM.ENCODING)
                jsonFile = json.loads(file.read())
                convertedJSON = self.convertJSON(jsonFile, filename)
                loadedJSON = json.loads(convertedJSON)
                pusher.Pusher.pushDocument(loadedJSON, loadedJSON[SCRAPER_PARAM.UNIQUE_DOCUMENT_ID_NODE])
                file.close()
    
    def convertJSON(self, jsonfile, filename):
        data = {}
        track = filename.split("_")[0]
        speakersName = [jsonfile['fields']['speakerName']['value']]
        speakersTitle = [jsonfile['fields']['speakerTitle']['value'].replace('<br/>','')]
        
        #Super dirty workaround for Martina, Altola, The Bernt Group and Avanade
        if(jsonfile['fields']['speakerTitle']['value'].split(",")[-1] == 'Programmer Writer'):
            speakersCo = ['Sitecore']
        elif(jsonfile['fields']['speakerTitle']['value'].split(",")[-1] == ' Inc.'):
            speakersCo = ['Altola']   
        elif(jsonfile['fields']['speakerTitle']['value'].split(",")[-1] == ' Ltd.'):
            speakersCo = ['The Berndt Group']
        elif(jsonfile['fields']['speakerTitle']['value'].split(",")[-1] == 'Group Manager at Avanade'):
            speakersCo = ['Avanade']
        else:
            speakersCo = [jsonfile['fields']['speakerTitle']['value'].replace('<br/>','').split(",")[-1]]

        #Not pretty support for multiple speakers
        if 'speaker2Name' in jsonfile['fields']:
           speakersName.append(jsonfile['fields']['speaker2Name']['value'])
           speakersTitle.append(jsonfile['fields']['speaker2Title']['value'].replace('<br/>',''))
           #Terrible workaround for Avanade
           if(jsonfile['fields']['speaker2Title']['value'].split(",")[-1] == 'Group Manager at Avanade'):
               speakersCo.append('Avanade')
           else:
               speakersCo.append(jsonfile['fields']['speaker2Title']['value'].replace('<br/>','').split(",")[-1])
        if 'speaker3Name' in jsonfile['fields']:
           speakersName.append(jsonfile['fields']['speaker3Name']['value'])
           speakersTitle.append(jsonfile['fields']['speaker3Title']['value'].replace('<br/>',''))
           speakersCo.append(jsonfile['fields']['speaker3Title']['value'].replace('<br/>','').split(",")[-1])

        data = {'author' : 'Sitecore Symposium', 
          'documenttype' : 'Text',
          'filename' : filename,
          'language' : 'English',
          'sourcetype' : 'Push',
          'title' : jsonfile['fields']['title']['value'],
          'fileExtension' : SCRAPER_PARAM.FILE_TYPE,
          'data' : jsonfile['fields']['description']['value'],
          'documentId' : 'file://' + filename,
          'speakers' : speakersName,
          'speakerstitle' : speakersTitle,
          'speakersco' : speakersCo,
          'track' : track
        }
        json_data = json.dumps(data)
        return json_data

        