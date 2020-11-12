import boto3

def create_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.create_table(
        TableName='Covid',
        KeySchema=[
            {
                'AttributeName': 'Date',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'Cases',
                'KeyType': 'RANGE'
            },           
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'Date',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'Cases',
                'AttributeType': 'S'
            },            
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table


if __name__ == '__main__':
    covid_table = create_table()
    print("Table status:", covid_table.table_status)