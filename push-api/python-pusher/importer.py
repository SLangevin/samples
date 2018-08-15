import urllib.request
import shutil
import config
import json
import parameters

IMPORTER = config.IMPORTER()
SCRAPER_PARAM = parameters.SCRAPER_PARAM()
IMPORTER_PARAMETERS = parameters.IMPORTER()

class Importer():
  def importFile(self):
    if(IMPORTER.DOWNLOAD_FILE):
      with urllib.request.urlopen(IMPORTER.IMPORT_URL) as response, open(IMPORTER.FILE_NAME + IMPORTER_PARAMETERS.FILE_TYPE, IMPORTER_PARAMETERS.URL_OPEN_MODE) as out_file:
        shutil.copyfileobj(response, out_file)
      dictionaryFile = self.exportDictionary(IMPORTER.FILE_NAME + IMPORTER_PARAMETERS.FILE_TYPE)
      dictionary_file = open(IMPORTER.DICTIONARY_FILE_NAME + IMPORTER_PARAMETERS.FILE_TYPE, IMPORTER_PARAMETERS.FILE_OPEN_MODE, encoding = SCRAPER_PARAM.ENCODING)
      dictionary_file.write(json.dumps(dictionaryFile))
      dictionary_file.close()
  
  def exportDictionary(self, jsonFile):
    with open(jsonFile, encoding = SCRAPER_PARAM.ENCODING) as json_file:
      data = json.load(json_file)
      dictionary = data["placeholders"]["main"][0]["placeholders"]["content"][0]["fields"]["tracks"]
    return dictionary