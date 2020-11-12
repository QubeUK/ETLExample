def handler(event,context):
    import myModules, boto3
    from pandas import read_csv

    #Load the NY Times data into Memory
    nyUrl = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv' #Set URL for CSV to load
    nyData = read_csv(nyUrl) #Load CSV into Memory
    nyData.rename(columns = {"date": "Date"}, inplace = True) #Rename columns to match in both files
    nyData.rename(columns = {"cases": "Cases"}, inplace = True) #Rename columns to match in both files
    nyData.rename(columns = {"deaths": "Deaths"}, inplace = True) #Rename columns to match in both files

    #Load the John Hopkins  data into Memory and remove surplus data
    jhUrl = 'https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv' #Set URL for CSV to load
    jhData = read_csv(jhUrl) #Load CSV into Memory
    jhData = jhData[jhData['Country/Region'] == 'US'] #Remove all onn US data 
    jhData.drop(['Country/Region','Province/State','Confirmed','Deaths'],axis=1,inplace=True) #Remove surplus columns

    combined = myModules.combi_func(nyData,jhData) #Call module to join the files and convert Dates from string to Date object type

    for i in combined.columns: #converts all data to strings
        combined[i] = combined[i].astype(str)

    myDict=combined.T.to_dict().values() #converts all data to json dict structure

    resource = boto3.resource('dynamodb')
    table = resource.Table('Covid')
    for Case in myDict: #inputs lines into the database
        table.put_item(Item=Case)
        return