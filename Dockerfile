# Version: latest
FROM ubuntu:latest
ENV REFRESHED_AT 2017-05-09

# Update cache and install python and PostgreSQL client as Docker Stack don't support depends_on option
RUN apt-get -qqy update \
 && apt-get install -qqy python-pip python3-dev postgresql-client

# Add requirements.txt
ADD api/requirements.txt /webapp/

# Modify the working directory
WORKDIR /webapp

# Install webapp dependencies
RUN pip install -r requirements.txt

# Add the API Rest code
ADD api .
RUN chmod +x wait-for-database.sh

# Listen port 8080
EXPOSE 8080

ENTRYPOINT ["./wait-for-database.sh", "python", "app.py"]
