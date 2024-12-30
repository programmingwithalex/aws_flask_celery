# AWS ECS Service Discovery

## Deployment Notes

* allows multiple AWS ECS services to talk to each other
* deployment order of services matters - for the **first** deployment
  * subsequent deployment all services will be aware of each other
    * ex: if `app` service depends on `db` service, deploy the `db` service first

* service task definitions CloudFormation
  * `portName` - referencing port name in task definition json file
  * `discoveryName` - reservation of application name
  * defaults to portName
  * can have more than one `discoveryName`
  * sub-parameter: `dnsName` - tells how client to connect to service
    * defaults to `discoverName`.`namespace`

* in each service's task definition, there will be two containers:
    (1) the app you specified in task definition
    (2) ecs-service-connect container (sidecar container)
* can be multiple task definition's per service if want replication

## Creating Components

* can specify the `Dockerfile` `command` argument for the container when creating the `task-definition`
  * means can reuse base `Dockerfile`
* when creating AWS service must put task in the public subnet or it can't communicate with the ECR repo
  * [reference](https://stackoverflow.com/questions/61265108/aws-ecs-fargate-resourceinitializationerror-unable-to-pull-secrets-or-registry)

## Debugging References

* [ECS unable to pull secrets or registry](https://stackoverflow.com/questions/61265108/aws-ecs-fargate-resourceinitializationerror-unable-to-pull-secrets-or-registry)
* [ECS tasks stuck in provisioning state](https://stackoverflow.com/questions/63123466/all-tasks-on-a-ecs-service-stuck-in-provisioning-state)
* [ECS large VPC for cluster](https://containersonaws.com/pattern/large-vpc-for-amazon-ecs-cluster)

* [create ALB](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/create-application-load-balancer.html)
  * If your service's task definition uses the awsvpc network mode (which is required for the Fargate launch type), you must choose IP addresses as the target type This is because tasks that use the awsvpc network mode are associated with an elastic network interface, not an Amazon EC2 instance.

## Networking Setup References

* [enable internet access for EC2 in private subnet](https://www.secopsolution.com/blog/enable-internet-access-for-ec2-instances-in-private-subnet)

## ECS Service Connect References

* [service connect component definitions](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-connect-concepts.html#service-connect-concepts-terms)
* [service connect vs service discovery](https://www.cloudkeeper.com/insight/blog/amazon-ecs-service-communication-via-service-discovery-connect)