'''
Created on Dec 11, 2011

@author: sem
'''

from lib.sem.gtalk import GTalk
import cfg
import threading;
import socket,SocketServer
import lib.growl as growl;

gt = GTalk(cfg.couchpotato);
gt.setState('available', 'Notifier')

class movieDownload(threading.Thread):
    def __init__(self,gt):
        self.gt = gt;
        threading.Thread.__init__(self)
        
    def run(self):
        self.gt.start(cfg.login, cfg.password)

class reGrowl(threading.Thread):
    def __init__(self,gt):
        growl.gt = gt;
        threading.Thread.__init__(self)

    def run(self):
        
        SocketServer.UDPServer.allow_reuse_address = True # Attempt to let growlpeat run on the same machine as another Growl client
        
        try:
            GrowlMessageListener = SocketServer.UDPServer(("127.0.0.1", 9887), growl.IncomingGrowlHandler)
            GrowlMessageListener.serve_forever()
        except socket.error, (errNum, errText):
            print 'Encountered an error while attempting to listen for Growl messages: [{0}] {1}'.format(errNum, errText)
            print 'Is growlpeat or a Growl client already running on this computer?'
        
movieDownload(gt).start()
reGrowl(gt).start()