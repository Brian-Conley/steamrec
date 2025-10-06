# steamrec

## REQUIREMENTS
### Linux
- Docker
- Docker Compose
### Windows
- Docker Desktop (comes with Docker/Docker Compose)  
Download from www.docker.com/products/docker-desktop/
- WSL2  
To install WSL2:
1. Open PowerShell
2. Run: 
```batch
wsl --install
```

## RUNNING THE PROJECT
1. **Build and start containers:**
```bash
docker compose up --build
```

## CONTRIBUTING
1. Use branches 
- **Never** commit directly to main. That can and will cause problems for others.
- Create a new branch for your work using:
```bash
git checkout -b branch-name
```
2. Make commits
3. Open a Pull Request (PR)
- Push your branch to the repo.
- Create a PR from your branch into main.
- This is how code will make it to the main branch.
4. Review and merge
- It's best if PRs are reviewed by a teammate before merging.

Following these steps keeps the project stable and should make collaboration smoother for the whole team.
