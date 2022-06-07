class CFG:

    def __init__(self, year):
        self._staticData = {}
        self.addStatic()
        self.specificExceptions = {}
        self.specificExceptionsYearly = {}
        self.allLocations = {"groceries": {'Supermarket','Asia store'},
                             "food": {'MacDonalds','Burger King','Tonys'},
                             "sports": {'Gorilla Gym'}}
                            #...
        self.topics = {'groceries','food','sports'}
        self.topicsComplete = {'groceries','food','sports','static topic','unclassified'}
        self.topicsCompleteAbbrv = {'groc','food','sport','stat','unlass'}
        self.howFix = {'groceries':3,'food':2,'sports':1,'static topics...':2,'unclassified':3}

        self.timeDictionaryShort = {1: 'Jan',
                                    2: 'Feb',
                                    3: 'Mar',
                                    4: 'Apr',
                                    5: 'May',
                                    6: 'Jun',
                                    7: 'Jul',
                                    8: 'Aug',
                                    9: 'Sep',
                                    10: 'Oct',
                                    11: 'Nov',
                                    12: 'Dec'}
        self.timeDictionaryLong = {1: 'January',
                                   2: 'February',
                                   3: 'March',
                                   4: 'April',
                                   5: 'May',
                                   6: 'June',
                                   7: 'July',
                                   8: 'August',
                                   9: 'September',
                                   10: 'October',
                                   11: 'November',
                                   12: 'December'}

        self.generalExceptions = {'Failed transaction'} # only an example
        self.initSpecExcept(year)

    def addStatic(self):
        # example for static topic

        #monthly expenses for going to the gym
        gymFees = {"UNI gym":100,"gorilla gym":200,"downtown gym":500}
        sum = 0
        for key in gymFees.keys():
            sum += gymFees[key]
        self._staticData["gymFees"] = sum

    @property
    def staticData(self):
        return self._staticData

    def initSpecExcept(self, year):
        if year == 2015:
            self.specificExceptions[1] = {}
            self.specificExceptions[2] = {'TWINT Anthony'}
            self.specificExceptions[3] = {'Apple shop'}
            self.specificExceptions[4] = {}
            self.specificExceptions[5] = {'Gorilla Gym excursion'}
        elif year == 2016:
            self.specificExceptions[5] = {'Jeffs Bike shop'}
            self.specificExceptions[6] = {}
            self.specificExceptions[7] = {}
            self.specificExceptions[8] = {}
            self.specificExceptions[9] = {}
            self.specificExceptions[10] = {'company lunch'}
            self.specificExceptions[11] = {}
            self.specificExceptions[12] = {}
