from stockex import stockwrapper as sw

data = sw.YahooData()

file = open('test.txt', 'w')

file.write(str(data.get_current(['GOOG'])))