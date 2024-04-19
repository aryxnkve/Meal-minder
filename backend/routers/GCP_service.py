from fastapi import APIRouter, HTTPException, Response
from dotenv import dotenv_values
from fastapi import FastAPI, File, UploadFile

from fastapi.responses import JSONResponse

import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import logging
from utils.util import generate_file_name, is_pdf
import asyncio

router = APIRouter()

config = dotenv_values(".env")

# Create an S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=config["S3_ACCESS_KEY"],
    aws_secret_access_key=config["S3_SECRET_KEY"],
    region_name=config["S3_REGION"]
)

# @router.post("/upload_s3/")
# async def upload_file(file_obj: UploadFile = File(...)):
#     if not is_pdf(file_obj.filename):
#         raise HTTPException(status_code=400, detail="Only PDF files are allowed")
#     try:
#         # Upload the file to S3
#         config = dotenv_values(".env")
#         S3_BUCKET_NAME = config["S3_BUCKET_NAME"]
#         folder_name = config["S3_UPLOAD_PDF_FOLDER"]
#         print(S3_BUCKET_NAME,folder_name,file_obj.file)
#         print("filename = ", file_name)
#         success = upload_file_to_bucket(file_obj.file, S3_BUCKET_NAME,folder_name, file_name)
#         print("Uploaded ", file_name, " to S3 bucket")
#         if success:
#             print("Uploaded ", file_name, " to S3 bucket")
#             s3_link = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{folder_name}/{file_name}"
#             print("s3_link to access the file", s3_link)
#             return {"status": "Success", "message": "File uploaded successfully", "s3_link": s3_link}
#         else:
#             return {"status": "Failure", "error": "Some error occurred"}
#     except NoCredentialsError:
#         return {"status": "Failure", "error": "AWS credentials not found or invalid"}
#     except Exception as e:
#         print("------>",e)
#         return {"status": "Failure", "error": "Something went wrong"}

@router.post("/upload_s3_2/")
async def upload(file_obj: UploadFile = File(...) ):
    loop = asyncio.get_event_loop()
    # Use a thread pool to handle the synchronous S3 upload function
    t = await loop.run_in_executor(
        None,  # None uses the default executor (ThreadPoolExecutor)
        upload_file_to_s3,
        file_obj.filename,
        file_obj.file,  # Pass file content or a BytesIO object
    )
    return t 

def upload_file_to_s3(filename, file_obj: UploadFile = File(...)):
    #  filename, bucket_name, s3_folder, access_key, secret_key, region
    # Create an S3 client
    config = dotenv_values(".env")
    bucket_name = config["S3_BUCKET_NAME"]
    s3_folder = config["S3_UPLOAD_PDF_FOLDER"]
    access_key = config["S3_ACCESS_KEY"]
    secret_key = config["S3_SECRET_KEY"]
    region =config["S3_REGION"]
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region)
    s3_object_key = f"{s3_folder}/{filename}"
    print(s3_object_key)
    # Check if the file already exists in S3
    try:
        s3.head_object(Bucket=bucket_name, Key=s3_object_key)
        print(f"File {filename} already exists in S3. Overwriting...")
    except s3.exceptions.ClientError as e:
        pass  # We'll proceed to upload since the file doesn't exist

    # Upload the file-like object to S3
    try:
        s3.upload_fileobj(file_obj, bucket_name, s3_object_key)
        print(f"File {filename} uploaded successfully to S3: s3://{bucket_name}/{s3_object_key}")
        return JSONResponse(content={"status": "Success", "message": f" file upload successful."}, status_code=200)

    except Exception as upload_error:
        print(f"Error uploading file {filename} to S3: {upload_error}")
        return JSONResponse(content={"status": "Failure", "message": f"Failed to upload file"}, status_code=400)


