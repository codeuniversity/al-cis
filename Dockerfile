FROM python:3.7.2-slim
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r prod-requirements.txt
CMD [ "python", "./main.py" ]
EXPOSE 5000
