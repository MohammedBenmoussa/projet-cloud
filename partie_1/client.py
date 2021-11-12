import boto3
import time


# Get the service resource
sqs = boto3.resource('sqs')

# Create the queue. This returns an SQS.Queue instance
queue = sqs.create_queue(QueueName='requestQueue', Attributes={
                'DelaySeconds': '0'
                })

print(queue.url)


val = input("Enter your value: ")
response = queue.send_message(MessageBody=val)


time.sleep(30)

# Get the queue
queueResponse = sqs.get_queue_by_name(QueueName='responseQueue')
# Process messages by printing out body and optional author name
for message in queueResponse.receive_messages():
        print(format(message.body))
        message.delete(QueueUrl='https://sqs.us-east-1.amazonaws.com/389161245274/responseQueue', ReceiptHandle=message.receipt_handle)
