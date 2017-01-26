import os
import random
class Cow:
    def __init__(self, filename ='data_cows.txt'):
        self.cows = []
        self.filename = filename

    def find_buddies(self):
        """Saves available .cow file names in a file with name 
         self.filename, and loads to self.cows"""

        os.system('cowsay -l > %s' %self.filename)
        with open(self.filename) as infile:
            cow_dir = infile.readline()
            self.cows=reduce(lambda x,y: x+y, map(str.split, infile.readlines()))
        return self.cows

    def speak(self, txt, cow = '', eyes='', figspeak=False, lolcat=False, width = 40):
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
            cow = cows[random.randint(0,len(cows)-1)]
        if eyes:
            eyes = '-e '+eyes
        if not figspeak:
            cmd='cowsay %s -f %s %s -W %d' %(eyes, cow, txt, width)
        else:
            cmd='figlet %s | cowsay %s -f %s -n -W %d'%(txt,eyes,cow,width)
        if lolcat:
            cmd += '| lolcat'
        os.system(cmd)


if __name__ == '__main__':
    ku = Cow()
    eyes = "HS" if random.randint(0,9) == 0 else ""
    ku.speak('HEI', figspeak=True)
