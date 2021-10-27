import json
from text_converter import to_image
def handler(event, context):
    print(event)
    return {
        'statusCode': 200,
        'Success': to_image(event['files_path'])
    }

