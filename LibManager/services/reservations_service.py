from ..models import Reservation
from ..repository.repository import get_user_reservation
from datetime import datetime,timedelta

def off_check(user_id):
    '''get user object as argument and check if user reserve more than 3 books or not. then it calculate 30% off on total cost '''
    now = datetime.now()
    one_month = timedelta(days=31)
    past_month = now - one_month
    user_reserve = get_user_reservation(user_id)
    total_reserve = 0
    for reserve_date in user_reserve.reserved_start_data:
        if reserve_date >= past_month:
            total_reserve += 1
    if total_reserve > 3:
        return True
    

def free_check(user_id):
    '''get user object as an argument and if user pay more than 300,000 in past two month the total cost is free and function return True otherwise it return None'''
    now = datetime.now()
    two_month = timedelta(days=30)
    past_two_month = now - two_month
    user_reserve = get_user_reservation(user_id)
    total_cost = 0
    for cost in user_reserve.cost:
        if user_reserve.reserve_start_date > past_two_month:
            total_cost += cost
    if total_cost >= 300000:
        return True


def cost_calculater(user_id,reserve_day,membership_type):
    '''calculate the cost of user reserve by take user id, How many days has the book been reserved, and what is user membership and return a number'''
    reserve_cost = int(reserve_day) * 1000
    if membership_type == 'vip':
         reserve_cost = 0
         return reserve_cost

    if free_check(user_id):
        reserve_cost = 0
        return reserve_cost

    if off_check(user_id):
        reserve_cost = reserve_cost - (reserve_cost * 0.3)
        return reserve_cost



