# 🧠 Talk to PDF (FastAPI + React)

Let your users chat with their PDFs using AI — supports chunked vector search, authentication, limits, and Stripe billing.

---

## 🔥 Features

- Upload PDF, split & embed using OpenAI
- Chat with your documents using RAG
- JWT Auth with Signup/Login
- Usage limits (per day, per plan)
- Stripe subscription billing
- Postgres + pgvector support
- Modular & production-ready backend

---

## 🛠️ Tech Stack

- **Backend**: FastAPI, PostgreSQL, SQLAlchemy, pgvector, Pydantic
- **Frontend**: React + Tailwind (to be built)
- **Auth**: JWT
- **Payments**: Stripe
- **Vector Store**: PostgreSQL w/ `pgvector`

---

## 🧪 Quick Start

```bash
git clone https://github.com/pal-sandeep/talk-to-pdf.git
cd talk-to-pdf

python -m venv env
source env/bin/activate

pip install -r requirements.txt

# Set up your database and env vars
cp .env.example .env

uvicorn app.main:app --reload


# FastAPI-Boilerplate

FastAPI Starter: A simple and intuitive example repository showcasing basic functionality and best practices for building web APIs with FastAPI. Use this as a template or reference for accelerating your FastAPI projects

## How to get started

```bash
python3.12 -m venv env
source env/bin/activate
```

Create a .env file following the example `example.env`

`app/config.py` has 3 sets of configurations: Test, Dev, and Prod.

```bash
touch .env
```

Run the following command to install dependencies. `runtime.txt` specifies the runtime version used.

```bash
bash reset.sh
```

## Run the app locally

```bash
python run.py
```

## Run tests.

We use the `TestConfig` to run tests

```bash
bash test.sh
```

## Features

- **Asynchronous SQLAlchemy**: Utilizes SQLAlchemy's asynchronous capabilities to handle database operations efficiently.
- **FastAPI Framework**: Leverages FastAPI for building high-performance APIs with Python 3.8+.
- **Pydantic for Data Validation**: Employs Pydantic models to ensure data integrity and validation.
- **OAuth2 Authentication**: Implements OAuth2 protocols for secure user authentication and authorization.
- **Comprehensive Logging**: Incorporates logging to monitor application behavior and facilitate debugging.
- **Environment-Based Configurations**: Supports multiple configurations (Test, Development, Production) to adapt to various deployment scenarios.

## Project Structure

The application models three primary entities:

- **User**: Represents the application's users.
- **Post**: Denotes content created by users.
- **Tag**: Categorizes posts for better organization.

Relationships between these models are defined as follows:

- A **User** can have multiple **Tags**.
- A **User** can create multiple **Posts**.
- **Posts** and **Tags** share a many-to-many relationship, managed through an association table.

This design facilitates efficient data retrieval and manipulation, adhering to best practices in database normalization.

## Efficient Relationship Loading

To optimize performance, the framework employs selective relationship loading strategies:

- When fetching multiple records of a model, related entities are not loaded by default, reducing unnecessary database queries.
- When retrieving a single record, typically by its ID, related entities are eagerly loaded to provide comprehensive data in one query.

This approach balances performance with data availability, ensuring efficient resource utilization.

## Base Model Class

The project defines a custom `Base` class that all models inherit from. This class includes common configurations and behaviors, promoting code reusability and consistency across the application's data models.