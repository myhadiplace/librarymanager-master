import pika
import json
from ..models import Book


def main():
    def send_to_rabbitmq(data):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='Books')

        data_json = json.dumps(data)

        channel.basic_publish(exchange="",routing_key='Books',body=data_json)
        print(" [x] Sent 'Hello World!' ")

        connection.close()

    all_books = Book.objects.all()
    books_data = [{'id':str(book.id),'title':book.title,'author':book.author.full_name,'country':book.country.name,'ISBN':book.ISBN,'Genres':book.Genres,'book_image':str(book.book_image.url),'Publication_date':str(book.Publication_date),'price':str(book.price)} for book in all_books]

    send_to_rabbitmq(books_data)