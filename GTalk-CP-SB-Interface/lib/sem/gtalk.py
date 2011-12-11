'''
Created on Dec 11, 2011

@author: sem
'''
from lib.PyGtalkRobot import GtalkRobot
from imdb import IMDb
import httplib
import urllib

class GTalk(GtalkRobot):
    '''
    classdocs
    '''     
    
    def __init__(self, url):
        GtalkRobot.__init__(self)
        self.url = url;
        self.ia = IMDb('mobile')
        self.movielist={};
        self.searchlist={};
        self.moreindex={};
    
    def searchMovie(self, user, query):
        movies = self.ia.search_movie(query);
        rv="";
        end=4;
        if(len(movies)<5):
            end=len(movies)-1;
        for i in range(0,end+1):
            rv+=str(i+1)+": "+movies[i]['long imdb canonical title']+"\n";
        
        if(len(movies)==0):
            rv="There were no results."
        
        self.movielist[user]=movies;
        self.searchlist[user]=True;
        self.moreindex[user]=0;
        return rv;
    
    def moreMovie(self, user):
        if(self.searchlist.has_key(user)):
            if(self.searchlist[user]==True):
                self.moreindex[user]+=1;
                movies = self.movielist[user];
                index = self.moreindex[user]*5;
                if(index <= len(movies)-1):
                    end=index+4;
                    rv="";
                    if(index+4>len(movies)-1):
                        end=len(movies)-1;
                    for i in range(index,end+1):
                        rv+=str(i+1)+": "+movies[i]['long imdb canonical title']+"\n";
                    return rv;
                self.moreindex[user]-=2;
                rv = self.moreMovie(user);
        return "There was an error.";
    
    def addMovie(self, user, args):
        if(self.searchlist.has_key(user) and int(args[0])<=10 and int(args[0])>0):
            if(self.searchlist[user]==True):
                rv = "Added: " + self.movielist[user][int(args[0])-1]['long imdb canonical title']
                url = "/movie/imdbAdd/?id=" + str(self.movielist[user][int(args[0])-1].movieID) + '&year=' + str(self.movielist[user][int(args[0])-1]['year']);
                print(self.url+url);
                params = urllib.urlencode({'quality': 8, 'add': 'Add'})
                headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
                conn = httplib.HTTPConnection(self.url)
                conn.request("POST", url, params, headers)
                r1 = conn.getresponse()
                if(int(r1.status) != 200):
                    rv = "There was an error."
                
                self.searchlist[user]=False;
                self.movielist[user]=None;
                
                return rv;
            return "There was an error."
    
    def command_001_imdb(self, user, message, args):
        '''[s|S]\s+(.*)'''
        self.replyMessage(user, str(self.searchMovie(user, args[0])))
    
    def command_002_add(self, user, message, args):
        '''[a|A]\s+([1-9]+)'''
        self.replyMessage(user, str(self.addMovie(user, args)))

    
    def command_003_more(self, user, message, args):
        '''[m|M]'''
        self.replyMessage(user, self.moreMovie(user));
        
            
    def command_100_nothing(self, user, message, args):
        '''.*'''
        print("hoi")
        self.replyMessage(user, None)