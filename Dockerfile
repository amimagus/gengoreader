FROM python:latest
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "executable" ]
USER root
ENV PORT=8000
WORKDIR /app
EXPOSE 8000
COPY . .
RUN pip install requests schedule beautifulsoup4 lxml
CMD ["python", "./rssfeedreader.py"]