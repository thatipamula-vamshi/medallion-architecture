import json
import boto3
import os 

# creates a low-level client to interact with Amazon S3 (Simple Storage Service).
client = boto3.client('s3')

def lambda_handler(event, context):

    """This function will take josnl format file from s3 Bucket
    and out puts the clean data. It will also create two file
    one conatians inconsistent data, other contains outlier data """
    
    # This will get the bucket_name and file name from event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object1 = event['Records'][0]['s3']['object']['key']
    
    # These will get the bukets and files name from environment varibales  
    Rejected_Bucket = os.environ.get('Rejected_Bucket')
    Rejected_File = os.environ.get('Rejected_File')
    
    Below_18_Bucket = os.environ.get('Below_18_Bucket')
    Below_18_File = os.environ.get('Below_18_File')
    
    Success_Bucket = os.environ.get('Success_Bucket')
    Success_File = os.environ.get('Success_File')
    
    # These lists will hold the data of the cleaned, inconsisent, outliers. 
    Above_18 = []
    Below_18 = []
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
            #We are checking if the age above 18 or not and appedning to their respective list
            if record['age']>18:
                Above_18.append(record)
            else:
                Below_18.append(record)
                
        except (json.JSONDecodeError, TypeError, KeyError) as e:
            Rejected_Data.append(record)
            
    #we are upload the data to there respetive buckets     
    client.put_object(
            Bucket=Rejected_Bucket,
            Key=Rejected_File,
            Body='\n'.join(map(json.dumps, Rejected_Data)).encode('utf-8')
        )
        
    client.put_object(
            Bucket=Below_18_Bucket,
            Key=Below_18_File,
            Body='\n'.join(map(json.dumps, Below_18)).encode('utf-8')
        )
            
    client.put_object(
            Bucket=Success_Bucket,
            Key=Success_File,
            # Convert each item in Above_18 to a JSON string, join them with newline characters,
            # then encode the entire string to bytes using UTF-8 encoding for uploading or transmission.
            Body='\n'.join(map(json.dumps, Above_18)).encode('utf-8')
        )
            
    return {
        'statusCode': 200,
        'body': json.dumps('Data is cleaned and sent to their respective s3 buckets')
    }
