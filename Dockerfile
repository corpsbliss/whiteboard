FROM python
COPY . /my_app
WORKDIR /my_app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python","app.py"]
