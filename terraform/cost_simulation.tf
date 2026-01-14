# 가상의 AWS 고성능 서버 견적용 코드 (실제 배포 X)
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "web_server" {
  ami           = "ami-12345678"
  instance_type = "m5.4xlarge" # 꽤 비싼 서버
}

resource "aws_db_instance" "default" {
  allocated_storage    = 100
  engine               = "mysql"
  instance_class       = "db.m5.large"
}
