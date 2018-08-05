
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import codecs
import unidecode
import os
import requests
import shutil
import re
from io import StringIO

def download_file(url):
    local_filename = url.split('/')[-1]
    local_filename = local_filename.replace("%20", "_")
    r = requests.get(url, stream=True)
    print(r)
    with open(local_filename, 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    return local_filename

def convert(fname):
    pagenums = set()

    output = StringIO()
    manager = PDFResourceManager()
    laparams=LAParams()
    laparams.char_margin = float(50)
    converter = TextConverter(manager, output, laparams=laparams)
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text

url = 'http://www.ipe.com/Uploads/k/x/x/Top-400-Ranking.pdf'

text = convert(download_file(url))
#text = convert('Top-400-Ranking.pdf')

'Filter Out front and end stuff that\'s not data'
text = text[text.index('\n\n1  ') : text.index("\n\n©IPE Research.")]

acc = ''
for line in text.splitlines():
    if len(line) > 0 and line[0].isdigit():
        if not ('INVESTMENT & PENSIONS' in line or 'ASSET MANAGERS 2' in line):
            acc += line + '\n'

#acc = acc.replace('  ', ' ')
acc = acc.replace('*', '')
acc = re.sub(r"(?<=\d)(,)(?=\d)", '', acc)
acc = re.sub(r" \(.\d*\)", '', acc)
#acc = re.sub(r"[-$]", 'N/A', acc)
acc = re.sub(re.compile(r"^[0-9]*=? *", re.MULTILINE), "", acc)
#acc = acc.replace('  ', '|')

acc = acc.replace(' -', ' 0')

text = ""
for line in acc.splitlines():
    # company = ""
    # country = ""

    # scountry = re.findall(r"\b[^\d\W]+\b", line)
    # country = scountry[len(scountry)-1]

    # search = re.findall(r"(\d+)", line)
    # if search:
    #     y2018 = search[len(search)-2]
    #     y2017 = search[len(search)-1]
    # else:
    #     print("CANT FIND last num for:" + line)

    # scompany = re.sub(r"\b[^\d\W]+\b", "", line)
    s = line.split()
    l = len(s)
    country = s[l-3]
    y2018 = s[l-2]
    y2017 = s[l-1]
    company = ' '.join(s[:l-3])

    if 'Korea' in country:
        country = 'South Korea'
        company = company[:-5].strip()

    #print(company)
    text += company + '|' + country + '|' + y2018 + '|' + y2017 + '\n'

text = unidecode.unidecode(text)

print(text)

file = codecs.open("output.csv", 'w', 'utf-8')
file.write(text)
file.close()

os.remove('Top-400-Ranking.pdf')