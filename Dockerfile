FROM python

WORKDIR /var/app

COPY . /var/app

# RUN /bin/bash -c "virtualenv .venv"

# RUN /bin/bash -c "source /var/app/.venv/bin/activate"

RUN pip install -U setuptools

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["/usr/local/bin/gunicorn", "-b", ":80", "sf-contacts-backend.app"]

