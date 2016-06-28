#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__      = "Xonshiz"
__email__ = "Xonshiz@psychoticelites.com"
__website__ = "http://www.psychoticelites.com"
__version__ = "v2.0"

'''
Found an interesting thread on reddit that helped me convert vtt to srt.
A HUGE thanks to fiskenslakt (https://www.reddit.com/user/fiskenslakt) for this "VTT" to "SRT conversion".
Read his contribution here : https://www.reddit.com/r/learnpython/comments/4i380g/add_line_number_for_empty_lines_in_a_text_file/d2upf5l

'''


import sys
import os, re
import requests
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf8')


# Let's fetch the Link and the source code of the video page.
def Url_And_Data_Fetcher():
    try:
        Link = raw_input("Please enter your Link : ")
        if not Link:
            raise ValueError('Please Enter A Link To The Video. This Application Will now Exit in 5 Seconds.')
    except ValueError as e:
        print(e)
        time.sleep(5)
        exit()

    q = requests.get(Link)
    soup = BeautifulSoup(q.text,"lxml")
    file = open("newfile.txt", "w")
    file.write(soup.encode("utf8") + "\n")
    file.close


# Looking up the "Content_id" for getting our subs and "Title" to name our sub file.
def Data_Lookup():
    with open('newfile.txt') as searchfile:
        for line in searchfile:
            left,sep,right = line.partition('/video/') #Looking For "Content_id" in the <meta content="http://ib3.huluim.com/video/60585710?region=US&amp;size=600x400" property="og:image"/> (60585710 is Con_id)
            if sep:
                OG_Title = right
                Splitter = OG_Title.split("?")
                Con_id = Splitter[0]
                #print "Content_id : ",Con_id

    with open('newfile.txt') as searchfile:
        for line in searchfile:
            left,sep,right = line.partition('title')
            if sep:
                Episode_Number = right
                Final_EP_Num = Episode_Number[7:].replace('| Hulu</title>','').replace('>','').replace("Online","")

    return (Con_id,Final_EP_Num)            

# Con_id = 60585710
# Final_EP_Num = Oh My Ghostess - Episode 1


# Getting the required things from Data_Lookup() and navigating to differnet URLs to get the VTT subs. VTT to SRT conversion is now in effect.
def Sub_Lookup(Con_id,Final_EP_Num):
    if not Con_id: # This shit isn't really working... but, oh well, you'll see a nice error anyway xD!
        print "Seems like there are no subs for ",Final_EP_Num,"\nMy work here is done!"
        sys.exit()
    else :
        Caption_Lookup = 'http://www.hulu.com/captions.xml?content_id='+Con_id
        q1 = requests.get(Caption_Lookup)
        soup1 = str(BeautifulSoup(q1.text,"lxml"))
        if soup1 == '':
            print "Seems like there are no subs for ",Final_EP_Num,"\nMy work here is done!"
            sys.exit()
        else :
            SMI_File_Link = soup1.replace('<?xml version="1.0" encoding="utf-8"?><html><body><transcripts><en>','').replace('</en></transcripts></body></html>','').replace('<html><body><transcripts><en>','') # Remove lxml usage, hence, this fugly code with shit load of replace.
            VTT_Sub_Link = SMI_File_Link.replace('captions','captions_webvtt').replace('smi','vtt') # Changing things so we get URL to our subs
            head, sep, tail = VTT_Sub_Link.partition('.vtt')
            print 'This is ', head
            #print "Downloading Subs From : ",VTT_Sub_Link # Nuffing Important
            print "Downloading Subs From : ",str(head)+'.vtt' # Nuffing Important
            VTT_Sub_Link_Main = str(head)+'.vtt'
            q3 = requests.get(VTT_Sub_Link_Main)
            soup3 = str(BeautifulSoup(q3.text,"lxml"))
            Subs_Data = soup3.replace('.',',').replace("<html><body><p>WEBVTT\n","").replace("--&gt;","-->").replace("</p></body></html>","").encode('utf8') # Conversion from VTT to SRT process 1
            File_Name = re.sub('[^A-Za-z0-9- ]+', '', Final_EP_Num) +'.srt' # Fix for "Special Characters" in The series name
            text_file = open(File_Name, "w")
            text_file.write(Subs_Data)
            text_file.close()
            with open(File_Name,'r+') as f: # A HUGE thanks to fiskenslakt (https://www.reddit.com/user/fiskenslakt) for this "VTT" to "SRT conversion". Read his contribution here : https://www.reddit.com/r/learnpython/comments/4i380g/add_line_number_for_empty_lines_in_a_text_file/
                lines = f.readlines()
                newLineCount = 0
                for i,num in enumerate(lines): 
                    if num == '\n':
                        newLineCount += 1
                        lines[i] = str(newLineCount) + '\n'
                f.seek(0)
                for line in lines:
                    f.write(line+'\n')

            
            print 'Subs Have Been Downloaded'


def main():
    try:
        Url_And_Data_Fetcher()
        Data_Lookup()
        Con_id,Final_EP_Num = Data_Lookup()
        os.remove("newfile.txt")
        Sub_Lookup(Con_id,Final_EP_Num)
    except Exception, e:
        print e
        pass




if __name__ == "__main__":
    main()