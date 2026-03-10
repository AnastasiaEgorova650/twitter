FROM python:3.12-slim
WORKDIR /home
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt src/
RUN pip install --upgrade pip
RUN pip install -r /home/src/requirements.txt

COPY src src/
COPY tests tests/
COPY static static/
COPY pyproject.toml /home

EXPOSE 8000

CMD ["fastapi", "run", "src/main.py", "--host", "0.0.0.0", "--port", "8000"]
