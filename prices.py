import my_const
import energidataservice


class Prices():
    def __init__(self):
        self.tid = []
        self.pris = []
        self.avg = []
        self.min_idx = 0

        responseJSON = energidataservice.spotprices(my_const.windowAhead)
        data = responseJSON["result"]["records"]

        for x in data:
            x_tid = x["HourDK"]
            x_pris = x["SpotPriceEUR"]
            print(x_tid, x_pris)
            self.tid.append(x_tid)
            x_pris = round((float(x_pris) * 7.46) / 1000.0, 2)
            self.pris.append(x_pris)

        print("len(tid) : ", len(self.tid))
        print("len(pris) : ", len(self.pris))

        self.calcAvg()

    def calcAvg(self):
        idx = 0
        for x in self.pris:
            if idx > 3 and (idx < (len(self.pris) - 3)):
                avg_window = round(
                    (self.pris[idx-1] + x + self.pris[idx+1])/3, 2)
            else:
                avg_window = round(x)

            self.avg.append(avg_window)

            print(idx, " avg : ", avg_window, " pris : ",
                  self.pris[idx], " dato : ", self.tid[idx])
            idx += 1

        min_val = min(self.avg)
        print("Min value = ", min_val)
        self.min_idx = self.avg.index(min_val)
        print("Min. value index = ", self.min_idx)

        print("dato for min value : ", self.tid[self.min_idx])
