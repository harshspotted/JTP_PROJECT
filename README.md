# JTP Test

This project contains a multi-service application with FastAPI backends, Next.js frontend, Qdrant vector database, and optional Ollama integration.

# AI-Powered Employee Skill & Project Recommendation System

An intelligent system that recommends roles and training programs based on employee skills, leveraging AI for personalized career development and project matching.

## Overview

This comprehensive AI system analyzes employee skills and provides intelligent recommendations for:

- **Project Assignments**: Match employees with suitable projects based on their skill profiles
- **Training Programs**: Recommend courses and learning paths to bridge skill gaps
- **Career Development**: Generate personalized analysis for professional growth
- **Job Readiness Assessment**: AI-powered analysis of employment prospects and skill gaps
- **Generative AI Insights**: Deep analysis of what skills you lack for target positions

## Architecture

The system follows a microservices architecture with the following components:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │  Inference API  │    │    CRUD API     │
│   (Next.js)     │────│   (FastAPI)     │────│   (FastAPI)     │
│   Port: 3000    │    │   Port: 8001    │    │   Port: 8002    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐    ┌─────────────────┐
                    │     Qdrant      │    │     Ollama      │
                    │  (Vector DB)    │    │   (Optional)    │
                    │  Port: 6333     │    │  Port: 11434    │
                    └─────────────────┘    └─────────────────┘
```

## Technology Stack

### Frontend

- **Next.js 14**: React framework with server-side rendering
- **TypeScript**: Type-safe development experience
- **Tailwind CSS**: Utility-first CSS framework
- **Shadcn UI**: Modern component library built on Radix UI
- **TanStack Table**: Powerful data table management

### Backend

- **FastAPI**: High-performance API framework
- **Python**: Core programming language
- **Qdrant**: Vector database for semantic search
- **SQLite**: Lightweight database for CRUD operations
- **Ollama**: Optional LLM integration

### Infrastructure

- **Docker**: Containerization platform
- **Docker Compose**: Multi-container orchestration
- **Kubernetes**: Production deployment (optional)

## Quick Start

### Prerequisites

Ensure you have the following installed:

- Docker & Docker Compose
- Make (optional, for convenient commands)
- Node.js 18+ (for local development)
- Python 3.9+ (for local development)

### Basic Setup (without Ollama)

```bash
# Clone the repository
git clone <repository-url>
cd jtp-test

# Start all services
docker compose -f docker-compose.yml up

# Or using the Makefile
make up
```

### With Ollama Integration

```bash
# Start all services including Ollama for enhanced AI capabilities
docker compose -f docker-compose.yml -f docker-compose.override.yml up -d

# Or using the Makefile
make up-ollama
```

## Project Structure

```
.
├── backend/
│   ├── inference_app.py        # AI inference service
│   ├── crud_app.py            # Data management service
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── components/           # React components
│   ├── pages/               # Next.js pages
│   ├── package.json         # Node.js dependencies
│   └── next.config.js       # Next.js configuration
├── docker/
│   ├── Dockerfile.inference  # Inference service container
│   ├── Dockerfile.crud      # CRUD service container
│   └── Dockerfile.frontend  # Frontend container
├── docker-compose.yml        # Main compose configuration
├── docker-compose.override.yml # Ollama integration
├── Makefile                 # Development commands
└── README.md               # This file
```

## Available Commands

### Docker Compose Commands

```bash
# Start services
make up                   # Start without Ollama
make up-ollama            # Start with Ollama
make build-up             # Build and start without Ollama
make build-up-ollama      # Build and start with Ollama

# Stop services
make down                 # Stop without Ollama
make down-ollama          # Stop with Ollama

# View logs
make logs                 # All services
make logs-inference       # Inference service only
make logs-crud           # CRUD service only
make logs-frontend       # Frontend service only
make logs-qdrant         # Qdrant service only
make logs-ollama         # Ollama service only

# Development
make dev-inference       # Start dependencies + inference service
make dev-crud           # Start dependencies + CRUD service
make dev-frontend       # Start backends + frontend service

# Utilities
make status             # Show service status
make clean              # Clean up containers and volumes
```

### Shell Access

```bash
make shell-inference    # Access inference container
make shell-crud        # Access CRUD container
make shell-frontend    # Access frontend container
make shell-qdrant      # Access Qdrant container
make shell-ollama      # Access Ollama container
```

## Service URLs

- **Frontend**: http://localhost:3000
- **Inference API**: http://localhost:8001
- **CRUD API**: http://localhost:8002
- **Qdrant Dashboard**: http://localhost:6333
- **Ollama** (if enabled): http://localhost:11434

## Core Features

### Skills & Expertise Management

- **TanStack Table** integration for efficient skills data presentation
- Interactive form interface for adding and managing employee skills
- Real-time skill proficiency tracking with experience levels
- Professional skill level categorization (Basic, Professional, CollegeResearch)

### AI-Powered Recommendations

- **Project Matching**: Intelligent project recommendations based on skill profiles
- **Semantic Search**: Vector-based similarity matching using Qdrant
- **Personalized Analysis**: Comprehensive employee-project fit evaluation
- **Training Recommendations**: AI-generated course suggestions for skill development

### Employee Profile Management

- Comprehensive skill portfolio tracking
- Experience level documentation (months of experience)
- Skill description and proficiency management
- Career progression visualization

### Learning Path Generation

- **Gap Analysis**: Identifies skill deficiencies for target projects
- **Course Recommendations**: Suggests relevant training programs
- **Personalized Learning Paths**: Tailored development roadmaps
- **Progress Tracking**: Monitors skill development over time

## API Endpoints

### Health Check

```http
GET /
```

Returns system health status.

### Project Recommendations

```http
POST /predict/
Content-Type: application/json

{
  "skills": [
    {
      "skill_name": "Python",
      "level": "Professional",
      "months": 24
    }
  ],
  "description": "Backend developer with API experience",
  "top_k": 5
}
```

**Response:**

```json
[
  {
    "rank": 1,
    "project_id": "project_22",
    "score": 55707.93,
    "description": "A backend project using Docker and Python...",
    "required_skills": [
      { "skill_name": "Python", "level": "Professional", "months": 12 }
    ]
  }
]
```

### Employee-Project Analysis

```http
POST /analysis/
Content-Type: application/json

{
  "employee_skills": [...],
  "employee_description": "Senior backend developer",
  "project_skills": [...],
  "project_description": "Containerize microservices platform",
  "score": 0.75
}
```

**Response:**

```json
{
  "fitness_evaluation": "Medium - Excellent Python background, but Docker skills need deepening.",
  "recommended_courses": "Enroll in an advanced Docker course and complete two hands-on container projects."
}
```

## Database Architecture

### SQLite (CRUD Operations)

- **Purpose**: Lightweight database for metadata and structured data
- **Location**: Within crud-app container or mounted volume
- **Usage**: Employee profiles, project definitions, skill catalogues

### Qdrant (Vector Database)

- **Purpose**: High-dimensional embedding storage and semantic search
- **Features**: Nearest-neighbor search, similarity matching
- **Use Cases**:
  - Skill similarity analysis
  - Project-employee matching
  - Contextual understanding for recommendations

## Dataset Generation Workflow

1. **Input Processing**: Frontend/API accepts new employee or project data
2. **Preprocessing**: Inference service generates embeddings from text descriptions
3. **Dual Storage**:
   - Metadata → SQLite via crud-app
   - Vector embeddings → Qdrant for similarity search
4. **Retrieval**: Qdrant provides contextually similar data for AI recommendations

## ☸️ Kubernetes Deployment

The system supports scalable Kubernetes deployment with dedicated pods:

| Pod Name        | Description                  | Database |
| --------------- | ---------------------------- | -------- |
| `inference-app` | FastAPI inference operations | -        |
| `crud-app`      | CRUD operations with SQLite  | SQLite   |
| `fe-app`        | Next.js frontend application | -        |
| `qdrant-pod`    | Vector database service      | Qdrant   |

## Environment Configuration

### Backend Services

```env
QDRANT_HOST=qdrant
QDRANT_PORT=6333
OLLAMA_HOST=ollama
OLLAMA_PORT=11434
```

### Frontend

```env
NEXT_PUBLIC_INFERENCE_API_URL=http://localhost:8001
NEXT_PUBLIC_CRUD_API_URL=http://localhost:8002
```

## 🔧 Development Setup

### Backend Requirements

```txt
fastapi>=0.100.0
uvicorn[standard]>=0.23.0
qdrant-client>=1.6.0
python-multipart>=0.0.6
pydantic>=2.0.0
```

### Frontend Dependencies

```json
{
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "@types/react": "^18.0.0",
    "typescript": "^5.0.0",
    "tailwindcss": "^3.3.0",
    "@tanstack/react-table": "^8.10.0"
  }
}
```

## Usage Examples

### Adding Employee Skills

1. Navigate to the Profile page
2. Click "Add Skills" button
3. Fill in skill details (name, level, experience)
4. Submit to update skill portfolio

### Generating Project Recommendations

1. Ensure employee profile is complete
2. Click "Generate Recommendations"
3. Review AI-suggested projects with match scores
4. Select project for detailed analysis

### Getting Learning Recommendations

1. Select a target project from recommendations
2. Click "Generate Analysis"
3. Review skill gap analysis
4. Follow suggested learning path

## GPU Support

For enhanced AI performance with Ollama, enable GPU support:

```yaml
# In docker-compose.override.yml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: 1
          capabilities: [gpu]
```

## Troubleshooting

### Common Issues

**Port Conflicts**

```bash
# Check if ports are available
netstat -tulpn | grep :3000
netstat -tulpn | grep :8001
```

**Build Issues**

```bash
# Clean and rebuild
make clean
make build-up
```

**Network Connectivity**

```bash
# Verify service communication
docker network ls
docker network inspect jtp-test_app-network
```

**Volume Issues**

```bash
# Clean unused volumes
docker volume prune
```
