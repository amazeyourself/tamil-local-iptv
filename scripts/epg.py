import urllib3
import json
import xml.etree.ElementTree as ET
import pathlib
import gzip
from datetime import datetime

root = ET.Element('tv')
root.set('generator-info-url', 'https://github.com/amazeyourself')

epglinks = ["https://epg.neotvapp.com/RojaTV.xml",
            "https://epg.neotvapp.com/RojaMovies.xml",
            "https://olidigital.space/olitv-epg.php"]
epgids = ["RojaTV", "RojaMovies", "OliTV"]
displayNames = ["Roja TV", "Roja Movies", "Oli TV"]
logos = ["jio/rojatv.png", "jio/rojamovies.png", "https://i.ibb.co/XfvTQyJn/main-removebg-preview.png"]

for i in epglinks:
    resp = urllib3.request("GET", i)
    epgid = epgids[epglinks.index(i)]
    chnl = ET.SubElement(root, 'channel')
    chnl.set('id', epgid)
    dspl = ET.SubElement(chnl, 'display-name')
    icon = ET.SubElement(chnl, 'icon')
    dspl.text = displayNames[epglinks.index(i)]
    ico = logos[epglinks.index(i)].replace("jio", "https://jiotvimages.cdn.jio.com/dare_images/images").replace("ashoka", "https://livetv.ashokadigital.net/upload/logo")
    icon.set('src', ico)
    if "jiotvapi" in i:
        jsonresp = resp.json()
        for j in jsonresp['epg']:
            stringdata = json.dumps(j)
            prgdata = json.loads(stringdata)
            start = datetime.fromtimestamp(prgdata['startEpoch']/1000).strftime("%Y%m%d%H%M%S +0530")
            stop = datetime.fromtimestamp(prgdata['endEpoch']/1000).strftime("%Y%m%d%H%M%S +0530")
            catchup = str(prgdata['srno'])
            prog = ET.SubElement(root, 'programme')
            prog.set('channel', epgid)
            prog.set('start', start)
            prog.set('stop', stop)
            prog.set('catchup-id', catchup)
            title = prgdata['showname']
            if prgdata['description'] != None:
                desc = prgdata['description']
            cat = prgdata['showCategory']
            date = prgdata['serverDate'][0:9].replace("-", "")
            thumb = "https://jiotv.catchup.cdn.jio.com/dare_images/shows/" + prgdata['episodeThumbnail']
            progtitle = ET.SubElement(prog, 'title')
            progtitle.text = title
            progdesc = ET.SubElement(prog, 'desc')
            if desc != None:
                progdesc = ET.SubElement(prog, 'desc')
                progdesc.text = desc
            progcat = ET.SubElement(prog, 'category')
            progcat.text = cat
            progdate = ET.SubElement(prog, 'date')
            progdate.text = date
            progico = ET.SubElement(prog, 'icon')
            progico.set("src", thumb)
    else:
        epgroot = ET.fromstring(resp.data)
        for type_tag in epgroot.findall('programme'):
            title = type_tag.find('title').text
            desctag = type_tag.find('desc')
            if desctag.text != None:
                desc = desctag.text
            start = type_tag.get("start")
            stop = type_tag.get("stop")
            prog = ET.SubElement(root, 'programme')
            prog.set('channel', epgid)
            prog.set('start', start)
            prog.set('stop', stop)
            progtitle = ET.SubElement(prog, 'title')
            progtitle.text = title
            progdesc = ET.SubElement(prog, 'desc')
            progdesc.text = desc


xml_data = ET.tostring(root)

with open('epg.xml', 'wb') as f:
    f.write(xml_data)
f.close()

with gzip.open('epg.xml.gz', 'wb') as f:
    f.write(xml_data)
f.close()
