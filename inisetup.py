import json
import boto3 as aws

def lambda_handler(event, context):
    # TODO implement
    user_id=event['user_id']
    device_name=event['device_id']
    device_type=event['device_name']
    client = aws.client('iot')
    
    #create thing
    initResponse = client.create_thing(
        thingName=device_name,
        thingTypeName=device_type,
        attributePayload={
        'attributes': {
            'version': '1.0.0'
        },
        'merge': True
    }
    )
    
    #thing created
    
    #create certificate and keys
    certAndKeys = client.create_keys_and_certificate(
    setAsActive=True
    )
    #keys and cerificate created
    
    #attach certificate
    client.attach_thing_principal(
    thingName=initResponse['thingName'],
    principal=certAndKeys['certificateArn']
    )
    #cerificate attched
    
    #clinet attach policy
    client.attach_policy(
    policyName='default_pol',
    target=certAndKeys['certificateArn']
    )
    #policy attatched
    response = {
        "thingName":initResponse['thingName'],
        "thingId":initResponse['thingId'],
        "thingArn":initResponse['thingArn'],
        "cerificate":certAndKeys['certificatePem'],
        "privateKey":certAndKeys['keyPair']['PrivateKey']
    }
    return {
        "statusCode": 200,
        "body": response
    }

