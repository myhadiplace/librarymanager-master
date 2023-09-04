from django.contrib import admin
from .models import Book,Users,Reservation,Author
# Register your models here.
admin.site.register(Book)
admin.site.register(Users)
admin.site.register(Reservation)
admin.site.register(Author)