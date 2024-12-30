# NGINX as a Solution to ECS Mutliple Target Groups with AWS CDK

## Initial Goal

- create ECS Service with two Target Groups
  - `flask` (5000)
  - `celery_flower` (5555)
- use ALB with listener rules based on path to load balance to `flask` or `celery_flower` (`/flower`) Target Groups based on path

### Manual

- succeeded in adding two Target Groups to ECS Service
  - can't specify two Target Groups in ECS Service creation
    - have to use separate script to assign second Target Group after ECS Service creation (`add_target_group_to_load_balancer.py`)
- succeeded in using ALB rules to conditionally direct traffic to each target group

### AWS CDK

- succeeded in adding two Target Groups to ECS Service
- issue #1:
  - whichever container is assigned to the task definition first, that port mapping will be used to register target in every Target Group assigned to ECS Service
    - it overrides the port specification of the Target Group itself
  - attempted solution of assigning target with correct port to second Target Group after running CDK script (leads to issue #2)
- issue #2:
  - even after assigning target to second Target Group with correct port, the health checks would never resolve
    - `Request Timed Out`
    - verified containers were all running
    - didn't have this issue when creating manually

## Final Resolution

- forget the two Target Groups, just making life hard for no reason
- instead add a `nginx` container on port 80
  - Load Balancer health checks resolve
  - Target Group health checks resolve
  - can access `flask` app and `celery_flower` dashboard
