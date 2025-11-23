// DELETE BEFORE SUBMISSION //
docker run -p 5000:5000 myapp
docker build -t app .
docker-compose up -d --builddocker-compose down

Ref
Puikinsh (no date) login-forms/forms/basic/index.html at main · puikinsh/login-forms, GitHub. Available at: https://github.com/puikinsh/login-forms/blob/main/forms/basic/index.html (Accessed: 12 October 2025).


// DELETE BEFORE SUBMISSION //

## **Architecture Diagram**
<img width="500" height="1260" alt="Blank diagram (1)" src="https://github.com/user-attachments/assets/ca62443b-2dc9-40c5-b5c6-b9584d12aaa2" />

##**CI/CD Workflow Diagram**
<img width="1160" height="612" alt="Blank diagram (3)" src="https://github.com/user-attachments/assets/995c2d1d-17bf-4d0a-9662-2658dc453bae" />



### Trigger Strategy

The CI pipeline triggers on:

- push to *main*
- pull requests targeting *main*

This ensures:
- PRs are validated before merging
- *main* always deploys a fully tested, production-ready build

### Branching Strategy

- main → production
- feature (e.g. tests, azure) → individual tasks

Rationale:
- Keeps production stable
- Tasks remain contained until tested
- Easy rollback in case of errors
