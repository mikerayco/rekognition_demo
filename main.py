import io
from PIL import Image

import boto3

client = boto3.client('rekognition')


def detect_celebrity(image_uri: str):
    stream = io.BytesIO()
    image = Image.open(image_uri)
    image.save(stream, format="jpeg")
    image_binary = stream.getvalue()

    response = client.recognize_celebrities(
        Image={"Bytes": image_binary}
    )
    celeb = response['CelebrityFaces'][0]
    name = celeb['Name']
    confidence = celeb['MatchConfidence']
    # print(response)
    return f'This is {confidence}% {name}'


def detect_labels(bucket_name: str, obj_name: str):
    response = client.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': obj_name,
            }
        },
        MaxLabels=10,
        MinConfidence=85
    )
    labels = []
    for label in response['Labels']:
        item = {'labels': label['Name'], 'confidence': round(label['Confidence'], 2)}
        labels.append(item)
    return labels


if __name__ == "__main__":

    _bucket_name = ''
    # celebrity_resp = detect_celebrity(image_uri='')
    # labels_resp = detect_labels(bucket_name=_bucket_name, obj_name='')
