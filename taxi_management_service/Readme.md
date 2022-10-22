# How to run the  docker container in local

## Run it from shell locally

```bash
git clone https://github.com/rsharm18/GL_taxicoop.git
cd GL_taxicoop\taxi_management_service
pip3 install -r requirements.txt
cd service
python app.py
```

``` bash 
docker build -t taxi_mgmt .
docker run -p 127.0.0.1:8080:8080/tcp taxi_mgmt
```

## Publish a docker container to AWS ECR

```bash
aws configure
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 515412545596.dkr.ecr.us-east-1.amazonaws.com
docker build -t 515412545596.dkr.ecr.us-east-1.amazonaws.com/taxicocop-backend:taxi-management-service .
docker images
docker push 515412545596.dkr.ecr.us-east-1.amazonaws.com/taxicocop-backend:taxi-management-service
```