import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TICKETMASTER_API_KEY")
BASE_URL = os.getenv("BASE_URL")
PREDICTHQ_API_KEY = os.getenv("PREDICTHQ_API_KEY")
