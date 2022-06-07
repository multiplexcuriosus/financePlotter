'''
Created by Jaú Gretler in May 2022
See main.py for full description of project.
This class can be used to analyse a set of month objects and plot the findings.
'''
import numpy as np

from month import Month
import matplotlib.pyplot as plt
from cfg import CFG


class Selection:
    def __init__(self, _months):
        self._cfg = CFG(2022)
        self._months = _months
        self._topics = self._cfg.topicsComplete
        self._averages = {}
        self.yaxis = None
        self.xaxis = None

    # create a quadratic grid of subplots, each subplot plotting a specific topic over all months
    # added to the selection
    def plotAllTopics(self):
        # get grid size
        m = len(self._cfg.topicsComplete)
        n = min(int(np.sqrt(m)) + 1, int(np.sqrt(m)))
        # create plot objects
        fig, axs = plt.subplots(n, n)
        # create x axis
        X = []
        for mon in self._months:
            idy = mon.year - 2000
            id = str(mon.monIdx) + "." + str(idy)
            X.append(id)
        tops = list(self._cfg.topicsComplete)  # get a complete list of all topics incl. static and unclassified
        # create all plots
        k = 0
        for i in range(n):
            for j in range(n):
                if k <= m:
                    top = tops[k]
                    Yarr = np.asarray([m.Res[top] for m in self._months])
                    AvLine = np.ones(len(self._months)) * np.average(Yarr)
                    axs[i][j].plot(AvLine, color='red', label='Av')
                    axs[i][j].bar(X, Yarr, color='blue')
                    axs[i][j].set(ylabel="CHF")
                    axs[i][j].tick_params('x', rotation=90, size=2)
                    axs[i][j].grid()
                    axs[i][j].set_title(top, fontweight='bold')
                    k += 1
        # polish plots
        plt.subplots_adjust(top=0.92)
        plt.subplots_adjust(left=0.064)
        plt.subplots_adjust(right=0.98)
        plt.subplots_adjust(bottom=0.029)
        plt.subplots_adjust(wspace=0.2)
        plt.subplots_adjust(hspace=0.452)

        tit = "All topics over " + str(len(self._months)) + " months"
        plt.suptitle(tit, fontsize=20)

        # plt.get_current_fig_manager().full_screen_toggle()  # toggle fullscreen mode
        plt.show()

    # plot a single topic over all months added to selection, incl. overall average
    def plotTopic(self, top):
        Yarr = np.asarray([m.Res[top] for m in self._months])
        AvLine = np.ones(len(self._months)) * np.average(Yarr)
        X = [m.name for m in self._months]
        fig = plt.figure(figsize=(10, 10))
        plt.bar(X, Yarr, color='orange')
        plt.plot(AvLine, color='blue', label='Av')
        plt.xticks(rotation=45)
        plt.ylabel('CHF')
        _title = top + " over " + str(len(self._months)) + " months"
        plt.title(_title)
        plt.legend()
        plt.grid()
        plt.show()

    # plot in- and outflow of bank account excl. the exceptions over all months added to the selection
    # incl. mon average of in- and outflow
    def plotFlow(self):
        # create x axis
        x = [m.name for m in self._months]
        x_axis = np.arange(len(x))
        # create np flow arrays
        inf = np.asarray([mon.inflow for mon in self._months])
        outf = np.asarray([mon.outflow for mon in self._months])
        # calc average
        infMonAv = np.average(inf)
        outfMonAv = np.average(outf)
        # craeate avg lines
        infMonAvLine = np.ones(len(self._months)) * infMonAv
        outfMonAvLine = np.ones(len(self._months)) * outfMonAv
        # plot avg lines and bar plot itself
        plt.plot(infMonAvLine, color='lime', label='inflow  Av / mon')
        plt.plot(outfMonAvLine, color='salmon', label='outflow  Av / mon')
        plt.plot(x_axis, inf, label='inflow', color='green')
        plt.plot(x_axis, outf, label='outflow', color='red')
        plt.xticks(x_axis, x)
        plt.tick_params('x', rotation=45, size=5)
        tit = 'Inflow and outflow over period of ' + str(len(x)) + ' months'
        plt.title(tit)
        plt.grid()
        plt.legend()
        plt.show()

    # plot average of each topic over all months added to selection
    def plotAvPAllMon(self):
        # calc averages
        for top in self._topics:
            sum = 0
            for mon in self._months:
                sum += mon._Res[top]
            self._averages[top] = sum / len(self._months)
        self._averages = dict(sorted(self._averages.items(), key=lambda x: x[1]))
        # setup plot
        fig = plt.figure(figsize=(10, 10))
        X = list(self._averages.keys())
        Yarr = np.asarray(list(self._averages.values()))
        # create handle for howFix table
        fixDict = self._cfg.howFix
        # create color scheme
        colDict = {0: 'grey', 1: 'green', 2: 'blue', 3: 'red'}
        cols = [colDict[fixDict[x]] for x in X]
        # do plotting
        plt.bar(X, Yarr, color=cols)
        plt.xticks(rotation=45)
        plt.ylabel('CHF')
        _title = "Average over " + str(len(self._months)) + " months"
        plt.title(_title)
        plt.grid()
        plt.show()

    @property
    def averages(self):
        return self._averages

    # plot 15months, each month containing the expenses from all topics
    def plot15months(self):
        # use abbreviations of topic names to make plot prettier
        abbrv = True
        # create plot objects
        m = len(self._months)
        fig, axs = plt.subplots(3, 5)
        # create plots
        k = 0
        for i in range(3):
            for j in range(5):
                if k < m:
                    mon = self._months[k]
                    Yarr = []
                    X = []
                    for key in mon.Res.keys():
                        if mon.Res[key] > 0:
                            Yarr.append(mon.Res[key])
                            X.append(key)

                    # create averages
                    fixDict = self._cfg.howFix
                    # create colors
                    colDict = {0: 'grey', 1: 'green', 2: 'blue', 3: 'red'}
                    cols = [colDict[fixDict[x]] for x in X]
                    # create fix level avgs
                    fixDict = self._cfg.howFix
                    fix3avg = [mon.Res[x] for x in X if fixDict[x] == 3]
                    fix3avgLine = np.ones(len(X)) * np.average(fix3avg)
                    axs[i][j].plot(fix3avgLine, color=colDict[3], label='Fix level 3', linewidth=1)
                    fix2avg = [mon.Res[x] for x in X if fixDict[x] == 2]
                    fix2avgLine = np.ones(len(X)) * np.average(fix2avg)
                    axs[i][j].plot(fix2avgLine, color=colDict[2], label='Fix level 2', linewidth=1)
                    fix1avg = [mon.Res[x] for x in X if fixDict[x] == 1]
                    fix1avgLine = np.ones(len(X)) * np.average(fix1avg)
                    axs[i][j].plot(fix1avgLine, color=colDict[1], label='Fix level 1', linewidth=1)
                    # total AV
                    AvLine = np.ones(len(X)) * np.average(Yarr)
                    axs[i][j].plot(AvLine, color='black', label='Av', linewidth=2)
                    if abbrv:
                        X = [self._cfg.topicsCompleteAbbrv[x] for x in X]
                    axs[i][j].bar(X, Yarr, color=cols)
                    if j == 0:
                        axs[i][j].set(ylabel="CHF")
                    axs[i][j].tick_params('x', rotation=90, size=2)
                    axs[i][j].grid()
                    axs[i][j].set_title(mon.name, fontweight='bold')
                    k += 1

        # polish plots
        linux = False
        topV = 0
        bottomV = 0
        hV = 0
        if linux:
            topV = 0.92
            bottomV = 0.029
            hV = 0.636
        else:
            topV = 0.9
            bottomV = 0.102
            hV = 0.674
        plt.subplots_adjust(top=topV)
        plt.subplots_adjust(left=0.064)
        plt.subplots_adjust(right=0.98)
        plt.subplots_adjust(bottom=bottomV)
        plt.subplots_adjust(wspace=0.26)
        plt.subplots_adjust(hspace=hV)
        plt.legend()

        tit = "Expenses in each of up to 15 months"
        plt.suptitle(tit, fontsize=20)

        # plt.get_current_fig_manager().full_screen_toggle()  # toggle fullscreen mode
        plt.show()

    # plot 4 months
    def plot4(self, _months):
        n = len(_months)
        # create plot objects
        fig, axs = plt.subplots(2, 2, figsize=(20, 10))
        # create plots
        k = 0
        for i in range(2):
            for j in range(2):
                mon = _months[k]
                axs[i][j].bar(mon.Res.keys(), mon.Res.values(), color='blue')
                axs[i][j].set(ylabel="CHF")
                axs[i][j].tick_params('x', rotation=45, size=5)
                axs[i][j].grid()
                axs[i][j].title.set_text("Expenses " + mon.name)
                k += 1

        # polish plots
        fig.tight_layout(h_pad=8)
        plt.subplots_adjust(top=0.95)
        plt.subplots_adjust(left=0.05)
        plt.subplots_adjust(bottom=0.1)

        plt.show()

    # plot 2 months
    def plot2(self, _months):
        n = len(_months)
        # create plot objects
        fig, axs = plt.subplots(n, figsize=(20, 10))
        # create plots
        for i in range(n):
            mon = _months[i]
            axs[i].bar(mon.Res.keys(), mon.Res.values(), color='blue')
            axs[i].set(ylabel="CHF")
            axs[i].tick_params('x', rotation=45, size=5)
            axs[i].grid()
            axs[i].title.set_text("Expenses " + mon.name)
        # polish plots
        fig.tight_layout(h_pad=8)
        plt.subplots_adjust(top=0.95)
        plt.subplots_adjust(left=0.05)
        plt.subplots_adjust(bottom=0.1)
        plt.show()
