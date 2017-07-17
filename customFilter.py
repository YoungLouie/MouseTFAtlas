import math
def logFot(fot):
    if fot!=0:
        return round(math.log(fot*1e10,10),3);
    else:
        return 0.0