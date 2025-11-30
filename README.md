// DELETE BEFORE SUBMISSION //
docker run -p 5000:5000 myapp
docker build -t app .
docker-compose up -d --builddocker-compose down

Ref
Puikinsh (no date) login-forms/forms/basic/index.html at main · puikinsh/login-forms, GitHub. Available at: https://github.com/puikinsh/login-forms/blob/main/forms/basic/index.html (Accessed: 12 October 2025).


// DELETE BEFORE SUBMISSION //

## **Architecture Diagram**
<img width="500" height="1260" alt="Blank diagram (1)" src="https://github.com/user-attachments/assets/ca62443b-2dc9-40c5-b5c6-b9584d12aaa2" />

## **CI/CD Workflow Diagram**
<img width="1160" height="612" alt="Blank diagram (3)" src="https://github.com/user-attachments/assets/995c2d1d-17bf-4d0a-9662-2658dc453bae" />


## **Engineering Decisions**
### **Trigger Strategy**

The CI pipeline triggers on:

- push to *main*
- pull requests targeting *main*

This ensures:
- PRs are validated before merging
- *main* always deploys a fully tested, production-ready build

### **Branching Strategy**

- main → production
- feature (e.g. tests, azure) → individual tasks

Rationale:
- Keeps production stable
- Tasks remain contained until tested
- Easy rollback in case of errors

### **Pipeline Steps Rationale**
| Step                            | Why                                            |
| ------------------------------  | ---------------------------------------------- |
| Checkout code                   | Required for all workflows                     |
| Install dependencies            | Ensures environment is reproducible            |
| Run tests                       | Prevent bad code deployments                   |
| Build Docker image              | Needed to deploy containers                    |
| Push to ACR                     | Central place to store production-ready images |
| Deploy to Azure Container Apps  | Fully automated delivery                       |



## **Tools Used & Why They Are Used**

**1. Azure Container Apps (ACA)**
- Serverless containers
- Autoscaling
- Ideal for Flask microservices

**2. Azure Database for PostgreSQL**
- Fully managed Postgres
- Built-in backups and scaling
- No container-based database risk

**3. Azure Container Registry (ACR)**
- Secure private registry
- Works seamlessly with Container Apps

**4. GitHub Actions**
- Native integration with GitHub repos
- Free compute (on current scale)
- Excellent for container builds

**5. Python + Flask + Gunicorn**
- Lightweight
- Easy to containerize
- Familiar to most engineers

## **Handover Notes**
### Application Overview

This is a Flask-based job management application running on Azure Container Apps.
Data is stored in Azure PostgreSQL.
The application exposes metrics and uses Gunicorn for concurrency.

### How to Deploy
- Push code to main branch
- GitHub Actions builds + tests code
- Docker image is pushed to ACR
- Azure Container Apps pulls the new image
- New revision becomes active

### Where to Find Things
/app            - Flask backend

/templates      - HTML templates

requirements.txt

Dockerfile

### How to Onboard
- Clone the repository
- Install Python
- Run locally using docker-compose up
- Deploy using GitHub Actions
