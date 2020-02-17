"""         Набор полезных функций          """
from datetime import datetime


def read_refresh_token():
	"""
	Читает токен из файла refresh_token.txt
	:return:
	token или 0
	"""
	try:
		with open('refresh_token.txt', 'r') as f:
			refresh_token = f.read()
		return refresh_token
	except Exception as e:
		return 0


def write_refresh_token(refresh_token):
	"""
	Записывает токен в файл refresh_token.txt
	:return:
	1 или 0
	"""
	try:
		with open('refresh_token.txt', 'w') as f:
			f.write(refresh_token)
		return 1
	except Exception as e:
		return 0


def convert_timestamp_to_datetime(timestamp):
	return datetime.fromtimestamp(timestamp)
