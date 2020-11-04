FROM alpine:3.12

RUN apk add --no-cache python3-dev \
	&& apk add python3 py3-pip \
	&& apk add --no-cache --update python3 \
	&& pip3 install --upgrade pip 


EXPOSE 6379
WORKDIR /app

COPY . /app
RUN pip3 --no-cache-dir install -r requirements.txt

CMD ["python3","src/app.py"]