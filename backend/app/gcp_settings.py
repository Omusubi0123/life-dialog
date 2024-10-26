import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore, storage

from app.settings import settings

cred = credentials.Certificate(settings.firebase_credential)
firebase_app = firebase_admin.initialize_app(cred)

db = firestore.Client()
storage_client = storage.Client()
