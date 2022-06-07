'''
Created by Jaú Gretler in May 2022
See main.py for full description of project.
This class can be used to analyse a csv file containing monetary flux of a bank account over a certain month
'''
import pandas as pd
from cfg import CFG


class Month:

    # remove the data rows who contain keywords marked as exception in cfg.py
    def rmExcept(self):
        idxToDrop = []
        # remove general exceptions
        for gE in self._genExcept:
            remData = self._data[self._data["Buchungstext"].str.contains(gE, na=False)]
            tempIdx = remData.index
            for tidx in tempIdx:
                idxToDrop.append(tidx)
        self._data = self._data.drop(index=idxToDrop)

        idxToDrop = []  # reset idxToDrop

        # remove month specific exceptions
        for sE in self._specExcept[self._monIdx]:
            remData = self._data[self._data["Buchungstext"].str.contains(sE, na=False)]
            tempIdx = remData.index
            for tidx in tempIdx:
                idxToDrop.append(tidx)
        self._data = self._data.drop(index=idxToDrop)

    # For each row in csv file, check which topic it matches (or if its unclassified) and in
    # the ._Res dict add the an entry _Res["topic" = <sum of expenses in that topic>
    # If you want to save the topic specific extactedData in the member variable _extractedData["Topic"]
    # set loadData = true
    def getTopic(self, topic, monthData, idxToDrop):
        loadData = False
        itemLocs = self._allLocs[topic]
        val = 0
        exData = pd.DataFrame()
        for _item in itemLocs:
            tempData = monthData.loc[
                monthData['Buchungstext'].str.contains(_item, na=False), ['Buchungstext', 'Belastung CHF']]
            if loadData:
                exData = pd.concat([exData, tempData]) #execute to have all meta data in each month as attribute in dict
            val += tempData['Belastung CHF'].sum()
            tempIdx = tempData.index
            for tidx in tempIdx:
                idxToDrop.append(tidx)
            del tempData
        self._extractedData[topic] = exData
        del exData
        self._Res[topic] = val

    # calc outflow and add it as member variable to the class object
    def addOutFlow(self):
        total = 0
        for key in self._Res:
            if key != "inflow":
                total += self._Res[key]
        # self.Res["outflow"] = total
        self._outflow = total
        total = 0

    ##########################################################################################

    def initConfig(self):
        self._cfg = CFG(self._year)
        self._topics = self._cfg.topics
        self._allLocs = self._cfg.allLocations
        self._specExcept = self._cfg.specificExceptions
        self._genExcept = self._cfg.generalExceptions

    ##########################################################################################

    def __init__(self, year, number):
        # declarations
        self._extractedData = {}
        self._yaxis = None
        self._topics = None
        self._Res = {}
        self._genExcept = None
        self._specExcept = None
        self._cfg = None
        self._outflow = 0
        self._xaxis = None
        self._allLocs = {}
        self._monIdx = number
        self._year = year

        # data reading
        filename = "<bank>_" + str(year) + "_" + str(number) + ".csv"
        self._data = pd.read_csv(filename, sep=';')

        # data cleaning
        self._data = self._data[
            ['Buchungstext', 'Belastung CHF', 'Gutschrift CHF']].copy()  # extract interesting columns

        # containers for results
        self.initConfig()
        self.name = str(self._year - 2000) + " " + self._cfg.timeDictionaryShort[self._monIdx]

        # remove exceptions
        self.rmExcept()

        # get inflow
        inflowData = self._data[self._data['Gutschrift CHF'] > 0]
        self._extractedData["inflow"] = inflowData
        inflowIdx = inflowData.index
        inflow = inflowData['Gutschrift CHF'].sum()
        self._inflow = inflow

        # get outflow data
        self._extractedData["outflow"] = self._data

        # drop gutschriften
        self._data = self._data.drop(index=inflowIdx)
        self._data = self._data[['Buchungstext', 'Belastung CHF']].copy()  # drop rows with Gutschrift

        idxToDrop = []

        # start analysis ########################################

        # analyze topics
        for to in self._topics:
            self.getTopic(to, self._data, idxToDrop)

        # add static expenses (these are expenses whose entries are hard coded in the cfg file)
        self.addStatic()

        # get outflow
        self.addOutFlow()

        # drop classified things and rows with empty cells
        self._data = self._data.drop(index=idxToDrop)
        self._data.dropna(inplace=True)

        # create class of unclassified things
        self._unclassified = self._data
        self._Res["unclassified"] = self._unclassified["Belastung CHF"].sum()

        # sort dictionary
        # self._Res = dict(sorted(self._Res.items(), key=lambda x: x[1]))

    @property
    def unclassified(self):
        return self._unclassified

    @property
    def year(self):
        return self._year

    @property
    def monIdx(self):
        return self._monIdx

    @property
    def inflow(self):
        return self._inflow

    @property
    def outflow(self):
        return self._outflow

    @property
    def data(self):
        return self._data

    @property
    def extractedData(self):
        return self._extractedData

    @property
    def Res(self):
        return self._Res

    def getExpensesOver(self, thresh):
        allOut = self._extractedData["outflow"]
        allOut = allOut[['Buchungstext', 'Belastung CHF']].copy()
        return allOut[allOut["Belastung CHF"] > thresh]

    def addStatic(self):
        for sDat in self._cfg.staticData:
            self._Res[sDat] = self._cfg.staticData[sDat]
