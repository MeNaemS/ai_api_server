# AI Server

A modern API server for AI-powered chat applications with authentication and database integration.

## 🚀 Features

- **Authentication System**: Secure user registration and login with JWT tokens
- **PostgreSQL Integration**: Robust data storage with asyncpg
- **AI Chat**: Support for configurable AI chat models
- **Clean Architecture**: Well-organized codebase with separation of concerns
- **Dependency Injection**: Using dishka for clean and testable code
- **FastAPI Framework**: High-performance async API with automatic documentation
- **Docker Support**: Easy deployment with Docker and docker-compose
- **Comprehensive Logging**: Configurable logging system with file and console outputs
- **Data Transfer Objects**: Type-safe data exchange between application layers

## 🛠️ Tech Stack

- **Python 3.13+**: Modern Python features
- **FastAPI**: High-performance web framework
- **PostgreSQL**: Reliable database storage
- **SQLAlchemy**: ORM for database operations
- **Psycopg**: Asynchronous PostgreSQL client
- **Alembic**: Database migrations
- **Dishka**: Dependency injection
- **JWT**: Authentication tokens
- **Pytest**: Testing framework with async support
- **Docker**: Containerization

## 🏗️ Project Structure

```text
AIServer/
├── config/               # Application configuration
├── src/
│   ├── alembic/          # Database migrations
│   ├── adapters/         # External interfaces (API, etc.)
│   ├── application/      # Business logic and use cases
│   ├── bootstrap/        # Application initialization and DI setup
│   ├── domain/           # Core business entities and rules
│   └── infrastructure/   # External tools and frameworks
│       ├── database/     # Database models and repositories
│       ├── logging/      # Logging configuration
│       └── security/     # Authentication and security
└── tests/                # Test suite
    └── e2e/              # End-to-end tests
```

## 🚦 Getting Started

### Prerequisites

- Python 3.13+
- PostgreSQL
- Docker and docker-compose (optional)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/AIBot.git
   cd AIBot/AIServer
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your configuration:

   ```text
   POSTGRES_NAME=your_username
   POSTGRES_PASSWORD=your_password
   POSTRGES_DATABASE=your_database
   ```

### Configuration and Secrets

The application uses a two-tier configuration system:

1. **Base Configuration** (`config/config.toml`):
   - Contains non-sensitive configuration settings
   - Should be committed to version control

2. **Secret Configuration** (`config/secret.toml`):
   - Contains sensitive data like API keys and JWT secrets
   - Should NOT be committed to version control (included in .gitignore)
   - Example structure:

     ```toml
     [jwt]
     secret_key = "your-secret-key-here"
     algorithm = "HS256"
     
     [database]
     username = "postgres"
     password = "your-password"
     database = "postgres"
     ```

### Running with Docker

1. Start the services:

   ```bash
   docker-compose up -d
   ```

2. Access pgAdmin at <http://localhost:5050> to manage your database.

### Database Setup

1. Run migrations:

   ```bash
   alembic -c src/alembic.ini upgrade head
   ```

### Running the Server

```bash
uvicorn src.bootstrap.main:app
```

The API will be available at <http://localhost:8000> with interactive documentation at <http://localhost:8000/docs>.

## 🧪 Testing

### Test Structure

- End-to-end (e2e) tests for API and database operations
- Configured pytest with support for asynchronous testing

### Running Tests

Run the test suite:

```bash
# Run all tests
pytest

# Run only e2e tests
pytest tests/e2e
```

Before running tests, make sure to apply migrations:

```bash
alembic -c src/alembic.ini upgrade head
```

## 📝 API Documentation

Once the server is running, visit <http://localhost:8000/docs> for the interactive API documentation.

### Main Endpoints

- **POST /auth/token**: Get access token with user credentials
- **POST /auth/users**: Register a new user

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
