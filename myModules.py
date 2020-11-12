def combi_func( df1, df2 ):
    #import pandas as pd
    combined = df1.merge(df2, on=["Date"], how='outer') #Join both of the CSV files using the 'Date' field
    combined = combined.iloc[1:] #Remove first row from file as date not matched
    #combined['Date'] = pd.to_datetime(combined['Date']) #Convert Dates from string to Date object type
    return combined