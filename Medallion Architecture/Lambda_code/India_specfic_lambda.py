import json
import boto3
import os 

# creates a low-level client to interact with Amazon S3 (Simple Storage Service).
client = boto3.client('s3')

def lambda_handler(event, context):

    """This function will take josnl format file from s3 bucket
    and will check if the user belongs to india or not then it uplaod the active 
    Indian users to the respective s3 Bucket"""

    # This will get the bucket_name and file name from event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object1 = event['Records'][0]['s3']['object']['key']

    # These will get the bukets and files name from environment varibale
    India_Specific_Bucket = os.environ.get('India_Specific_Bucket')
    India_Specific_File = os.environ.get('India_Specific_File')

    #This will hold the indian specific users and other users in there respective list.
    India_Specific = []
    Rejected_Data = []
    
    # This will get the body(i.e content of the file) by default it is a streaming body and all the metadata.
    file_content = client.get_object(
        Bucket = bucket_name,
        Key = object1)

    # We are accessing the body(i.e File content). iter_lines() will only load the file content line by line() It is generator object  
    response = file_content['Body'].iter_lines()

    # we are calling each line with for loop
    for line in response:
        # We are decoding it by decode('utf-8'), after decoding it will be in string format. For this we are using json.loads() to covert to jsonl format
        record = json.loads(line.decode('utf-8'))
        
        try:
            # We are checking if the user belong to India or not
            if record['country'] == 'India':
                India_Specific.append(record)
                
        except (json.JSONDecodeError, TypeError, KeyError) as e:
            Rejected_Data.append(record)
            
    # we are upload the data to there respetive buckets
    client.put_object(
            Bucket=India_Specific_Bucket,
            Key=India_Specific_File,
            # Convert each item in India_Specific to a JSON string, join them with newline characters,
            # then encode the entire string to bytes using UTF-8 encoding for uploading or transmission.
            Body='\n'.join(map(json.dumps, India_Specific)).encode('utf-8')
        )
        
    return {
        'statusCode': 200,
        'body': json.dumps('Data is cleaned and sent to the respective S3 Bucket')
    }
