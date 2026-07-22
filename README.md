# IS218 Module 11

## Description

This project implements a SQLAlchemy Calculation model, Pydantic
validation schemas, a calculation factory, PostgreSQL integration
tests, Docker, and a GitHub Actions CI/CD pipeline.

## Supported Operations

- Add
- Sub
- Multiply
- Divide

## Calculation Model

The Calculation model stores:

- id
- user_id
- a
- b
- type
- result

The result is calculated using the CalculationFactory and stored
in PostgreSQL.

## Local Setup

```bash
git clone git@github.com:davidcruzzy03/IS218-Module11.git
cd IS218-Module11

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt