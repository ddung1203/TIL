terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "4.22.0"
    }
  }
}

provider "aws" {
  # Configuration options
    profile = "default"
  region  = "ap-northeast-2"
}
