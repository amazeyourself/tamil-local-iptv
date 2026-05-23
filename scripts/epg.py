import urllib3
import json
import xml.etree.ElementTree as ET
import gzip
from datetime import datetime

root = ET.Element('tv')
root.set('generator-info-url', 'https://github.com/amazeyourself')

epglinks = ["https://jiotvapi.cdn.jio.com/apis/v1.3/getepg/get?channel_id=3201&offset=0",
            "https://jiotvapi.cdn.jio.com/apis/v1.3/getepg/get?channel_id=3356&offset=0",
            "https://jiotvapi.cdn.jio.com/apis/v1.3/getepg/get?channel_id=3357&offset=0",
            "https://jiotvapi.cdn.jio.com/apis/v1.3/getepg/get?channel_id=3359&offset=0",
            "https://jiotvapi.cdn.jio.com/apis/v1.3/getepg/get?channel_id=3360&offset=0",
            "https://jiotvapi.cdn.jio.com/apis/v1.3/getepg/get?channel_id=3393&offset=0",
            "https://jiotvapi.cdn.jio.com/apis/v1.3/getepg/get?channel_id=3394&offset=0",
            "https://jiotvapi.cdn.jio.com/apis/v1.3/getepg/get?channel_id=3395&offset=0",
            "https://jiotvapi.cdn.jio.com/apis/v1.3/getepg/get?channel_id=3396&offset=0",
            "https://jiotvapi.cdn.jio.com/apis/v1.3/getepg/get?channel_id=3409&offset=0",
            "https://jiotvapi.cdn.jio.com/apis/v1.3/getepg/get?channel_id=3417&offset=0",
            "https://olidigital.space/olitv-epg.php"]
epgids = ["SanaTV", "RockTV", "DharsanTV", "SanaPlus", "SubinTV", "NTCTV", "SuriyaTV", "AaryaaTV", "UltimateTV", "RojaTV", "RojaMovies", "OliTV"]
displayNames = ["Sana TV", "Rock TV", "Dharsan TV", "Sana Plus", "Subin TV", "NTC TV", "Suriya TV", "Aaryaa TV", "Ultimate TV", "Roja TV", "Roja Movies", "Oli TV"]
logos = ["jio/sanatv.png", "jio/suriyantvtamil.png", "jio/dharshantvtamil.png", "jio/sanaplus.png", "https://subintv.in/SUBINLOGO.png", "jio/ntvtamil.png",
         "ashoka/1732170490_WhatsApp_Image_2024-11-21_at_11.10.20_AM-removebg-preview%20(2).png", "jio/aryatvtamil.png", "jio/utvtamil.png", "jio/rojatv.png", "jio/rojamovies.png",
         "https://i.ibb.co/XfvTQyJn/main-removebg-preview.png"]

for i in epglinks:
    resp = urllib3.request("GET", i)
    epgid = epgids[epglinks.index(i)]
    chnl = ET.SubElement(root, 'channel')
    chnl.set('id', epgid)
    dspl = ET.SubElement(chnl, 'display-name')
    icon = ET.SubElement(chnl, 'icon')
    dspl.text = displayNames[epglinks.index(i)]
    ico = displayNames[epglinks.index(i)].replace("jio", "https://jiotvimages.cdn.jio.com/dare_images/images").replace("ashoka", "https://livetv.ashokadigital.net/upload/logo")
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
            desc = prgdata['description']
            cat = prgdata['showCategory']
            date = prgdata['serverDate'][0:9].replace("-", "")
            thumb = "https://jiotv.catchup.cdn.jio.com/dare_images/shows/" + prgdata['episodeThumbnail']
            progtitle = ET.SubElement(prog, 'title')
            progtitle.text = title
            progdesc = ET.SubElement(prog, 'desc')
            progdesc.text = desc
            progcat = ET.SubElement(prog, 'category')
            progcat.text = cat
            progdate = ET.SubElement(prog, 'date')
            progdate.text = date
            progico = ET.SubElement(prog, 'icon')
            progico.set("src", thumb)
    else:
        epgroot = ET.fromstring(resp.data, parser=etree.XMLParser(recover=True,encoding='utf-8'))
        for type_tag in epgroot.findall('programme'):
            title = type_tag.find('title').text
            desctag = type_tag.find('desc')
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
