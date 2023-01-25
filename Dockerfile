FROM python:3.9.6

ENV PYTHONUNBUFFERED 1
RUN mkdir /container

WORKDIR /container

COPY requirements.txt /container/
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /container/

# COPY entrypoint.sh /
# RUN mv /container/entrypoint.sh /opt/entrypoint.sh
# RUN chmod +x /opt/entrypoint.sh
# ENTRYPOINT ["sh","/opt/entrypoint.sh"]

CMD ["gunicorn", "-c" , "config/gunicorn/conf.py", "-b", ":80", "runner"]
