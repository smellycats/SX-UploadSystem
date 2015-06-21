#from iniconf import MyIni
from my_logger import debug_logging, online_logging
from app import app, db
from models import Users, Upload
import views
from main import Uploader, History, Digger

__version__ = '0.1.0'
