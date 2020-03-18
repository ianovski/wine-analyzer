import boto3
import pandas as pd
import time
import io
from io import BytesIO
import sys
import logging
from botocore.exceptions import ClientError

import math
from PIL import Image, ImageDraw, ImageFont

class aws_textract():

	def __init__(self):
		self.access_key_id  = "ACCESS_KEY_ID"
		self.secret_access_key= "SECRET_ACCESS_KEY"
		self.s3_client = boto3.client('s3',
      region_name="us-east-2",
      aws_access_key_id=self.access_key_id,
      aws_secret_access_key=self.secret_access_key)
		self.s3_resource = boto3.resource('s3',
			region_name="us-east-2",
			aws_access_key_id=self.access_key_id,
			aws_secret_access_key=self.secret_access_key)
		self.textract_client = boto3.client('textract',
			region_name="us-east-2",
			aws_access_key_id=self.access_key_id,
			aws_secret_access_key=self.secret_access_key)

	def upload_file(self, file_name, bucket, object_name=None):
		"""Upload a file to an S3 bucket
			:param file_name: File to upload
    	:param bucket: Bucket to upload to
    	:param object_name: S3 object name. If not specified then file_name is used
    	:return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
		if object_name is None:
			object_name = file_name

    # Upload the file
		try:
			response = self.s3_client.upload_file(file_name, bucket, object_name)
		except ClientError as e:
			logging.error(e)
			return False
		return True

  # Filter word blocks with confidence level > 90%
	def filter_top_words(self,blocks):
		print("Filtering top words...........")
		top_words = []
		for block in blocks:
			if 'Confidence' in block:
				if(block['Confidence']> 90 and block['Text'] not in top_words): # Remove repeated words
					top_words.append(block['Text'])
		return top_words

	def get_text_analysis(self,bucket,document):
		# Get the document from S3
		print("Importing image..........")
		s3_object = self.s3_resource.Object(bucket,document)
		s3_response = s3_object.get()
		stream = io.BytesIO(s3_response['Body'].read())
		image=Image.open(stream)
    
		image_binary = stream.getvalue()
		print('Extracting words..........')
		response = self.textract_client.analyze_document(Document={'Bytes': image_binary},FeatureTypes=["TABLES", "FORMS"])
      
    # Get the text blocks
		blocks=response['Blocks']
		print ('Detected Document Text')

		# Filter words with confidence level > 90%
		top_words = self.filter_top_words(blocks)
		return top_words

	def main(self,bucket,document):
		block_count=self.get_text_analysis(bucket,document)
		seperator = " "
		wine_scanned = seperator.join(block_count)
		return(str(wine_scanned) + " wine enthusiast")

# awstextract = aws_textract()
# awstextract.upload_file("hoya.jpg",'wine-analyzer')
# result = awstextract.main("wine-analyzer","hoya.jpg")
# print(result)

