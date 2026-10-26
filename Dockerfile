#Start with a lightweight Python Image
# This gives our container a python runtime
FROM python:3.14-slim
#Set the working directory inside the container
WORKDIR /app
#Copy the dependency list before copying the application code

COPY requirements.txt .

#avoid retaining pip's download cache in the image
RUN pip install --no-cache-dir -r requirements.txt

#Copy the application code and saved model into /app
COPY . . 

#doucment 
EXPOSE 8000

#start the api server when the container launches
#0.0.0.0 allows connections through the container's network interface
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]