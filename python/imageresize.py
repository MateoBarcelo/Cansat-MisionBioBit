import os
from PIL import Image
class Resize:

    def __init__(self,base):

        self.base = base

    def resizeImage(self,path):
        img = Image.open(path)
        wpercent = (self.base/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((self.base,hsize), Image.ANTIALIAS)
        if(path=='ndvi.png'):
            img.save("build/assets/" +"converted"+path)
        img.save("converted"+path)
        
