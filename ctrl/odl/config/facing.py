#!/usr/bin/python

import requests
import xml.etree.ElementTree as ET
import progressbar

from time import sleep
bar = progressbar.ProgressBar(maxval=20, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

barcount=1

# Mount point names
nodes = ['host-eth', 'host-wifi', 'host-isp','host-en','host-enc','host-int','host-privc','host-pubc']

SUCCESS = [200,201,202]
print("Adding face to the network")
bar.start()
for node in nodes:
      response=None
      url=None
      tree = ET.parse('/hicn/cntrl/face.xml')
      root = tree.getroot()
      for faces in root:
         for face in faces:
                 if face.tag=='lip6':
                     lip6=face.text
                 if face.tag=='rip6':
                     rip6=face.text
                 if face.tag=='swif':
                     swif=face.text
         if faces.tag==str(node):
            tree = ET.parse('/hicn/cntrl/tface.xml')
            troot = tree.getroot()
            for elem in troot:
               if elem.tag=='{urn:sysrepo:hicn}lip6':
                   elem.text=lip6
               if elem.tag=='{urn:sysrepo:hicn}rip6':
                   elem.text=rip6
               if elem.tag=='{urn:sysrepo:hicn}swif':
                   elem.text=swif
            tree.write('/hicn/cntrl/aface.xml')
            filename='/hicn/cntrl/aface.xml'
            url = 'http://localhost:8181/restconf/operations/network-topology:network-topology/topology/topology-netconf/node/'+str(node)+'/yang-ext:mount/hicn:face-ip-add'
            headers = {'content-type': 'application/xml','accept':'application/xml'}
            response = requests.post(url, auth=('admin', 'admin'),data=open(filename).read(),headers=headers)
            if response.status_code in SUCCESS:
               bar.update(barcount+1)
               barcount=barcount+1
               sleep(0.1)
            else:
               print('operation failed'+str(node)+response.text)
bar.finish()

