# https://cloud.google.com/vision/docs/detecting-safe-search?hl=ja
from google.oauth2 import service_account
from google.cloud import vision
import io

def detect_safe_search(path: str) -> dict:
    """Detects unsafe features in the file."""
    service_account_file = '/Users/masiro/Downloads/service-account-file.json'
    credentials = service_account.Credentials.from_service_account_file(service_account_file)
    client = vision.ImageAnnotatorClient(credentials=credentials)

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return {
        'adult': safe.adult,
        'medical': safe.medical,
        'spoofed': safe.spoof,
        'violence': safe.violence,
        'racy': safe.racy,
    }
