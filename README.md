# Customer Data Listing API

This repository contains the backend API for a customer data listing service. It is a robust and scalable Python application built with FastAPI, designed to serve customer data with functionality for searching, filtering, sorting, and pagination. 

[![Python Version](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Framework](https://img.shields.io/badge/framework-FastAPI-green.svg)](https://fastapi.tiangolo.com/)
[![Swagger](https://img.shields.io/badge/Swagger-85EA2D?logo=insomnia&logoColor=000)](#)
[![Docker](https://img.shields.io/badge/container-Docker-blue.svg)](https://www.docker.com/)

---

## Table of Contents

-   [Project Overview](#project-overview)
-   [Features](#features)
-   [Tech Stack & Architectural Choices](#tech-stack--architectural-choices)
-   [Prerequisites](#prerequisites)
-   [Getting Started](#getting-started)
-   [Usage](#usage)
    -   [Interactive API Documentation (Swagger UI)](#interactive-api-documentation-swagger-ui)
    -   [API Endpoints](#api-endpoints)
-   [Deployment Strategy](#deployment-strategy)
-   [Future Improvements](#future-improvements)

---

## Project Overview

This microservice provides the backend infrastructure for a customer data management system. It exposes a set of API endpoints to handle customer information and their associated items. The application is built following modern API development practices, emphasising performance and ease of use.

The core responsibilities of this service are:
1.  To provide a robust API for fetching customer records.
2.  To ensure data integrity and validation through schema enforcement.
3.  To offer a simple, containerised setup for local development and deployment.

---

## Features

-   **Fast & Modern API:** Built with FastAPI for high performance, asynchronous capabilities, and automatic documentation.
-   **Data Validation:** Leverages Pydantic schemas for powerful request body validation and data serialization.
-   **Containerised:** Fully containerised with Docker and Docker Compose for a one-command setup and a consistent runtime environment.
-   **Interactive Documentation:** Automatically generated, interactive API documentation via Swagger UI, allowing for easy endpoint testing.

---

## Tech Stack & Architectural Choices

-   **Python 3.9:** A modern, stable version of Python.
-   **FastAPI:** Chosen for its high performance, native async support, and tight integration with Pydantic for data validation and the automatic generation of OpenAPI specifications.
-   **Uvicorn:** A lightning-fast ASGI server, recommended for running FastAPI applications.
-   **Docker & Docker Compose:** Chosen to ensure the application and its database dependency can be run easily and consistently anywhere. This simplifies the local development setup to a single command.

---

## Prerequisites

To run this project, you will need to have **Docker** and **Docker Compose** installed on your local machine.
-   [Install Docker Desktop](https://www.docker.com/products/docker-desktop/)

---

## Getting Started

Follow these steps to get the microservice up and running.

**1. Clone the repository:**
```bash
git clone https://github.com/e3mandle6n1/customer-data-listing.git
```

**2. Navigate to the project directory:**
```bash
cd customer-data-listing
```

**3. Build and run the containers using Docker Compose:**
This command will build the Docker image for the API, start a container, and connect.
```bash
docker-compose up --build
```

The API will now be running and accessible. You should see log output from Uvicorn in your terminal, and the API will be available at `http://localhost:8000`.

---

## Usage

### Interactive API Documentation (Swagger UI)

The easiest way to interact with the API is through the automatically generated Swagger UI documentation. Once the containers are running, navigate to the following URL in your web browser:

**[http://localhost:8000/docs](http://localhost:8000/docs)**

Here you can see all available endpoints, their expected parameters, and response models. You can also execute API calls directly from the page.

### API Endpoints

The service exposes the following endpoints:

#### 1. Get a List of All Customers

-   **Endpoint:** `/api/customers`
-   **Method:** `GET`
-   **Description:** Returns a paginated and sorted list of all customers.
-   **Query Parameters:**
    -   `sortBy` (optional): The field to sort by (e.g., `date`, `name`). Defaults to `date`.
    -   `sortDirection` (optional): The direction to sort (`asc` or `desc`). Defaults to `desc`.
    -   `page` (optional): The page number to retrieve. Defaults to `1`.
    -   `pageSize` (optional): The number of customers per page. Defaults to `10`.
-   **`curl` Example:**
    ```bash
    curl -X GET "http://localhost:8000/api/customers?sortBy=date&sortDirection=desc&page=1&pageSize=10"
    ```
-   **Success Response (200 OK):**
    *(The response is an object containing the total count and a list of customer objects)*
    ```json
    {
      "total_count": 2,
      "customers": [
        {
          "id": "d2e3f4a5-b6c7-4d8e-a9b0-00089b0c1d2e",
          "name": "Michael Lewis",
          "email": "michael.lewis@mail.com",
          "created_date": "2025-05-25T11:11:11.010000Z",
          "is_active": true,
          "country_code": "KR"
        },
        {
          "id": "c9d0e1f2-a3b4-4c5d-a6b7-00028a9b0c1d",
          "name": "Michael Lee",
          "email": "michael.lee@mail.com",
          "created_date": "2025-05-20T10:10:10.010000Z",
          "is_active": true,
          "country_code": "KR"
        }
      ]
    }
    ```

#### 2. Get All Unique Country Codes

-   **Endpoint:** `/api/countries`
-   **Method:** `GET`
-   **Description:** Returns a list of all unique country codes present in the customer data.
-   **`curl` Example:**
    ```bash
    curl -X GET "http://localhost:8000/api/countries"
    ```
-   **Success Response (200 OK):**
    *(The response is a list of strings, truncated here for brevity)*
    ```json
    [
      "AE",
      "AR",
      "AT",
      "AU",
      "BD",
      "BE",
      "BR",
      "CA",
      "CH",
      "CL"
    ]
    ```
---

## Deployment Strategy

For a production environment, the following deployment approach is recommended:

1.  **Containerization:** The application is already containerized with Docker, which is the foundation of a modern deployment workflow.
2.  **CI/CD Pipeline:** A CI/CD pipeline (e.g., using GitHub Actions) would be established. On every merge to the `main` branch, this pipeline would:
    -   Run automated tests (e.g., Pytest) to ensure code quality.
    -   Build the Docker image.
    -   Push the versioned image to a container registry (e.g., AWS ECR, Google Artifact Registry, or Docker Hub).
3.  **Deployment Target:** The service would be deployed to a container orchestration or serverless container platform like **Google Cloud Run**, **AWS Fargate**, or a **Kubernetes** cluster.
    -   **Why?** These platforms are ideal for microservices as they handle scaling, availability, and networking, removing the burden of managing underlying server infrastructure.

---

## Future Improvements

-   **Database:** The csv with data setup is for local development only. In production, a managed database service like **AWS RDS**, **Google Cloud SQL**, or **Azure Database for PostgreSQL** should be used for reliability, backups, and scalability.
-   **Authentication & Authorization:** Secure the endpoints using a standard mechanism like OAuth2 with JWT tokens to ensure that only authenticated and authorized users can access or modify data.
-   **Configuration Management:** Externalize configuration (like database URLs, file paths and application settings) using environment variables and a settings management library to avoid hardcoding values.
-   **Logging and Monitoring:** Integrate a structured logging library and expose metrics for monitoring tools like Prometheus and Grafana to observe application health and performance in production.
