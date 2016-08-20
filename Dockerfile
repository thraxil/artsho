FROM ccnmtl/django.base
RUN apt-get update && apt-get install -qy \
		binutils \
		build-essential \
		gcc \
		libffi-dev \
		libssl-dev \
		libexif-dev \
		libexif12 \
		libfontconfig1-dev \
		libfreetype6-dev \
		libldap2-dev \
		libpq-dev  \
		libsasl2-dev \
		libssl-dev \
		libxft-dev \
		libxml2-dev \
		libxslt1-dev \
		python-all-dev \
		python-dev \
		python-beautifulsoup \
		python-ldap \
		python-tk \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*
RUN /ve/bin/pip install wheel
WORKDIR /app
COPY package.json /app/package.json
RUN npm install
ADD requirements.txt
RUN /ve/bin/pip install --no-index -f /wheelhouse -r /wheelhouse/requirements.txt \
  && rm -rf /wheelhouse

COPY . /app/
RUN /ve/bin/flake8 /app/artsho/ --max-complexity=5 \
  && /ve/bin/python manage.py test \
  && npm install
EXPOSE 8000
ADD docker-run.sh /run.sh
ENV APP artsho
ENTRYPOINT ["/run.sh"]
CMD ["run"]
