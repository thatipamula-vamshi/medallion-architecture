import json

def lambda_handler(event, context):
    """This function will notify if the filed file is created.
    it get triggred if a file lands in the customer-rejected-data-landing bucket"""
    
    print("Fail File Created")
    return {
        'statusCode': 200,
        'body': json.dumps('Failed file created')
    }
