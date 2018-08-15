import config
import json
import os
import parameters

IMPORTER = config.IMPORTER()
IMPORTER_PARAMETER = parameters.IMPORTER()
SCRAPER = config.SCRAPER()
SCRAPER_PARAM = parameters.SCRAPER_PARAM()
SPLITTER = parameters.SPLITTER()

class Splitter():
  def splitFile(self):
    with open(IMPORTER.DICTIONARY_FILE_NAME + IMPORTER_PARAMETER.FILE_TYPE, encoding = SCRAPER_PARAM.ENCODING) as json_file:
      data = json.load(json_file)
    if not os.path.exists(SCRAPER.FOLDER):
      os.makedirs(SCRAPER.FOLDER)
    i = 0
    while i < len(data):
      fileName = data[i]["fields"]["name"]["value"]
      fileList = data[i]["fields"]["sessions"]
      j = 0
      while j < len(fileList):
        f = open(SCRAPER.FOLDER + fileName + SPLITTER.FILE_SEPARATOR + str(j) + SPLITTER.FILE_TYPE, SPLITTER.FILE_OPEN_MODE, encoding = SPLITTER.ENCODING)
        f.write(json.dumps(fileList[j]))
        f.close()
        j += 1
      i += 1