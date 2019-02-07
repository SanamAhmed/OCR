import requests
import json
import os
from PyPDF2 import PdfFileReader, PdfFileWriter

def ocr_space_file(filename, overlay=False, api_key='<YOUR_API_KEY>', language='eng'):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
        :param filename: Your file path & name.
        :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
        :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
        :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    """

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    m = r.content.decode()
    jsonstr = json.loads(m)
    print(jsonstr["ParsedResults"][0]["ParsedText"])
    

 
def pdf_splitter(path):
    fname = os.path.splitext(os.path.basename(path))[0]
 
    pdf = PdfFileReader(path)
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))
 
        output_filename = '{}_page_{}.pdf'.format(
            fname, page+1)
 
        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)
            
        #Calling the function
        ocr_space_file(filename=output_filename, language='eng')
        
        #printing the names of two files created from pdf
        #print('Created: {}'.format(output_filename))
 
if __name__ == '__main__':
    #Enter the path of your file here
    path = 'test.pdf'
    pdf_splitter(path)