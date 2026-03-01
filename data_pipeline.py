
from dotenv import load_dotenv
import os

load_dotenv("guesty.env")

guesty_client_ID = os.getenv("CLIENT_ID")
guesty_client_secret = os.getenv("CLIENT_SECRET")

 