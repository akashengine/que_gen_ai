from pypdf import PdfReader
from pdf2image import convert_from_bytes
import requests
import os
from io import BytesIO

def pdf_to_images(pdf_file):
    pdf_bytes = pdf_file.read()
    return convert_from_bytes(pdf_bytes, dpi=300)

def upload_to_imgbb(image):
    api_key = os.getenv('IMGBB_API_KEY')
    url = "https://api.imgbb.com/1/upload"
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    image_bytes = buffered.getvalue()
    response = requests.post(
        url,
        params={'key': api_key},
        files={'image': image_bytes}
    )
    if response.status_code == 200:
        return response.json()['data']['url']
    else:
        raise Exception(f"Failed to upload image: {response.text}")

def process_pdf(pdf_file):
    images = pdf_to_images(pdf_file)
    image_urls = []
    for image in images:
        image_url = upload_to_imgbb(image)
        image_urls.append(image_url)
    return image_urls
