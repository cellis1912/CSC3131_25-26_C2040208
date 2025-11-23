// DELETE BEFORE SUBMISSION //
docker run -p 5000:5000 myapp
docker build -t app .

docker-compose up -d --build
docker-compose down
// DELETE BEFORE SUBMISSION //

Architecture Diagram

<img width="1940" height="1280" alt="Blank diagram (3)" src="https://github.com/user-attachments/assets/8b8081f5-7d63-492f-85fa-3f4018d5839c" />

CI/CD Workflow Diagram
GitHub Repo
   │
   ├── On push to "main" branch
   │
   ▼
GitHub Actions Workflow
   │
   ├── Step 1: Checkout code
   ├── Step 2: Install dependencies
   ├── Step 3: Run tests
   ├── Step 4: Login to Azure Container Registry
   ├── Step 5: Build Docker image
   ├── Step 6: Push image to ACR
   ├── Step 7: Deploy new revision to Azure Container Apps
   │
   ▼
Azure Container Apps
   │
   └── Automatically updates revision + scales new version in

Ref
Puikinsh (no date) login-forms/forms/basic/index.html at main · puikinsh/login-forms, GitHub. Available at: https://github.com/puikinsh/login-forms/blob/main/forms/basic/index.html (Accessed: 12 October 2025).
