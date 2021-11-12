import boto3
import statistics
from datetime import datetime


# Get the service resource
sqs1 = boto3.resource('sqs')

s3 = boto3.resource('s3')
partie1_bucket = s3.Bucket("partie1")

#Get the queue
queueRequest = sqs1.get_queue_by_name(QueueName="requestQueue")

queue = sqs1.create_queue(QueueName='responseQueue', Attributes={
                'DelaySeconds': '0',

                })

while(1):



    try:
        for message in queueRequest.receive_messages():
            #--------recuperer les nombres et les stocker dans une liste--------
            t=[int(n) for n in (format(message.body)).split(',')]
            #--------gestion des erreurs--------
            flag=0
            for i in t:
                if i<0:
                    flag=1
            if flag == 1:
                results="le tableau doit contenir des nombres positifs"
            elif len(t) > 10:
                results="le tableau doit contenir 10 nombres au maximum"
            else:
                print(t)
                minimum = min(t)
                maximum = max(t)
                sum1 = sum(t)
                length = len(t)
                average = sum1/length
                median = statistics.median(t)
                results = "minimum is %d " %(minimum) + " maximum is %d " %(maximum) +  " average is %d  " %(average) + " median is %d " %(median)
            #--------afficher les msg--------
            print(results)
            #--------fichier log--------
            current_date_and_time = datetime.now().strftime("%Y-%m-%d-%H%M%S")
            current_date_and_time_string = str(current_date_and_time)
            extension = ".txt"
            log_file =  "log_"+current_date_and_time_string + extension
            s3 = boto3.resource('s3')
            txt_data = results
            object = s3.Object(bucket_name='partie1', key=log_file)
            result = object.put(Body=txt_data)         
            response = queue.send_message(MessageBody=results)
            res = result.get('ResponseMetadata')
            if res.get('HTTPStatusCode') == 200:
                print('File Uploaded Successfully')
            else:
                print('File Not Uploaded')
            #--------supprimer la queue---------
            message.delete(QueueUrl='https://sqs.us-east-1.amazonaws.com/389161245274/requestQueue', ReceiptHandle=message.receipt_handle)
            print("request queue deleted")

    except:
        print("Wait...")

