# Lab 4 - Self-Driving Car

Link to document: https://docs.google.com/document/d/15m3dQ6kDUtlmzz9U-uds3tYJRxPFpJNa-XeZYZpXJTk/edit#heading=h.ovu6ng5gkq6t

## steps in AWS CLI
To create lots of things:

aws iot create-thing --thing-name test-thing-1 --output json
aws iot create-thing --thing-name test-thing-2 --output json
aws iot create-thing --thing-name test-thing-3 --output json
aws iot create-thing --thing-name test-thing-4 --output json
aws iot create-thing --thing-name test-thing-5 --output json
aws iot create-thing --thing-name test-thing-6 --output json
aws iot create-thing --thing-name test-thing-7 --output json
aws iot create-thing --thing-name test-thing-8 --output json
aws iot create-thing --thing-name test-thing-9 --output json
aws iot create-thing --thing-name test-thing-10 --output json

To add them to the test-things group:

aws iot add-thing-to-thing-group --thing-name test-thing-1 --thing-group-name test_things
aws iot add-thing-to-thing-group --thing-name test-thing-2 --thing-group-name test_things
aws iot add-thing-to-thing-group --thing-name test-thing-3 --thing-group-name test_things
aws iot add-thing-to-thing-group --thing-name test-thing-4 --thing-group-name test_things
aws iot add-thing-to-thing-group --thing-name test-thing-5 --thing-group-name test_things
aws iot add-thing-to-thing-group --thing-name test-thing-6 --thing-group-name test_things
aws iot add-thing-to-thing-group --thing-name test-thing-7 --thing-group-name test_things
aws iot add-thing-to-thing-group --thing-name test-thing-8 --thing-group-name test_things
aws iot add-thing-to-thing-group --thing-name test-thing-9 --thing-group-name test_things
aws iot add-thing-to-thing-group --thing-name test-thing-10 --thing-group-name test_things

Assigned certificates to each thing:

aws iot attach-thing-principal --thing-name test-thing-1 --principal arn:aws:iot:us-east-2:681631399186:cert/94fb09fc355f25b7423158840e3fcc3eddb51d387276e577b6899097f7c3bb36 --output json
aws iot attach-thing-principal --thing-name test-thing-2 --principal arn:aws:iot:us-east-2:681631399186:cert/94fb09fc355f25b7423158840e3fcc3eddb51d387276e577b6899097f7c3bb36 --output json                             
aws iot attach-thing-principal --thing-name test-thing-3 --principal arn:aws:iot:us-east-2:681631399186:cert/94fb09fc355f25b7423158840e3fcc3eddb51d387276e577b6899097f7c3bb36 --output json                             
aws iot attach-thing-principal --thing-name test-thing-4 --principal arn:aws:iot:us-east-2:681631399186:cert/94fb09fc355f25b7423158840e3fcc3eddb51d387276e577b6899097f7c3bb36 --output json                             
aws iot attach-thing-principal --thing-name test-thing-5 --principal arn:aws:iot:us-east-2:681631399186:cert/94fb09fc355f25b7423158840e3fcc3eddb51d387276e577b6899097f7c3bb36 --output json                             
aws iot attach-thing-principal --thing-name test-thing-6 --principal arn:aws:iot:us-east-2:681631399186:cert/94fb09fc355f25b7423158840e3fcc3eddb51d387276e577b6899097f7c3bb36 --output json                             
aws iot attach-thing-principal --thing-name test-thing-7 --principal arn:aws:iot:us-east-2:681631399186:cert/94fb09fc355f25b7423158840e3fcc3eddb51d387276e577b6899097f7c3bb36 --output json                             
aws iot attach-thing-principal --thing-name test-thing-8 --principal arn:aws:iot:us-east-2:681631399186:cert/94fb09fc355f25b7423158840e3fcc3eddb51d387276e577b6899097f7c3bb36 --output json                             
aws iot attach-thing-principal --thing-name test-thing-9 --principal arn:aws:iot:us-east-2:681631399186:cert/94fb09fc355f25b7423158840e3fcc3eddb51d387276e577b6899097f7c3bb36 --output json                             
aws iot attach-thing-principal --thing-name test-thing-10 --principal arn:aws:iot:us-east-2:681631399186:cert/94fb09fc355f25b7423158840e3fcc3eddb51d387276e577b6899097f7c3bb36 --output json                            

Attach policy to each thing (ended up just attaching it to the thing group):

aws iot attach-policy --policy-name incoming_messages --target arn:aws:iot:us-east-2:681631399186:thinggroup/test_things --output json


To get the certificate PEM and private key into files, use this bash script in AWS cloushell:

''' python

#!/bin/bash

- Specify the number of Things (change this to the actual number of Things)
num_things=10

- Use "./" to save files in the current directory
output_directory="./"

- Known certificate ID
common_certificate_id="94fb09fc355f25b7423158840e3fcc3eddb51d387276e577b6899097f7c3bb36"

for ((i = 1; i <= $num_things; i++)); do
    thing_name="test-thing-$i"
    
    # Download the certificate description
    aws iot describe-certificate --certificate-id "$common_certificate_id" --output json > "$output_directory/$thing_name-certificate-description.json"

    # Download the certificate PEM file
    aws iot describe-certificate --certificate-id "$common_certificate_id" --output json | jq -r '.certificateDescription.certificatePem' > "$output_directory/$thing_name-certificate.pem"

    # Download the private key file
    aws iot get-pem --thing-name "$thing_name" --set-as-active --output text > "$output_directory/$thing_name-private-key.pem"

    echo "Downloaded certificate and private key for $thing_name"
done
'''

I needed to download local after, so I did this:

zip -r my_certificates.zip *.pem *.json


Issue generating private keys for this, so had to undo with code here:

- Assume your test-things are named test-thing-1 to test-thing-10
for i in {1..10}; do
    thing_name="test-thing-$i"
    certificate_id=$(aws iot list-certificates --query "certificates[?thingName=='$thing_name'].certificateId" --output text)
    
    if [ -n "$certificate_id" ]; then
        # Detach the certificate from the thing
        aws iot detach-thing-principal --thing-name "$thing_name" --principal "$certificate_id"
        
        # Delete the certificate
        aws iot delete-certificate --certificate-id "$certificate_id"
    fi
done



I ended up scrapping all this above, and created certificates manually
But after this, I was able to renmae files easily after downloading with this below:

#!/bin/bash

# Rename folders
for i in {1..10}; do
  old_folder="test-thing-$i"
  new_folder="device_$i"
  mv "$old_folder" "$new_folder"
done

# Rename files
for i in {1..10}; do
  folder="device_$i"
  mv "$folder/"*"-certificate.pem.crt" "$folder/device_$i.certificate.pem"
  mv "$folder/"*"-private.pem.key" "$folder/device_$i.private.pem"
  mv "$folder/"*"-public.pem.key" "$folder/device_$i.public.pem"
done

# installing greengrass

Use these strategies to move certificatres and stuff:
IP of EC2 instance: 172.31.42.171 

cd path-to-downloaded-files
pscp -pw Pi-password greengrass-OS-architecture-1.11.6.tar.gz pi@IP-address:/home/pi
pscp -pw Pi-password certificateId-certificate.pem.crt pi@IP-address:/home/pi
pscp -pw Pi-password certificateId-public.pem.key pi@IP-address:/home/pi
pscp -pw Pi-password certificateId-private.pem.key pi@IP-address:/home/pi
pscp -pw Pi-password AmazonRootCA1.pem pi@IP-address:/home/pi