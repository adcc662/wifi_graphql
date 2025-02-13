# 📡 WiFi GraphQL API

## 📌 Introduction
This project implements a GraphQL API using **FastAPI**, **PostgreSQL with PostGIS**, and **SQLAlchemy**. Its goal is to provide access to a geospatial database of WiFi access points, enabling proximity queries and filtering by various criteria.

The API offers functionalities such as:
- Retrieving all WiFi access points with pagination.
- Querying by specific ID.
- Searching for WiFi points within a specified radius using PostGIS.
- Integration with Docker for quick deployment and execution.

## 📦 **Dependencies and Versions**

| Dependency        | Version |
|-------------------|---------|
| Python           | 3.11.x  |
| FastAPI          | 0.95+   |
| Strawberry-GraphQL | 0.138+ |
| SQLAlchemy       | 2.x     |
| asyncpg          | 0.28+   |
| PostgreSQL       | 14.x+   |
| PostGIS          | 3.x     |
| Docker & Docker Compose | Latest |

---

## 🚀 **Deployment Instructions**

### 📌 **Prerequisites**
Make sure you have installed:
- **Docker** and **Docker Compose**
- **Makefile** (Optional, to simplify commands)
- **PostgreSQL with PostGIS enabled** (if running without Docker)

### 📌 **Setup and Execution with Docker**

1. **Clone the repository**
   ```bash
   git clone https://github.com/adcc662/wifi_graphql.git
   cd wifi_graphql
   ```

2. **Set up environment variables**
   Copy the example file and edit it:
   ```bash
   cp .env.example .env
   ```
   Modify PostgreSQL credentials if necessary.

3. **Start services with Docker Compose**
   ```bash
   docker compose up --build
   ```

4. **Initialize the database and load data**
   ```bash
   docker compose exec web python -m src.scripts.load_data
   ```

5. **Access the GraphQL API**
   - Navigate to [http://localhost:8000/graphql](http://localhost:8000/graphql)
   - Test queries in GraphiQL

6. **Run unit tests**
   ```bash
   docker compose exec web pytest -v --disable-warnings
   ```

---

## 🏗 **General Solution Diagram**

The system consists of the following services:

```
+----------------------+          +----------------------+
|  GraphQL Client    |  --->    | FastAPI + Strawberry |
+----------------------+          +----------------------+
                                        |
+----------------------+          +----------------------+
|  PostgreSQL + PostGIS|  <----   |  SQLAlchemy + asyncpg|
+----------------------+          +----------------------+
```

- **FastAPI** exposes GraphQL endpoints using **Strawberry-GraphQL**.
- **PostgreSQL** stores WiFi access points and uses **PostGIS** for geospatial queries.
- **SQLAlchemy + asyncpg** handle asynchronous database operations.
- **Docker Compose** manages the deployment of API and PostgreSQL containers.

---

## 📜 **Solution Development**

### 📌 **Project Structure**
```plaintext
wifi_graphql/
│── src/
│   ├── core/
│   ├── database/  # Database connection and models
│   ├── graphql/   # GraphQL schema and resolvers
│   ├── models/    # SQLModel model definitions
│   ├── scripts/   # Data loading and testing
│   ├── schemas/   # Pydantic schemas for validation
│   ├── main.py    # FastAPI entry point
│── tests/         # Unit tests with pytest
│── Dockerfile
│── docker-compose.yml
│── requirements.txt
│── README.md
```

### 📌 **Key Components**

1. **SQLAlchemy Models** (`src/models/wifi_point.py`)
   - Defines `WifiAccessPoint` with PostGIS for location storage.

2. **Database and Sessions** (`src/database/session.py`)
   - Uses `asyncpg` and async SQLAlchemy for optimal performance.

3. **Data Loading** (`src/scripts/load_data.py`)
   - Imports data from CSV and stores it in PostgreSQL.

4. **GraphQL Queries** (`src/graphql/resolvers/wifi_point.py`)
   - Allows proximity queries using `ST_DWithin` from PostGIS.

5. **Unit Testing** (`tests/`)
   - Uses **pytest-asyncio** for testing endpoints and SQL queries.

---

## 🔍 **Example GraphQL Queries**

### **Query WiFi Points by Proximity**
```graphql
query {
  wifiPointsByProximity(
    location: {
      latitude: 19.432707,
      longitude: -99.086743,
      radius: 1000
    },
    page: 1,
    pageSize: 10
  ) {
    items {
      id
      program
      latitude
      longitude
      neighborhood
      district
    }
    total
    page
  }
}
```

### **Query All WiFi Points with Pagination**
```graphql
query {
  wifiPoints(page: 1, pageSize: 10) {
    items {
      id
      program
      installationDate
      latitude
      longitude
      neighborhood
      district
    }
    total
    page
    pageSize
    totalPages
  }
}
```

### **Query WiFi Point by ID**
```graphql
query {
  wifiPoint(id: "AICMT1-GW001") {
    id
    program
    installationDate
    latitude
    longitude
    neighborhood
    district
  }
}
```

### **Query WiFi Points by Neighborhood**
```graphql
query {
  wifiPoints(
    page: 1, 
    pageSize: 10, 
    neighborhood: "PEÑON DE LOS BAÑOS"
  ) {
    items {
      id
      program
      latitude
      longitude
      neighborhood
    }
    total
    page
  }
}
```

---

## ✅ **Conclusion**
This project implements an efficient and scalable API for querying WiFi access points using **GraphQL, FastAPI, and PostgreSQL/PostGIS**. Thanks to its asynchronous architecture and Docker integration, it allows rapid deployments and optimized geospatial queries.


