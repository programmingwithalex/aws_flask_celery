# ************************************************************************ #
# * Needed because can't add second target to load balancer in ECS console
# * Reference: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/register-multiple-targetgroups.html
#
# * don't end up using b/c issue specifying different containerPort for each target group when using CDK
# * instead use nginx on port `80` as entry point for `flask` and `celery-flower` dashboard
# ************************************************************************ #

import os

import boto3
from dotenv import load_dotenv

load_dotenv('default.env')

# Initialize the ECS client
ecs = boto3.client('ecs')

# Specify the ECS service and cluster information
cluster_name = f'{os.getenv("ENVIRONMENT_NAME")}-cluster'
service_name = f'{os.getenv("ENVIRONMENT_NAME")}-service'

# print(f'cluster_name: {cluster_name}')
# print(f'service_name: {service_name}')

# Describe the existing service to get the current configuration
response = ecs.describe_services(cluster=cluster_name, services=[service_name])

# Extract the existing load balancer configuration
load_balancers = response['services'][0]['loadBalancers']

# ************************************************************************ #
# * Add a new target group to the load balancer configuration
# * target_group_celery_flower_arn = \
# *   'arn:aws:elasticloadbalancing:<region>:<account_id>:targetgroup/<target_group_celery_flower_name>/<tg_id>'
# * pull from CloudFormation VPC outputs
# ************************************************************************ #
target_group_celery_flower_arn = os.environ['TARGET_GROUP_CELERY_FLOWER_ARN']
load_balancers.append(
    {
        'targetGroupArn': target_group_celery_flower_arn,
        'containerName': 'celery-flower',
        'containerPort': int(os.environ['PORT_CELERY_FLOWER']),
    }
)

# Update the ECS service with the new load balancer configuration
response = ecs.update_service(cluster=cluster_name, service=service_name, loadBalancers=load_balancers)
