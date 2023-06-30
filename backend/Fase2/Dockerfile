FROM  python:3.10
WORKDIR /Fase2
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 3800
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=3800"]