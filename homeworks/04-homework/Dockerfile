FROM svizor/zoomcamp-model:mlops-3.10.0-slim

COPY starter.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "starter.py"]
CMD ["2022", "4"]
