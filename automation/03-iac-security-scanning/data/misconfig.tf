# Meridian Cloud Infrastructure — first draft (intentionally misconfigured for lab exercise)
# DO NOT apply to a real cloud account.

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# Misconfiguration 1: S3 bucket with public ACL, no versioning, no access logging, no encryption
resource "aws_s3_bucket" "data_lake" {
  bucket = "meridian-data-lake"
  # Missing: server_side_encryption_configuration
  # Missing: versioning
  # Missing: logging
  tags = {
    Name = "meridian-data-lake"
  }
}

resource "aws_s3_bucket_acl" "data_lake_acl" {
  bucket = aws_s3_bucket.data_lake.id
  acl    = "public-read"  # Misconfiguration: public read access
}

# Misconfiguration 2: Security group open to the world on SSH
resource "aws_security_group" "admin_sg" {
  name        = "meridian-admin"
  description = "Admin access"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Misconfiguration: open to internet
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Misconfiguration 3: EC2 instance with admin IAM role and no IMDSv2 requirement
resource "aws_iam_role" "admin_role" {
  name = "meridian-admin-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy" "admin_policy" {
  name = "admin-policy"
  role = aws_iam_role.admin_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action   = "*"        # Misconfiguration: wildcard actions
      Effect   = "Allow"
      Resource = "*"        # Misconfiguration: all resources
    }]
  })
}

resource "aws_instance" "bastion" {
  ami                    = "ami-0c55b159cbfafe1f0"
  instance_type          = "t3.micro"
  iam_instance_profile   = aws_iam_role.admin_role.name
  # Misconfiguration: missing metadata_options { http_tokens = "required" } (IMDSv2)
  # Misconfiguration: missing monitoring = true
  vpc_security_group_ids = [aws_security_group.admin_sg.id]

  tags = {
    Name = "meridian-bastion"
  }
}
