
import pygame
import os

def load(man):
    
    man.instance.log("[ASSETS] Loading fonts...")
    for fontfile in os.listdir(os.path.join(man.location, "Fonts")):
        fpath = os.path.join(man.location, "Fonts")
        fontname, ext = os.path.splitext(fontfile)
        if ext == ".png":
            man.assets["fonts"][fontname] = Font(fpath, fontname)

class Font:

    def __init__(self, location, name):

        self.location = location
        self.name = name

        self.surface = pygame.image.load(os.path.join(self.location, self.name+".png"))
        with open(os.path.join(self.location, self.name+".txt"), "r", encoding="utf-8") as charfile:
            self.charset = charfile.read()
        self.size = self.surface.get_height()

        self._txt_cache = {}

    def get_size(self, txt, scale=1):
        tsize = len(txt) if not isinstance(txt, int) else txt
        return (tsize*self.size)*scale

    def get_size2(self, txt, scale=1, line_spacing=1):
        if not isinstance(txt, int):
            lines = txt.split("\n")
        w = max(len(l) for l in lines)*self.size if not isinstance(txt, int) else txt*self.size
        h = self.size+(txt.count('\n') if not isinstance(txt, int) else 1)*(self.size+line_spacing)

        return w*scale, h*scale

    def get_char(self, c):

        i = self.charset.index(c)
        r = pygame.Rect(0,0,0,0)
        r.width = r.height = self.size
        r.topleft = (i*self.size,0)

        return self.surface.subsurface(r)

    def render(self,surf,loc,txt,scale=1,blit_flags=0,line_spacing=1,blit_anchor_center=False,color=None,invalid_char_exception = False,multiline=True):

        if not multiline:
            txt = ''.join(txt.splitlines())

        cid = txt+":"+str(scale)+":"+str(color)

        if len(self._txt_cache) > 8000:
            self._txt_cache.clear()

        if cid not in self._txt_cache:
            #ts = pygame.Surface((len(txt)*self.size,self.size+txt.count('\n')*(self.size+line_spacing)))
            ts = pygame.Surface(self.get_size2(txt, 1, line_spacing))
            ts.set_colorkey((0,0,0))

            for linenum, line in enumerate(txt.split("\n")):
                for cp,c in enumerate(line):

                    if c == " ":
                        continue
                    elif c == "\n":
                        continue
                    
                    try:
                        cs = self.get_char(c)
                        ts.blit(cs,(cp*self.size,linenum*self.size+(line_spacing*linenum)))
                    except ValueError:
                        if invalid_char_exception:
                            raise

            ts = pygame.transform.scale(ts,(int(ts.get_width()*scale),int(ts.get_height()*scale))) if scale != 1 else ts

            if color:
                pa = pygame.PixelArray(ts)
                pa.replace((255,255,255),color)
                pa.close()

            self._txt_cache[cid] = ts
        else:
            ts = self._txt_cache[cid]

        surf.blit(ts,loc if not blit_anchor_center else pygame.Vector2(loc)-(int(ts.get_width()/2),int(ts.get_height()/2)),special_flags=blit_flags)
