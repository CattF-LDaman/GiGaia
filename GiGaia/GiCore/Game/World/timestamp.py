
from .constants import TIME_LENGTH_DAY
from GiGaia.GiCore.color_util import mix

class Timestamp:

    def __init__(self, tval):
        
        self.value = tval

        self.day, self.time_of_day = divmod(tval, TIME_LENGTH_DAY)
        self.day_progress = self.time_of_day/TIME_LENGTH_DAY

        self.is_day = self.day_progress < 0.72 and self.day_progress > 0.25
        self.is_night = not self.is_day

    def sky_color(self, cycle):

        cur = int(len(cycle)*self.day_progress)
        nxt = cur+1 if cur+1 < len(cycle) else 0

        return mix(cycle[cur], cycle[nxt], self.day_progress/(1/len(cycle))-int(len(cycle)*self.day_progress))
