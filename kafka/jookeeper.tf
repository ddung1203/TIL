module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "oh-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["ap-northeast-2a","ap-northeast-2c","ap-northeast-2d"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.11.0/24", "10.0.12.0/24", "10.0.13.0/24"]

  enable_nat_gateway = true
  enable_vpn_gateway = true

  tags = {
    Terraform = "true"
    Environment = "dev"
  }
}

resource "aws_key_pair" "app_server_key" {
  key_name = "app_server_key"
  public_key = file("/home/vagrant/.ssh/id_rsa.pub")
}

module "zookeeper" {
  source = "github.com/barryw/terraform-aws-zookeeper"

  # If empty, no keypair will be assigned to instances
  keypair_name              = aws_key_pair.app_server_key.key_name
  vpc_id                    = module.vpc.vpc_id
  # Zookeeper instance subnets. Should be private
  zookeeper_subnets         = [module.vpc.private_subnets[0], module.vpc.private_subnets[1]]
  # defaults to false
  create_bastion            = true
  bastion_subnet            = module.vpc.public_subnets[0]
  bastion_ingress_cidrs     = ["0.0.0.0/0"]
  zookeeper_version         = "3.7.0"
  # Add any custom tags to include on created resources
  tags                      = {}
  # Gets added to the beginning of resource names
  name_prefix               = "my-zookeeper"
  # Must be odd
  cluster_size              = 3
  instance_type             = "t3.medium"
  root_volume_size          = 32
  data_volume_type          = "gp2"
  data_volume_size          = 10
  log_volume_type           = "gp2"
  log_volume_size           = 10
  # Specify a zone to create records on
  route53_zone              = "testzookeeper.com"
  # Specify the security group id of the groups to allow connections to ZK. If not specified, use the VPC's CIDR
  client_security_group_id  = ""
  # The namespace to use for CloudWatch metrics
  cloudwatch_namespace      = "CWAgent"
  zookeeper_config = {
    clientPort = 2181,
    syncLimit  = 5,
    initLimit  = 10,
    tickTime   = 2000,
    zkHeap     = 4096
  }
}

