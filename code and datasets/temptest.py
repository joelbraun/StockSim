from pandas.io.data import Options

aapl = Options('AAPL')
vals = aapl.get_options_data()
print(vals)