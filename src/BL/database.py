import json
import requests
from kivymd.uix.snackbar import Snackbar
from kivymd.app import MDApp
from BL.utils import write_refresh_token
from datetime import datetime
import time
import threading


class DataBase:
    url = 'https://idoc-af7a0.firebaseio.com/'
    auth_key = 'AIzaSyAhdZTWK82KOcW60skjykCuFxHZBUimWHc'  # Web Api Key
    app_instance = None
    config = {
        'apiKey': 'AIzaSyAhdZTWK82KOcW60skjykCuFxHZBUimWHc',
        "authDomain": "idoc-af7a0.firebaseapp.com",
        "databaseURL": "https://idoc-af7a0.firebaseio.com",
        "storageBucket": "idoc-af7a0.appspot.com"
    }

    def __init__(self, *args):
        super().__init__(*args)
        self.app_instance = MDApp.get_running_app()

    """             МЕТОДЫ АВТОРИЗАЦИИ ПОЛЬЗОВАТЕЛЕЙ           """

    # Регистрация (Готово)
    def register_user(self, email, password, name, cb):

        # Создаем запрос регистрации на сервер
        url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=" + self.auth_key
        payload = {'email': email, 'password': password, 'returnSecureToken': True}
        request = requests.post(url, data=payload)
        user = json.loads(request.content.decode())

        if not request.ok:
            error_message = user['error']['message']
            Snackbar(text=error_message).show()
            return 0

        self.app_instance.local_id = user['localId']
        self.app_instance.id_token = user['idToken']
        if not write_refresh_token(user['refreshToken']):
            Snackbar(text='Не удалось записать токен').show()

        data_to_upload = {
            'name': str(name),
            'userType': 'Доктор' if cb else 'Пациент',
            'email': user['email'],
        }
        # Теперь необходимо записать данные пользователя в БД
        patch_result = self.patch_account_data(data_to_upload)

        if not patch_result:
            Snackbar(text='Не удалось записать данные на сервер').show()
            return 0

        # Далее заполняем все оставшиеся данные о пользователе
        self.app_instance.user_data['name'] = name
        self.app_instance.user_data['email'] = email

        Snackbar(text='{}, регистрация прошла успешно'.format(name)).show()
        self.app_instance.sm.current = 'main'

    # Вход по email и паролю (готово)
    def login(self, email, password):

        # Создаем запрос входа на сервер
        url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=" + self.auth_key
        payload = {"email": email, "password": password, "returnSecureToken": True}
        request = requests.post(url, data=payload)
        user = json.loads(request.content.decode())

        if not request.ok:
            error_message = user['error']['message']
            Snackbar(text=error_message).show()
            return 0

        self.app_instance.local_id = user['localId']
        self.app_instance.id_token = user['idToken']
        if not write_refresh_token(user['refreshToken']):
            Snackbar(text='Не удалось записать токен').show()

        user_data = self.get_user_data_all(self.app_instance.user_data)

        if not user_data:
            return 0

        self.app_instance.user_data = user_data
        Snackbar(text='Авторизация прошла успешно').show()
        self.app_instance.sm.current = 'main'

    # Вход по токену (готово)
    def login_refresh_token(self, refresh_token):
        tokens = self.exchange_refresh_token(refresh_token=refresh_token)

        if not tokens:
            Snackbar(text='Не удалось подключиться к сети').show()
            return 0

        # Если удалось восстановить токены
        self.app_instance.local_id = tokens['user_id']
        self.app_instance.id_token = tokens['id_token']

        # Далее получаем данные о пользователе
        user_data = self.get_user_data_all(self.app_instance.user_data)

        if not user_data:
            return 0
        self.app_instance.user_data = user_data
        return 1

    # Выход из аккаунта (Готово)
    def sign_out(self):
        write_refresh_token('none')
        self.app_instance.local_id = ''
        self.app_instance.id_token = ''
        self.app_instance.user_data = {}
        self.app_instance.sm.current = 'start'

    def send_reset_password_key(self, email):
        # Создаем запрос отправки пароля
        url = 'https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key=' + self.auth_key
        data = {'email': email, 'requestType': 'PASSWORD_RESET'}
        request = requests.post(url=url, data=data)
        if request.ok:
            Snackbar(text='Письмо успешно отправлено').show()
            return 1
        else:
            Snackbar(text='Не удалось отправить письмо').show()
            return 0

    def exchange_refresh_token(self, refresh_token):
        url = "https://securetoken.googleapis.com/v1/token?key=" + self.auth_key
        payload = json.dumps({"grant_type": "refresh_token", "refresh_token": str(refresh_token)})
        try:
            request = requests.post(url, data=payload)
        except Exception as e:
            print(e)
            return 0

        if not request.ok:
            return 0

        return {'id_token': request.json()['id_token'], 'user_id': request.json()['user_id']}

    """             ДЕЙСТВИЯ С АККАНУТОМ ПОЛЬЗОВАТЕЛЯ           """

    # Опубликовать данные об аккаунте польователя
    def patch_account_data(self, data):
        data = json.dumps(data)
        request = requests.patch(self.url + 'users/' + self.app_instance.local_id + '/account/' + '.json?auth=' + self.app_instance.id_token, data=data)
        if request.ok:
            return 1
        else:
            return 0

    # Возвращает полную информацию о пользователе
    def get_user_data_all(self, old_data):
        user_data = {}

        # # Получаем email пользователя
        # if 'email' not in old_data:
        #     print("Загружаем данные об email")
        #     url = "https://identitytoolkit.googleapis.com/v1/accounts:lookup?key=" + self.auth_key
        #     data = {'idToken': self.app_instance.id_token}
        #     request = requests.post(url=url, data=data)
        #
        #     if not request.ok:
        #         return 0
        #
        #     request_result = json.loads(request.content.decode())['users'][0]
        #
        #     # Заполняем общий словарь данных о пользователе если email еще не заполнен
        #     user_data['email'] = request_result['email']

        # Далее получаем данные из БД об аккаунте пользователя
        print("Загружаем данные об аккаунте")
        request = requests.get(self.url + 'users/' + self.app_instance.local_id + '/account/' + '.json?auth=' + self.app_instance.id_token)

        if request.ok:
            user_account = json.loads(request.content.decode())
            user_data = {**user_data, **user_account}

        # Получаем данные  из БД о тестированиях
        print("Загружаем данные о тестированиях")
        request = requests.get(self.url + 'users/' + self.app_instance.local_id + '/testing/' + '.json?auth=' + self.app_instance.id_token)
        user_testing = json.loads(request.content.decode())

        if request.ok and user_testing:
            user_data = {**user_data, **user_testing}

        print("User Data: \n{}".format(user_data))
        return user_data

    """             ДЕЙСТВИЯ С ЕЖЕДНЕВНЫМИ ТЕСТИРОВАНИЯМИ           """

    # Обновить время последнего теста
    def patch_last_testing_time(self, timestamp):
        to_upload = json.dumps({'lastTestingTime': timestamp})
        request = requests.patch(self.url + 'users/' + self.app_instance.local_id + '/testing/' + '.json?auth=' + self.app_instance.id_token,
                                 data=to_upload)
        if request.ok:
            return 1
        else:
            return 0

    def patch_new_testing_data(self, data, timestamp):
        to_upload = json.dumps(data)
        request = requests.patch(
            self.url + 'users/' + self.app_instance.local_id + '/testing/data/' + str(timestamp) + '/.json?auth=' + self.app_instance.id_token,
            data=to_upload)
        if request.ok:
            return 1
        else:
            return 0

    # Сохранить данные о тестировании в БД
    def patch_daily_testing(self, data):

        timestamp = int(datetime.today().timestamp())

        # Записываем данные о новом тестировании
        if not self.patch_new_testing_data(data, timestamp):
            return 0

        # Записываем данные о последнем тестировании
        if not self.patch_last_testing_time(timestamp):
            return 0

        return timestamp

    """             ДЕЙСТВИЯ В РОЛИ ДОКТОРА           """

    # Добавить пациента в свой список
    def add_patient(self, patient_local_id):

        # Ищем пациента по local_id
        request = requests.get(self.url + 'users/' + patient_local_id + '/account/' + '.json?auth=' + self.app_instance.id_token)
        patient = json.loads(request.content.decode())

        if not request.ok or not patient:
            print('Не удалось найти такого пользователя')
            return 0

        to_upload = json.dumps({patient_local_id: patient['name']})
        request = requests.patch(
            self.url + 'users/' + self.app_instance.local_id + '/patients_list/' + '/.json?auth=' + self.app_instance.id_token,
            data=to_upload
        )

        if not request.ok:
            return 0

        to_upload = json.dumps({'doctor_id': self.app_instance.local_id})
        request = requests.patch(
            self.url + 'users/' + patient_local_id + '/doctor/' + '/.json?auth=' + self.app_instance.id_token,
            to_upload
        )

        if not request.ok:
            return 0

        return 1

    # Получить данные о всех своих пациентах
    def get_patients_info(self):
        # TODO: Проверка на роль доктора/пациента

        request = requests.get(self.url + 'users/' + self.app_instance.local_id + '/patients_list/' + '.json?auth=' + self.app_instance.id_token)
        result = json.loads(request.content.decode())

        for key, value in result.items():
            request = requests.get(self.url + 'users/' + key + '/account/' + '.json?auth=' + self.app_instance.id_token)
            patient = json.loads(request.content.decode())
            result[key] = patient
        return result
