<a id="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![BSD-3-Clause License][license-shield]][license-url]

---

<br />
<div align="center">
    <p>Copyright (c) 2025, <a href="https://github.com/programmingwithalex">GitHub@programmingwithalex</a></p>

  <h3 align="center">Flask, Celery, & Nginx - AWS Deployment</h3>

  <p align="center">
    Guide on deploying a flask app on AWS running: celery, celery_beat, and celery_flower, with a nginx container as the entry point
    <br />
    <a href="https://www.youtube.com/watch?v=RBj7ctj5Sk8&list=PLbn3jWIXv_iZqYn-RxjzaGXrDTWa3OnNw&index=1">YouTube Demo</a>
    ·
    <a href="https://github.com/programmingwithalex/aws_flask_celery/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/programmingwithalex/aws_flask_celery/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#series-outline">Series Outline</a>
      <ul>
        <li><a href="#aws-components">AWS Components</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <ul>
            <li><a href="#software">Software</a></li>
            <li><a href="#aws">AWS</a></li>
            <li><a href="#cmd-line">CMD Line</a></li>
          </ul>
      </ul>
    </li>
    <li><a href="#commands">AWS (CDK) Commands</a></li>
    <li><a href="#references">References</a></li>
  </ol>
</details>

## Series Outline

1. Explain the codebase configurations to understand how the different components interact
    * `docker-compose.yml` and each of the separate containers
    * `nginx.conf`
    * `Dockerfile` and `Dockerfile_nginx`
    * environment variables
    * `flask` app files and the configuration of the `celery` components

2. Get `aws_flask_celery_app` example running locally using `docker-compose`

3. Create working example of `aws_flask_celery_app` on AWS using [ECS](https://aws.amazon.com/ecs/)
    * will not be production ready
    * will rely on a lot of default values provided by AWS, with no networking setup by us
    * `S3` for environment variable storage

4. Create production-ready example of microservices on AWS using [ECS](https://aws.amazon.com/ecs/)
    * configure networking setup and apply that to ECS components
    * `SSM Parameter Store` for environment variable storage

5. Use GitHub Actions to automate deployments to AWS ECS components, referred to as Continuous Deployment (CD)

6. Create networking setup and ECS components automatically with a single script using [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/home.html)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### AWS Components

* Virtual Private Cloud (VPC)
* NAT Gateway & Internet Gateway (IGW)
* Elastic Container Registry (ECR)
* Elastic Container Service (ECS)
* ECS Clusters
* ECS Services
* ECS Task Definitions
* Application Load Balancer (ALB)
* S3
* SSM Parameter Store
* AWS Cloud Development Kit (CDK)
  * written in Python

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

### Prerequisites

#### Software

* Python: version requirement determined by [AWS CLI requirement](https://github.com/aws/aws-cli) and optionally [AWS CDK requirement](https://github.com/aws/aws-cdk)
* [Docker Desktop](https://www.docker.com/products/docker-desktop/): account not required, just installation

#### AWS

* create [AWS IAM user account](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html) than can be configured with the AWS CLI

#### CMD Line

* follow setup guides for [`aws-cli`](https://github.com/aws/aws-cli?tab=readme-ov-file#getting-started) if not already configured

#### Google Mail Credentials

* must have credentials for either gmail or another provider to send emails with
* is using 2FA for gmail account, must get an app password from [here](https://myaccount.google.com/apppasswords)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## AWS Cloud Development (CDK)

### Installation (Windows)

* [download](https://nodejs.org/en/download/prebuilt-installer) `node.js`, includes `npm` which is necessary to install the `aws-cli`
* [install](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html) `aws-cdk`

```bash
npm install -g aws-cdk
```

### Commands

* `cdk init app --language python` - create the initial CDK app locally
* `cdk bootstrap` - deploying the AWS CDK for the first time
* `cdk synth` - constucts CloudFormation template and does some verification checks
* `cdk deploy --all` - deploy all CDK components
* `cdk destroy --all` - destroys all CDK components
  * issue with calling because of Fargate Cluster dependency - `FargateCluster/FargateCluster (...) Resource handler returned message: "The specified capacity provider is in use and cannot be removed.`
  * if called **twice** then all elements will be deleted

## References

[create ALB](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/create-application-load-balancer.html)
> If your service's task definition uses the awsvpc network mode (which is required for the Fargate launch type), you must choose IP addresses as the target type. This is because tasks that use the awsvpc network mode are associated with an elastic network interface, not an Amazon EC2 instance.

[Target group port when using ALB](https://stackoverflow.com/questions/42715647/whats-the-target-group-port-for-when-using-application-load-balancer-ec2-con)
> Protocol port will be overriden by ECS anwyays so doesn't matter.

[CDK Workshop](https://cdkworkshop.com/)
> Instructions on using the AWS Cloud Development Kit (CDK)

[contributors-shield]: https://img.shields.io/github/contributors/programmingwithalex/aws_flask_celery?style=for-the-badge
[contributors-url]: https://github.com/programmingwithalex/aws_flask_celery/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/programmingwithalex/aws_flask_celery?style=for-the-badge
[forks-url]: https://github.com/programmingwithalex/aws_flask_celery/network/members
[stars-shield]: https://img.shields.io/github/stars/programmingwithalex/aws_flask_celery?style=for-the-badge
[stars-url]: https://github.com/programmingwithalex/aws_flask_celery/stargazers
[issues-shield]: https://img.shields.io/github/issues/programmingwithalex/aws_flask_celery?style=for-the-badge
[issues-url]: https://github.com/programmingwithalex/aws_flask_celery/issues
[license-shield]: https://img.shields.io/github/license/programmingwithalex/aws_flask_celery.svg?style=for-the-badge
[license-url]: https://github.com/programmingwithalex/aws_flask_celery/blob/main/LICENSE
