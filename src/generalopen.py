#/***********************************************************************
# * Licensed Materials - Property of IBM 
# *
# * IBM SPSS Products: Statistics Common
# *
# * (C) Copyright IBM Corp. 1989, 2018
# *
# * US Government Users Restricted Rights - Use, duplication or disclosure
# * restricted by GSA ADP Schedule Contract with IBM Corp. 
# ************************************************************************/

# open files and windows specified by the General Open dialog box
# JKP, IBM SPSS
# history
# 08-05-2014 original version

import spss, os.path

class ManageClient(object):
    def __init__(self):
        self.clientstarted = False
        
    def start(self):
        if not self.clientstarted:
            self.SpssClient = __import__("SpssClient")
            self.SpssClient.StartClient()
            self.clientstarted = True
            
    def stop(self):
        if self.clientstarted:
            self.SpssClient.StopClient()
            self.clientstarted = False
            
    def OpenSavFile(self, existingfile, pwd, datasetname):
        spss.Submit(r"""get file="%s" %s.""" % (existingfile, pwd))
        if datasetname:
            spss.Submit("dataset name %s" % datasetname)
            
    def OpenExcelFile(self, existingfile, ext, sheet, readnames, assumedstrwidth, datasetname):
        spss.Submit(r"""get data /type=%s /file="%s" /sheet=name "%s" /readnames=%s
        /assumedstrwidth=%s.""" %
        (ext[1:], existingfile, sheet, readnames, assumedstrwidth))
        if datasetname:
            spss.Submit("dataset name %s." % datasetname)        
            
    def OpenSyntaxDoc(self, existingfile, password):
        self.start()
        self.SpssClient.OpenSyntaxDoc(existingfile, password=password)
    
    def OpenOutputDoc(self, existingfile, pwd):
        # pwd is syntax password expression password="password" or is blank
        spss.Submit(r"""output open file="%s" %s.""" % (existingfile, pwd))
    
    def NewDataFile(self, datasetname):
        spss.Submit("new file.")
        if datasetname:
            spss.Submit("""dataset name %s""" % datasetname)
            
    def NewSyntaxDoc(self):
        self.start()
        self.SpssClient.NewSyntaxDoc()
        
    def NewOutputDoc(self):
        self.start()
        self.SpssClient.NewOutputDoc()
     
def doopen(sheet, readnames, assumedstrwidth, data, syntax, output,
    existingfile="", datasetname="", newdatasetname="", password=""):

    client = ManageClient()
    
    if password:
        pwd = """ password="%s" """ % password
        spwd = password
    else:
        pwd = ""
        spwd = None
        
    ext = os.path.splitext(existingfile)[1]
    try:
        if ext:
            lowerext = ext.lower()
            if lowerext in [".sav", ".zsav"]:
                client.OpenSavFile(existingfile, pwd, datasetname)
            elif lowerext in [".sps", ".spsx"]:
                client.OpenSyntaxDoc(existingfile, password=spwd)
            elif lowerext in [".xls", ".xlsx", ".xlsm"]:
                client.OpenExcelFile(existingfile, ext, sheet, readnames, 
                    assumedstrwidth, datasetname)
            elif lowerext == ".spv":
                client.OpenOutputDoc(existingfile, pwd)
            else:
                raise ValueError("File type cannot be opened by this dialog box: %s" % ext)
        if data:
            client.NewDataFile(newdatasetname)
        if syntax:
            client.NewSyntaxDoc()
        if output:
            client.NewOutputDoc()
    finally:
        client.stop()