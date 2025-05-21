FROM python:3.13
RUN apt-get update && apt-get install -y \
    git \
    tesseract-ocr \
    tesseract-ocr-chi-tra \
    libtesseract-dev \
    poppler-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9050", "--reload"]