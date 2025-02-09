import pika, os, json, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mscore.settings")
django.setup()

from products.models import Product

params = pika.URLParameters('amqps://mmztoxid:TQVZqXcDQ_flhn9wAFD0WtxsnSfjiF1Q@hawk.rmq.cloudamqp.com/mmztoxid')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')

def callback(ch, method, properties, body):
    print("Receive in admin")
    data = json.loads(body)
    print(data)
    product = Product.objects.get(id=data)
    product.likes = product.likes + 1
    product.save()
    print('Product likes increased')


channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('Started consuming')

channel.start_consuming()

channel.close()