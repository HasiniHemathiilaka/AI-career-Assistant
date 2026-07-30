provider "aws" {
  region = "us-east-1"
}

# 1. AWS Container Registry (ECR) to store Docker images
resource "aws_ecr_repository" "app_repo" {
  name                 = "ai-career-assistant"
  image_tag_mutability = "MUTABLE"
}

# 2. Security Group for Free Tier EC2 instance
resource "aws_security_group" "app_sg" {
  name        = "ai-assistant-security-group"
  description = "Allow inbound SSH, Streamlit, and Prometheus traffic"

  # SSH Access
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Streamlit Web App Port
  ingress {
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Prometheus Metrics Port
  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Outbound All Traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 3. Free Tier EC2 Instance (Ubuntu 22.04 LTS)
resource "aws_instance" "app_server" {
  ami           = "ami-0c7217cdde317cfec" # Ubuntu 22.04 LTS (us-east-1)
  instance_type = "t3.micro"               # AWS Free Tier eligible
  security_groups = [aws_security_group.app_sg.name]

  user_data = <<-EOF
              #!/bin/bash
              sudo apt-get update -y
              sudo apt-get install -y docker.io docker-compose
              sudo systemctl start docker
              sudo systemctl enable docker
              sudo usermod -aG docker ubuntu
              EOF

  tags = {
    Name = "AI-Career-Assistant-Server"
  }
}

# Output values needed for CI/CD setup
output "ec2_public_ip" {
  description = "The public IP of your EC2 server"
  value       = aws_instance.app_server.public_ip
}

output "ecr_repository_url" {
  description = "The URL of your Amazon ECR repository"
  value       = aws_ecr_repository.app_repo.repository_url
}