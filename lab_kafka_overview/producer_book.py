# %%
import socket
from confluent_kafka import Producer

# %%
conf = {'bootstrap.servers': 'localhost:9092',
        'client.id': socket.gethostname()}

producer = Producer(conf)

# %%
topic='book-lines'
book_path='book.txt'  # Pride and Prejudice, Project Gutenberg (pg1342.txt)

# %% Send every non-empty line of the book to the topic
sent = 0
with open(book_path, encoding='utf-8-sig') as book:
  for line in book:
    line = line.strip()
    if not line:
      continue
    producer.produce(topic=topic, value=line.encode('utf-8'))
    producer.poll(0)  # serve delivery callbacks / free the local queue
    sent += 1

producer.flush()
print(f"{sent} lines sent to topic '{topic}'")
