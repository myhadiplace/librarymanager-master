from django.contrib.sessions.models import Session
from abc import ABC ,abstractmethod
import random
from datetime import datetime,timedelta
from .circuit_breaker import CircuitBreaker
import random

kavenagar_cb = CircuitBreaker(filure_threshold=3,reset_timeout=1800)
hamkaran_cb = CircuitBreaker(filure_threshold=3,reset_timeout=1800)
signal_cb = CircuitBreaker(filure_threshold=3,reset_timeout=1800)
faraz_cb = CircuitBreaker(filure_threshold=3,reset_timeout=1800)

class ServiceIntrupted(Exception):
    def __init__(self, message):
        super().__init__(message)


class OTPService(ABC):
    @abstractmethod
    def send_otp(self):
        pass

class KavehNegarService(OTPService):
    def send_otp(self,username):
        result = kavenagar_cb.execution()
        if result:
            return random.randint(1000,9999)
        else:
            raise ServiceIntrupted('service temprory intrupted')

class SignalService(OTPService):
    def send_otp(self,username):
        result = signal_cb.execution()
        if result:
            return random.randint(1000,9999)
        else:
            raise ServiceIntrupted('service temprory intrupted')
    
class HamkaranSmsService(OTPService):
    def send_otp(self,username):
        result = hamkaran_cb.execution()
        if result:
            return random.randint(1000,9999)
        else:
            raise ServiceIntrupted('service temprory intrupted')

class FarazSmsService(OTPService):
    def send_otp(self,username):
        result = faraz_cb.execution()
        if result:
            return random.randint(1000,9999)
        else:
            raise ServiceIntrupted('service temprory intrupted')   

class OTPManager:
    def __init__(self):
        self.smsservices = [FarazSmsService,SignalService,HamkaranSmsService,KavehNegarService]
        self.signalservice = SignalService()

    def send_otp(self,username):
        sended = False
        while not sended:
            try:
                selected_service = random.choice(self.smsservices)
                selected_service.send_otp(username)

            except Exception:
                selected_service = random.choice(self.smsservices)
                selected_service.send_otp()
            else:
                sended = True

def check_two_minute_limit(request,time_diff,user_id):
        user_session = request.session.get(f'user_{user_id}_data')
        now = datetime.now()
        two_minutes = timedelta(minutes=2)
        two_minutes_otp_counter = user_session['two_minutes_otp_counter']
        if two_minutes_otp_counter >= 5:
            if time_diff >= two_minutes:
                user_session['one_hours_otp_counter'] += 1
                user_session['two_minutes_otp_counter'] = 1
                user_session['last_time_code_send'] = now.isoformat()
                print('user can get code!!!')
                return user_session
            else:
                print('try again after 2 minutes')
                return False
        else:
            user_session['one_hours_otp_counter'] += 1
            user_session['two_minutes_otp_counter'] += 1
            user_session['last_time_code_send'] = now.isoformat()
            print('user can get code!!!')
            return user_session


def check_opt_limit(request,user_id):
    user_session = request.session.get(f'user_{user_id}_data')
    print('user session_____:',user_session)
    now = datetime.now()
    last_code_time = datetime.fromisoformat(user_session['last_time_code_send'])
    one_hours = timedelta(hours=1)
    time_diff = now - last_code_time
    if user_session['one_hours_otp_counter'] >= 10:
        print('33')
        if time_diff > one_hours:
            result = check_two_minute_limit(request,time_diff,user_id)
            if result:
                request.session[f'user_{user_id}_data'] = result
                return True
            else:
                return False
        else:
            print('try again after 1 hours')
            return False
    else:
        result = check_two_minute_limit(request,time_diff,user_id)
        if result:
            request.session[f'user_{user_id}_data'] = result
            return True
        else:
            print('55')
            return False
       

