import pika,sys,os
import json
from pymongo import MongoClient


def store_book_in_db(data):
    cluster = "mongodb://localhost:27017"
    client = MongoClient(cluster)
    db = client.library
    loaded_data = json.loads(data)
    try:
        db.book.insert_many(loaded_data)
    except:
        print('error while inset documents')
        return False

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='Books')

    def callback(ch,method,properties,body):
    
        store_book_in_db(body)
        print('data successfuly added')

    channel.basic_consume(queue='Books',auto_ack=True,on_message_callback=callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os.__exit(0)


