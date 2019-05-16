FROM python:2.7
RUN pip2 install requests
COPY movie_rating_exact_match.py /
COPY movie_rating_partial_match.py /
