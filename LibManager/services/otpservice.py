from django.contrib.sessions.models import Session
from abc import ABC ,abstractmethod
import random
from datetime import datetime,timedelta
import random
#redis configuration
import redis
redis_host = '192.168.1.10'
redis_port = '6379'
redis_password = 'default'

redis_db = redis.Redis(host=redis_host, port=redis_port, password=redis_password)

ALL_SERVICES = ['kavenegar','hamkaran','signal','faraz']


class ServiceIntrupted(Exception):
    def __init__(self, message):
        super().__init__(message)

class OTPService(ABC):
    @abstractmethod
    def send_otp(self):
        pass

class KavehNegarService(OTPService):
    def send_otp(self,username):
        try:
            return random.randint(1000,9999)
        except Exception:
            raise Exception

class SignalService(OTPService):
    def send_otp(self,username):
        try:
            return random.randint(1000,9999)
        except Exception:
            raise Exception

class HamkaranService(OTPService):
    def send_otp(self,username):
        try:
            return random.randint(1000,9999)
        except Exception:
            raise Exception

class FarazService(OTPService):
    def send_otp(self,username):
        try:
            return random.randint(1000,9999)
        except Exception:
            raise Exception


redis_db.set("kavenagar",0) #add set to database
redis_db.set('hamkaran',0)
redis_db.set('signal',0)
redis_db.set('faraz',0)

def get_unavailable_services():
    unavalible_list = []
    for services in ALL_SERVICES:
        is_unavalible = redis_db.get(services+"_is_unavaliable")
        if is_unavalible is not None:
            is_unavalible = is_unavalible.decode('utf-8') #return 0 or 1
            if int(is_unavalible):
                unavalible_list.append(services)
    return unavalible_list


#list all servies, get unavilable_services from redis, remove unavilable service from list and select randomly one service       
def select_service():
    '''select a service between all avilable services and return a random service'''
    all_services = ALL_SERVICES[:]
    unaviliable_service = get_unavailable_services()
    if unaviliable_service:
        set_all_service = set(all_services)
        set_unavilable_service = set(unaviliable_service)
        available_service = set_unavilable_service - set_all_service
    selected = random.choice(available_service)
    return selected

#in fact this piece of code get service name and finde coresponding data of this service that hold failure threshold
# it get failure threshold of this service and return a hash and we decoded it to utf-8.
#then if threshold was => we add service name to unavilable_service set in redis
#finally we add 30 minute expire time for it
def add_to_unavilable_service(servicename):
    '''this function get service name and block service'''
    redis_db.set(servicename+"_is_unavaliable",0)
    redis_db.expire(servicename,1800)
    
 

#this function first get set(data document) of service from redis. check if failure count of this service is equal or
# greater than 3 or not. if it was then it check for last time code sended.if more than 30 minute ago .
#function will return true otherwise it return False this mean that service still unavilable
def check_service_availability(servicename):
    '''get service name return 'available' if service should be avilable,return 'unavailable' if service is should unavilable'''
    is_unavalible = redis_db.get(servicename+"_is_unavaliable") #return 0 or 1
    if is_unavalible is not None:
        is_unavalible = is_unavalible.decode('utf-8')
        if int(is_unavalible):
            return 'unavailable'
        else:
            return 'available'

#this function increase the value of failure_threshold in service set of specefic service in redis
def increase_failure_threshold(servicename):
    '''get service name and increase failure of the service'''
    redis_db.incr(servicename)

def reset_service_data(servicename):
    redis_db.delete(servicename)
    redis_db.set(servicename,0)
    
#this function call select_service and select_service randomly return an avilable serviece name
# and function try to use this random selected service to send otp code and if service not respond 
# the increase_failure_threshold function get executed and if there is no error reset_service_data would
#be called and thereshold of service became 0 and last time code sended become now
def otp_manager():
    service = select_service()
    try:
        service.send_otp()

    except Exception:
        increase_failure_threshold(service)
        if check_service_availability(service) == 'unavilable':
            add_to_unavilable_service(service)
    else:
        reset_service_data(service)






















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
            return False