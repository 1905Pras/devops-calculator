# DevOps Calculator — Automated CI/CD with AWS

A Python calculator application demonstrating a complete DevOps workflow using **Git, Docker, pytest, GitHub Actions, AWS Lambda, Amazon API Gateway, AWS SAM, and AWS CloudFormation**.

The project automates application testing and AWS deployment through a GitHub Actions pipeline. When code is pushed to the `main` branch, the workflow builds a Docker image, runs automated tests, and deploys the serverless application to AWS if the tests pass.

## Table of Contents

- [Project Overview](#project-overview)
- [Objectives](#objectives)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Application Features](#application-features)
- [Prerequisites](#prerequisites)
- [Local Setup](#local-setup)
- [Running Automated Tests](#running-automated-tests)
- [Docker Setup](#docker-setup)
- [AWS Deployment](#aws-deployment)
- [GitHub Actions CI/CD Pipeline](#github-actions-cicd-pipeline)
- [API Documentation](#api-documentation)
- [IAM and Security](#iam-and-security)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)
- [Author](#author)

## Project Overview

The DevOps Calculator project demonstrates how software development, automated testing, containerization, and cloud deployment can be integrated into a single workflow.

The application supports arithmetic operations through a Python-based AWS Lambda function exposed using Amazon API Gateway.

The CI/CD pipeline is implemented using GitHub Actions. It builds a Docker image and executes automated tests. When changes are pushed to `main`, the workflow deploys the application using AWS Serverless Application Model (SAM) and AWS CloudFormation.

The project also demonstrates secure GitHub-to-AWS authentication using OpenID Connect (OIDC), avoiding the need to store long-lived AWS access keys in GitHub Actions secrets.

## Objectives

- Develop a Python calculator application.
- Write automated unit tests using pytest.
- Package the application and test environment using Docker.
- Automate builds and tests with GitHub Actions.
- Deploy a serverless application to AWS Lambda.
- Expose the application through Amazon API Gateway.
- Define AWS infrastructure using AWS SAM and CloudFormation.
- Configure IAM permissions and GitHub OIDC authentication.
- Understand CI/CD automation, deployment failures, and IAM troubleshooting.

## Architecture

The project follows this workflow:

```text
Developer
    |
    | Git commit and push
    v
GitHub Repository
    |
    v
GitHub Actions Workflow
    |
    v
Build Docker Image
    |
    v
Run pytest Tests in Docker
    |
    +---- Tests Fail ----> Stop Pipeline
    |
    +---- Tests Pass
              |
              v
      Configure AWS Credentials
          using GitHub OIDC
              |
              v
          Validate SAM
              |
              v
          Build SAM App
              |
              v
      Upload Deployment Artifacts
              |
              v
       AWS CloudFormation
              |
              v
        Amazon API Gateway
              |
              v
          AWS Lambda
              |
              v
       Calculator Response
```

### Architecture Components

| Component | Responsibility |
|---|---|
| Git and GitHub | Version control and source-code hosting |
| pytest | Automated application testing |
| Docker | Containerized test execution |
| GitHub Actions | CI/CD workflow automation |
| AWS IAM | Authentication and authorization |
| GitHub OIDC | Secure, temporary AWS credentials |
| AWS SAM | Serverless application packaging and deployment |
| Amazon S3 | Storage for deployment artifacts |
| AWS CloudFormation | Infrastructure provisioning and updates |
| AWS Lambda | Execution of the Python calculator |
| Amazon API Gateway | HTTP endpoint for calculator requests |
| Amazon CloudWatch | Lambda logs and operational monitoring |

## Technology Stack

- **Programming language:** Python 3.12
- **Testing framework:** pytest
- **Containerization:** Docker
- **Version control:** Git and GitHub
- **CI/CD:** GitHub Actions
- **Cloud provider:** Amazon Web Services (AWS)
- **Serverless compute:** AWS Lambda
- **API management:** Amazon API Gateway REST API
- **Infrastructure as Code:** AWS SAM and CloudFormation
- **Artifact storage:** Amazon S3
- **Authentication:** AWS IAM and GitHub OIDC
- **Monitoring:** Amazon CloudWatch

## Project Structure

```text
devops-calculator/
│
├── src/
│   └── app.py
│
├── tests/
│   └── test_app.py
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── pytest.ini
├── requirements.txt
├── template.yaml
└── README.md
```

### Important Files

| File | Purpose |
|---|---|
| `src/app.py` | Calculator logic and AWS Lambda handler |
| `tests/test_app.py` | Automated tests for calculator functionality |
| `requirements.txt` | Python dependencies required for testing |
| `pytest.ini` | pytest configuration |
| `Dockerfile` | Instructions for building the test container |
| `.dockerignore` | Files excluded from the Docker build context |
| `.gitignore` | Files excluded from Git version control |
| `template.yaml` | AWS SAM template defining the Lambda function and API |
| `.github/workflows/ci-cd.yml` | GitHub Actions CI/CD pipeline |
| `README.md` | Project documentation |

## Application Features

The calculator supports:

- Addition
- Subtraction
- Multiplication
- HTTP-based requests through Amazon API Gateway
- Serverless execution using AWS Lambda
- Automated testing using pytest
- Automated deployment through GitHub Actions

The API is configured with a `POST` method and the `/calculate` path.

## Prerequisites

Install the following tools before running the project locally:

1. Python 3.12
2. Git
3. Docker Desktop
4. AWS CLI
5. AWS SAM CLI
6. A GitHub account and repository
7. An AWS account with appropriately configured IAM permissions

Verify the installations:

```bash
python --version
git --version
docker --version
aws --version
sam --version
```

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/1905Pras/devops-calculator.git
cd devops-calculator
```

### 2. Create a Python virtual environment

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

On Linux or macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the application tests

```bash
python -m pytest -v
```

The tests should pass before proceeding to Docker and AWS deployment.

## Running Automated Tests

The project uses pytest to validate calculator functionality.

Run all tests:

```bash
pytest
```

Run tests with detailed output:

```bash
pytest -v
```

Run tests from a specific file:

```bash
pytest tests/test_app.py -v
```

Automated testing helps detect application defects before deployment. In this project, the Docker test job must succeed before the AWS deployment job can execute.

## Docker Setup

Docker provides a consistent environment for building and testing the application.

### Build the Docker image

```bash
docker build -t devops-calculator .
```

### Run the tests inside the container

```bash
docker run --rm devops-calculator
```

The container executes the test command defined in the Dockerfile.

### List Docker images

```bash
docker images
```

### Remove the image when no longer needed

```bash
docker rmi devops-calculator
```

The image can only be removed when no container is using it.

## AWS Deployment

The application is deployed to the AWS Mumbai region.

**AWS Region:** `ap-south-1`

**CloudFormation Stack:** `devops-calculator-dev`

**Deployment Method:** AWS SAM and CloudFormation

### AWS Resources

The SAM template defines:

- An AWS Lambda function using Python 3.12.
- An API Gateway REST API.
- A `POST /calculate` endpoint.
- Lambda execution permissions.
- A `Prod` API Gateway stage.

The deployment workflow also uploads packaged deployment artifacts to an S3 bucket.

### SAM Template Configuration

The main configuration in `template.yaml` is:

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Transform: AWS::Serverless-2016-10-31

Description: DevOps Calculator Assignment

Globals:
  Function:
    Runtime: python3.12
    Timeout: 10
    MemorySize: 128

Resources:
  CalculatorFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/
      Handler: app.lambda_handler
      Description: Calculator supporting addition, subtraction, and multiplication
      Policies:
        - AWSLambdaBasicExecutionRole
      Events:
        CalculatorApi:
          Type: Api
          Properties:
            Path: /calculate
            Method: POST

Outputs:
  CalculatorApiUrl:
    Description: Calculator API endpoint
    Value: !Sub "https://${ServerlessRestApi}.execute-api.${AWS::Region}.amazonaws.com/Prod/calculate"
```

### Validate and build locally

Validate the SAM template:

```bash
sam validate --template-file template.yaml --region ap-south-1
```

Build the serverless application:

```bash
sam build --template-file template.yaml
```

### Deploy locally using AWS credentials

For a local deployment, configure AWS credentials through an appropriate secure method, then run:

```bash
sam deploy \
  --template-file .aws-sam/build/template.yaml \
  --stack-name devops-calculator-dev \
  --s3-bucket YOUR_DEPLOYMENT_BUCKET \
  --capabilities CAPABILITY_IAM \
  --no-confirm-changeset \
  --no-fail-on-empty-changeset \
  --region ap-south-1
```

Replace `YOUR_DEPLOYMENT_BUCKET` with the name of your existing deployment bucket. This is an alternative manual deployment procedure; the normal automated deployment is performed by GitHub Actions.

### Verify the CloudFormation stack

```bash
aws cloudformation describe-stacks \
  --stack-name devops-calculator-dev \
  --region ap-south-1 \
  --query "Stacks[0].StackStatus" \
  --output text
```

A successful deployment generally reports `CREATE_COMPLETE` or `UPDATE_COMPLETE`.

### Retrieve the API endpoint

```bash
aws cloudformation describe-stacks \
  --stack-name devops-calculator-dev \
  --region ap-south-1 \
  --query "Stacks[0].Outputs" \
  --output table
```

## GitHub Actions CI/CD Pipeline

The workflow is defined in:

```text
.github/workflows/ci-cd.yml
```

### Continuous Integration (CI)

The CI job runs on pushes and pull requests.

It performs the following operations:

1. Checks out the repository.
2. Builds the Docker image.
3. Runs pytest inside the Docker container.
4. Reports the result to GitHub Actions.

If the tests fail, the dependent deployment job does not run.

### Continuous Deployment (CD)

The deployment job runs only when a push event targets the `main` branch and the CI job succeeds.

It performs the following operations:

1. Checks out the repository.
2. Sets up Python 3.12.
3. Installs AWS SAM CLI.
4. Obtains temporary AWS credentials using GitHub OIDC.
5. Validates the SAM template.
6. Builds the serverless application.
7. Uploads deployment artifacts to the configured S3 bucket.
8. Deploys the application using CloudFormation.

The deployment uses the stack name `devops-calculator-dev` and region `ap-south-1`.

### GitHub Repository Configuration

Configure these repository settings under **Settings → Secrets and variables → Actions**.

| Name | Type | Purpose |
|---|---|---|
| `AWS_ROLE_ARN` | Repository secret | ARN of the IAM role assumed by GitHub Actions |
| `AWS_REGION` | Repository variable | AWS deployment region, set to `ap-south-1` |

The IAM role must have an OIDC trust policy that allows the intended repository and branch to assume it. It also needs sufficient permissions to deploy the resources defined in the SAM template.

### How to Trigger the Pipeline

**For CI testing:**

```bash
git checkout -b feature/test-ci
git add .
git commit -m "test: verify CI pipeline"
git push -u origin feature/test-ci
```

Open a pull request to `main`. The CI job should run, while the deployment job should remain skipped.

**For deployment:**

After reviewing and merging the pull request into `main`, GitHub Actions runs the CI job and, if it succeeds, the deployment job.

A direct push to `main` also triggers deployment under the workflow configuration.

## API Documentation

### API Endpoint

The deployed API endpoint is:

`https://qb0zkko0uh.execute-api.ap-south-1.amazonaws.com/Prod/calculate`

### Request Details

| Property | Value |
|---|---|
| HTTP method | `POST` |
| Resource path | `/calculate` |
| Content type | `application/json` |
| API Gateway stage | `Prod` |
| AWS region | `ap-south-1` |

### Example Request

The following example assumes the Lambda handler accepts `a`, `b`, and `operation` as JSON fields.

```json
{
  "a": 10,
  "b": 5,
  "operation": "add"
}
```

### Test the API Using PowerShell

```powershell
Invoke-RestMethod `
  -Uri "https://qb0zkko0uh.execute-api.ap-south-1.amazonaws.com/Prod/calculate" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"a":10,"b":5,"operation":"add"}'
```

Expected mathematical result: `15`. The exact response format depends on how `lambda_handler` formats its response.

### Test Using curl

```bash
curl -X POST \
  "https://qb0zkko0uh.execute-api.ap-south-1.amazonaws.com/Prod/calculate" \
  -H "Content-Type: application/json" \
  -d '{"a":10,"b":5,"operation":"add"}'
```

### Additional Operations

If supported by the application handler, test subtraction:

```json
{
  "a": 10,
  "b": 5,
  "operation": "subtract"
}
```

Test multiplication:

```json
{
  "a": 10,
  "b": 5,
  "operation": "multiply"
}
```

Use the exact operation names supported by `src/app.py`.

## IAM and Security

The project uses AWS IAM to control deployment permissions.

### GitHub OIDC Authentication

GitHub Actions obtains temporary credentials by assuming the `GitHubActionsDeployRole` IAM role through OpenID Connect.

This avoids storing permanent AWS access keys in the repository.

### Permissions Required

The deployment role requires permissions appropriate to the deployment resources, including:

- CloudFormation stack operations.
- S3 access for deployment artifacts.
- Lambda function creation, updates, and permissions management.
- API Gateway REST API and stage management.
- IAM execution-role management and `iam:PassRole`, appropriately scoped.

The exact permissions depend on the resources and configuration in the SAM template.

### Security Best Practices

- Never commit AWS access keys, passwords, or other secrets.
- Prefer OIDC and temporary credentials for GitHub Actions.
- Scope IAM permissions to the required resources and actions.
- Restrict the OIDC trust policy to the intended repository and branch.
- Protect the `main` branch and require successful CI checks before merging.
- Avoid using AWS root credentials for routine deployment.
- Review AWS resources and costs after testing.

## Troubleshooting

### 1. Docker build fails

Check that Docker Desktop is running and that the Dockerfile is present.

```bash
docker build -t devops-calculator .
```

### 2. pytest tests fail

Activate the virtual environment, install dependencies, and inspect the test output.

```bash
pip install -r requirements.txt
pytest -v
```

### 3. GitHub Actions cannot assume the AWS role

Verify the `AWS_ROLE_ARN` secret, the `AWS_REGION` variable, the IAM OIDC identity provider, and the role trust policy.

### 4. AWS deployment fails with AccessDenied

Inspect the CloudFormation stack events to identify the exact missing IAM action and affected resource. Update the deployment role's policy with the necessary least-privilege permission.

### 5. CloudFormation stack is in ROLLBACK_COMPLETE

A stack in `ROLLBACK_COMPLETE` generally cannot be updated. If appropriate, delete the failed stack, wait for deletion to finish, and rerun the deployment after resolving the original failure.

For `ROLLBACK_FAILED`, inspect the latest failed events and resolve the cleanup permission issue before retrying deletion.

### 6. API returns Missing Authentication Token

Verify the API endpoint, stage, resource path, and HTTP method. This response can occur when the requested route or method does not match the deployed API configuration.

For this project, the configured route is `POST /calculate`.

### 7. API returns an application error

Check the request JSON against the fields expected by `src/app.py`. Inspect the Lambda function's CloudWatch logs for runtime errors.

## Future Improvements

Potential enhancements include:

- Add input validation and more unit tests.
- Add tests for division, invalid operations, missing fields, and edge cases if those features are implemented.
- Add API integration tests to the CI pipeline.
- Configure CloudWatch alarms and operational dashboards.
- Introduce separate development and production deployment environments.
- Add branch protection and mandatory pull-request reviews.
- Add automated rollback and deployment notifications.
- Explore API authentication and throttling.
- Improve deployment permissions and resource tagging.
- Add a manual approval step before production deployment.

## Author

**Prasanth**

GitHub: [1905Pras](https://github.com/1905Pras)

Repository: [devops-calculator](https://github.com/1905Pras/devops-calculator)

---

*This project was developed as a hands-on exercise to understand automated testing, Docker, GitHub Actions, AWS serverless services, Infrastructure as Code, IAM, and CI/CD deployment workflows.*
