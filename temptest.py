from optionchain import OptionChain

oc = OptionChain('NASDAQ:GOOG')

oc.to_excel() # outputs puts and calls in an excel sheet

print(oc.puts)

print(oc.calls)