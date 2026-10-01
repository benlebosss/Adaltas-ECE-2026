# Lab 4 – Kafka overview

Subject: [04.kafka_overview/lab.md](https://github.com/adaltas/ece-big-data-processing-fall-2026/blob/main/04.kafka_overview/lab.md)

## Files

| File | Role |
|---|---|
| `admin.py`, `producer.py`, `consumer.py` | Original demo (topic `timer`) |
| `admin_book.py` | Creates the topic `book-lines` |
| `producer_book.py` | Reads `book.txt` (Pride and Prejudice, Project Gutenberg) line by line and sends every non-empty line to `book-lines` |
| `consumer_book.py` | Reads `book-lines` from the beginning (`auto.offset.reset=earliest`), cleans each message and writes it to `cleaned.txt`; stops after 10 s without a new message |
| `run_lab.ps1` | Runs everything end to end on Windows |

## Text cleaning (inspired by the word count lab)

1. lower case
2. punctuation and digits removed (`[^a-z\s]` replaced by a space)
3. tokenisation into words (`split()`, which also drops blank spaces)

One output line per message, words separated by a single space.

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate   |   Linux/macOS: source .venv/bin/activate
pip install confluent-kafka

docker pull apache/kafka-native:4.1.1
docker run -d --name kafka-lab -p 9092:9092 apache/kafka-native:4.1.1

# Demo
python admin.py
python producer.py      # runs 5 min, Ctrl+C to stop earlier
python consumer.py

# Lab
curl -o book.txt https://www.gutenberg.org/cache/epub/1342/pg1342.txt
python admin_book.py
python producer_book.py
python consumer_book.py

docker stop kafka-lab && docker rm kafka-lab
```

Or on Windows: `powershell -ExecutionPolicy Bypass -File .\run_lab.ps1`
