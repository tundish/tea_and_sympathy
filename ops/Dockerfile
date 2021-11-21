FROM python:3.9-alpine

ARG user=service
ARG envname=py3

ADD https://api.github.com/repos/alpinelinux/aports/tags?per_page=1 aports.json
RUN apk update

RUN umask 775
RUN adduser -h /home/$user -D -g "" -s /bin/bash $user

USER $user
WORKDIR /home/$user

RUN python3 -m venv /home/$user/$envname
ADD https://api.github.com/repos/pypa/pip/tags?per_page=1 pip.json
RUN /home/$user/$envname/bin/pip install --upgrade pip

ADD https://api.github.com/repos/tundish/tea_and_sympathy/tags?per_page=1 app.json
RUN /home/$user/$envname/bin/pip install tea-and-sympathy

EXPOSE 8080

ENTRYPOINT ["/home/service/py3/bin/tas-web", "--host", "0.0.0.0", "--port", "8080", "--log", "tas.log"]
