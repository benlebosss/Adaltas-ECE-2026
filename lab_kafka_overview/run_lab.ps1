# Runs the whole Kafka lab end to end (Windows PowerShell, Docker Desktop started).
# Usage, from this folder:  powershell -ExecutionPolicy Bypass -File .\run_lab.ps1
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "== 1. Python virtual environment + confluent-kafka"
if (-not (Test-Path .venv)) { python -m venv .venv }
$py = ".\.venv\Scripts\python.exe"
& $py -m pip install -q confluent-kafka

Write-Host "== 2. Kafka broker (Docker)"
docker pull apache/kafka-native:4.1.1
docker rm -f kafka-lab 2>$null | Out-Null
docker run -d --name kafka-lab -p 9092:9092 apache/kafka-native:4.1.1
Start-Sleep -Seconds 10

try {
  Write-Host "== 3. Demo: admin.py / producer.py (20 s) / consumer.py"
  & $py admin.py
  $prod = Start-Process -FilePath $py -ArgumentList "producer.py" -PassThru -NoNewWindow
  Start-Sleep -Seconds 20
  Stop-Process -Id $prod.Id -Force
  & $py consumer.py

  Write-Host "== 4. Lab: book-lines"
  if (-not (Test-Path book.txt)) {
    Invoke-WebRequest "https://www.gutenberg.org/cache/epub/1342/pg1342.txt" -OutFile book.txt
  }
  & $py admin_book.py
  & $py producer_book.py
  & $py consumer_book.py

  Write-Host "== 5. First 10 lines of cleaned.txt"
  Get-Content cleaned.txt -TotalCount 10
  Write-Host ("cleaned.txt: {0} lines" -f (Get-Content cleaned.txt).Count)
}
finally {
  Write-Host "== 6. Stop and remove the container"
  docker stop kafka-lab | Out-Null
  docker rm kafka-lab | Out-Null
}
