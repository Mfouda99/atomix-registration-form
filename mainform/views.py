from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from .models import Registrationform
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
import tempfile
import os
import shutil
from io import BytesIO
from googleapiclient.http import MediaIoBaseUpload


# Google Sheets API Setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = r'C:\Users\genge\OneDrive\Desktop\atomix-24-form-da94ac11c803.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build('sheets', 'v4', credentials=credentials)
drive_service = build('drive', 'v3', credentials=credentials)

SPREADSHEET_ID = '1VLg_K9m2UH57Dwn7c0n3YCRObNNq3kFMqYmPmkPVFcY'
RANGE_NAME = 'Sheet1!A1'


def upload_to_drive(file):
    """Upload a file to Google Drive and return the file's link."""
    try:
        # Create a BytesIO object for in-memory file
        file_io = BytesIO(file.read())
        
        # Prepare the MediaIoBaseUpload object
        media = MediaIoBaseUpload(file_io, mimetype=file.content_type)
        
        # Upload the file to Google Drive
        request = drive_service.files().create(media_body=media, body={'name': file.name})
        file_metadata = request.execute()

        # Get the file ID and generate a link to it
        file_id = file_metadata.get('id')
        file_link = f"https://drive.google.com/drive/folders/1RG1xy1143dbhpAxscAe3v7jK9WZetkvN?usp=sharing"
        
        return file_link
    except Exception as e:
        print(f"Error uploading file to Google Drive: {e}")
        return None
    

def register(request):
    if request.method == 'POST':
        # Collect form data
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        position = request.POST.get('position')
        function = request.POST.get('function')
        id_front = request.FILES.get('id_front')
        id_back = request.FILES.get('id_back')
        indemnity_form = request.FILES.get('indemnity_form')
        personal_photo = request.FILES.get('personal_photo')

        # Save the Registrationform instance
        data = Registrationform(
            full_name=full_name,
            phone_number=phone_number,
            email=email,
            position=position,
            function=function,
            id_front=id_front,
            id_back=id_back,
            indemnity_form=indemnity_form,
            personal_photo=personal_photo
        )
        data.save()

        # Upload files to Google Drive and get the file links
        id_front_link = upload_to_drive(id_front) if id_front else "No ID Front Uploaded"
        id_back_link = upload_to_drive(id_back) if id_back else "No ID Back Uploaded"
        indemnity_form_link = upload_to_drive(indemnity_form) if indemnity_form else "No Indemnity Form Uploaded"
        personal_photo_link = upload_to_drive(personal_photo) if personal_photo else "No Personal Photo Uploaded"

        # Prepare data to send to Google Sheets
        values = [
            [full_name, phone_number, email, position, function, id_front_link, id_back_link, indemnity_form_link, personal_photo_link]
        ]

        body = {
            'values': values
        }

        # Update the Google Sheet
        try:
            sheet = service.spreadsheets()
            result = sheet.values().append(
                spreadsheetId=SPREADSHEET_ID,
                range=RANGE_NAME,
                valueInputOption="RAW",
                body=body
            ).execute()
            print("Successfully appended to Google Sheets")
        except Exception as e:
            print("Error appending to Google Sheets:", e)

        # Redirect to success page after saving
        return render(request, 'success.html', {'form': 'form'})
    
    else:   
        # If not POST, render the registration form
        return render(request, 'register.html', {'form': 'form'})

def register_success(request):
    return render(request, 'success.html', {'form': 'form'})
