# %%
import re
from confluent_kafka import Consumer

# %%
conf = {'bootstrap.servers': 'localhost:9092',
        'group.id': 'book-cleaner',
        'auto.offset.reset': 'earliest'}

consumer = Consumer(conf)

# %%
topic='book-lines'
consumer.subscribe([topic])
output_path='cleaned.txt'

# %% Text cleaning (inspired by the word count lab)
def clean(line):
  line = line.lower()                    # b. lower case
  line = re.sub(r'[^a-z\s]', ' ', line)  # f. remove punctuation and digits
  return line.split()                    # tokenize, drops blank spaces

# %%
# Configuration
MAX_EMPTY_POLLS = 10  # Ends after ~10 seconds of silence
MAX_ERRORS = 5        # Ends after 5 consecutive errors
empty_polls = 0
error_count = 0
received = 0

with open(output_path, 'w', encoding='utf-8') as out:
  while True:
    msg = consumer.poll(1.0)

    # 1. Handle "No Message" (Timeout)
    if msg is None:
      empty_polls += 1
      if empty_polls >= MAX_EMPTY_POLLS:
        print("Closing: No new messages received.")
        break
      continue

    # 2. Handle Errors
    if msg.error():
      error_count += 1
      print(f"Consumer error: {msg.error()}")
      if error_count >= MAX_ERRORS:
        print("Closing: Too many consecutive errors.")
        break
      continue

    # 3. Handle Success
    empty_polls = 0
    error_count = 0
    received += 1

    words = clean(msg.value().decode('utf-8'))
    if words:
      out.write(' '.join(words) + '\n')

# Clean up
consumer.close()
print(f"{received} messages processed, result written to {output_path}")
