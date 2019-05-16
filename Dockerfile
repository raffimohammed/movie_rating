FROM python:2.7
RUN pip2 install requests
COPY movie_rating_title.py /
