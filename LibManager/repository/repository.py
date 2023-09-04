from ..models import Users,Book,Reservation
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

def get_user_by_username(username):
    try:
        user_obj = Users.objects.get(username=username)
    except ObjectDoesNotExist:
        return {'error':'invalid username'}
    else:
        return user_obj



def get_book_by_filters(genre=None,author_country=None,price_max=None,price_min=None):
    query = Q()
    if genre:
        query &= Q(Genres=genre)
    if author_country:
        query &= Q(country= author_country)
    if price_max:
        query &= Q(price_max=price_max)
    if price_min:
        query &= Q(price_min=price_min)
    try:
        books_obj = Book.objects.filter(query)
        return books_obj
    
    except ObjectDoesNotExist:
        return {'error':'no result founded'}
    
    except Exception as e:
        return {'error':e}


def get_user_reservation(user_id):
    user_reserve = Reservation.objects.filter(user=user_id)
    return user_reserve


def get_uesr_reserved_book(user_id):
    try:
        user_obj = Users.objects.get(pk=user_id)
        reservations = Reservation.objects.filter(user=user_obj.id)
        books = [reservation.book for reservation in reservations]
        return {'books':books}
    except ObjectDoesNotExist:
        return {'error':'no book reserve founded'}   
