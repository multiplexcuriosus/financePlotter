'''
Created by Jaú Gretler, May 2022
'''

from month import Month
from selection import Selection

'''
This code can be used to analyze csv files containing money flows from a bank account.
Month objects can be instantiated with their respective year and index in the year (1-12).
Example: Jan = Month(2021,1) #create month object
The init method of the month object analyzes the csv file of that month.
A big part of this analysis is extracting how much money was spent on a certain topic, such as food or taxes.
These topics can and must be specified in the cfg file for this code to work.
You can also specify terms which should be ignored generally or in certain months.

To adapt this code to you, you need to do the following things:

0.) In the __init__ method in month.py there are the following two lines:
filename = "<bank>_" + str(year) + "_" + str(number) + ".csv"
--> Obviously, you have to bring the names of your target files into this format
self._data = pd.read_csv(filename, sep=';')
--> if your csv file has another seperator than ';', you have to specifiy that in the line above
1.) Fill the dict 'allLocations' in the cfg.py with your target topics and keywords for that topic. 
An example: self.alLLocations["food"] = {'Burger King', 'KFC', 'Peking garden'} 
When the program now parses each line of the csv file it will search for these keywords and remember 
how much you spent on eating at these places (1)
2.) In month.py you need to replace all occurrences of some words with their corresponding term
in your csv file:
"Buchungstext" <-- <Column name of the description of the expense>
"Belastung CHF" <-- <Column name of the value of the expense>
"Gutschrift CHF" <-- <Column name of the value of the credit>
3.) Fill the list 'topics' in the cfg.py file with the topics you want to analyze. See 1.) for an example. 
Also,fill the list 'topicsComplete' in the cfg.py file with all topics from 'topics' + 'unclassified' + 
all names of your static topics (see 4.))
4.) In the method 'addStatic' in cfg.py add dictionaries or just values of constant monthly expenses analogously to the example.
5.) In the method 'initSpecExcept' in cfg.py add exceptions to the year and month the exception to be ignored happend.
Example:
if year == 2022:
    self.specificExceptions[3] = {'Failed transaction'}
elif year == 2021:
    self.specificExceptions[6] = {'account transfer'}
With these parameters, the withdrawals in march and june of their respective years with these
key words are ignored for the analysis
6.) Fill the list 'generalExceptions' in cfg.py with keywords you want to be always ignored
7.) For the plot 'plot15months' in selection.py, the plot can be configured to use
abbreviations of the topics names to make the plot prettier. If you want to use that,
you need to define an abbreviation for each topic name in topicComplete. This you must do in the 
dict 'topicsCompleteAbbrv' in cfg.py. To use it, you also must set the bool 'abbrv' to true in 'plot15months'
8.) If you want to color the individual bars of the bar plot accoding to certain criteria,
you can edit the dict 'howFix' in cfg.py. In 'howFix' you can specify which topics has what criterion index
and in the dict 'colDict' in selection.py you can set which criterion index corresponds to what color

Note: 'plotAllTopics' will look bad on non-quadratic screens. You can adjust the paramters of the plot if it 
annoys you too much.

Good luck, have fun!

(1) If you set loadData = true in getTopic in month.py you will save
not only the information of how much you spend per topic, but you can then also call monX.extractedData["topicY]
to get a dataframe containing all entries about topicY in your month object monX
'''


# load months and analyze them during their __init__

months = []
for i in range(5, 13):
    months.append(Month(2021, i))
for i in range(1, 6):
    months.append(Month(2022, i))

# create selection and plot things
sel = Selection(months)
# calc and plot average per month
sel.plotAvPAllMon()
# calc and plot flows
sel.plotFlow()
# plot 15 months
sel.plot15months()
# plot topic
sel.plotTopic("food")
# plot all topics
sel.plotAllTopics()



