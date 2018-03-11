#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import random
import subprocess

class Cow:
    def __init__(self, filename ='data_cows.txt'):
        self.cows = []
        self.filename = filename
        self.current_cow = 0

    def find_buddies(self):
        """
        Finds and returns names of available cows
        """

        cow_data=subprocess.check_output(
                ['cowsay','-l']).decode("utf-8")
        cow_dir, cowsstr= cow_data.split('\n',1)
        self.cows = cowsstr.replace('\n',' ').split()
        self.current_cow = len(self.cows ) -1
        return self.cows

    def speak(self, txt, cow = '', eyes='', lolcat=False, width = 40):
        """
        : txt : ku-manus
        : cow : the name of a cow file in cow path. 
                see cowsay -l for list of options
        : eyes : string consisting of two letters
        """
        if not cow:
            if not self.cows:
                self.find_buddies()
            cows = self.cows
            cow = cows[self.current_cow]
            self.current_cow += 1
            self.current_cow %= (len(self.cows) - 1)
        if eyes:
            eyes = '-e '+eyes
        
        #cmd='figlet %s | cowsay %s -f %s -n -W %d'%(txt,eyes,cow,width)
        #cmd='cowsay %s -f %s  -W %d %s' %(eyes, cow, width, txt)

        cmds='%s -f %s -n -W %d'%(eyes,cow,width)
        args = ['cowsay'] + cmds.split()

        ps = subprocess.Popen(['figlet',txt], stdout=subprocess.PIPE)
        cowsay = subprocess.check_output(args, stdin=ps.stdout)
        ps.wait()
        #txt = cowsay.decode('utf-8')
        #txt_sp = txt.split('\n')
        #for line in txt_sp:
            #print(line +(60-len(line))*' '+ line)
        #print(repr(txt))
        lolcat = subprocess.Popen(['lolcat'], stdin=subprocess.PIPE)
        lolcat.communicate(cowsay)



if __name__ == '__main__':
    ku = Cow()
    print (ku.find_buddies())
    eyes = "HS" if random.randint(0,9) == 0 else ""
    ku.speak('HEI')
