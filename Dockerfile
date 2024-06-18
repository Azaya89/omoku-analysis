FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN python3 -m pip install --no-cache-dir --upgrade pip
RUN python3 -m pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

RUN mkdir /.cache .chroma && chmod 777 /.cache .chroma

CMD ["panel", "serve", "/code/app.py", "--address", "0.0.0.0", "--port", "7860",  "--allow-websocket-origin", "*"]