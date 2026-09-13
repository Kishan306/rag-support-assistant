FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
# CPU torch only — the default Linux wheel pulls CUDA and balloons the image.
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Build the vector DB at image build time
RUN python ingest.py

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]