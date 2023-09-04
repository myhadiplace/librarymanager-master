from django.db import models
from django_countries.fields import CountryField

# Create your models here.
GENERS = [('biography','Biography'),('science','Science'),('business','Business'),('history','History'),('romance','Romance'),('fiction','Fiction'),('fantasy','Fantasy'),('poetry','Poetry'),('science fiction','Science Fiction'),('novel','Novel'),('psychology','Psychology'),('self help','Self Help'),("children's'","Children's'")]

class Author(models.Model):
    full_name = models.CharField(max_length=100)
    birth_country = CountryField()

    def __str__(self):
        return f'{self.full_name}'

class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.ForeignKey(Author,on_delete=models.CASCADE,null=True)
    country = CountryField(null=True)
    ISBN = models.CharField(max_length=20)
    Genres = models.CharField(choices=GENERS)
    book_image = models.ImageField(upload_to="book images",default='')
    Publication_date = models.DateField()
    price = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f'{self.title} by {self.author}'


class Users(models.Model):
    full_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=100)
    membership_type = models.CharField(choices=[('vip',"VIP"),('normal','Normal')])

class Reservation(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    reserved_start_data = models.DateField(auto_now_add=True)
    reserve_end = models.DateField()
    cost = models.IntegerField(null=True)


