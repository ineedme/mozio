
# Mozio Geo-pricing API

## Overview

This project provides a powerful and efficient solution for managing providers and their service areas, allowing for dynamic pricing based on geographical location. The API is built with Django REST Framework and PostGIS, offering a robust and scalable platform for geo-pricing applications.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Database](#database)
- [Cache](#cache)
- [Tests](#tests)
- [License](#license)

## Features

- **Provider Management:** Create, read, update, and delete providers, including their contact information and language/currency preferences.
- **Service Area Management:** Define service areas for each provider using polygons, with associated pricing information.
- **Geo-pricing Queries:** Quickly find all providers that serve a specific location, along with their pricing information.
- **Caching:** Improve performance by caching the results of geo-pricing queries.
- **Spatial Indexing:** Optimize geo-pricing queries by using PostGIS's spatial indexing capabilities.

## Requirements

- Python 3.10+
- Django 4.1+
- Django REST Framework 3.14+
- PostGIS 2.5+
- PostgreSQL 12+

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/jules-dourlens/mozio.git
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up the database:**
   - Create a PostgreSQL database with PostGIS enabled.
   - Configure the database connection in `mozio_geo/settings.py`.
4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Start the server:**
   ```bash
   python manage.py runserver
   ```

## Usage

The API is available at `http://localhost:8000/api/v1/`. You can use a tool like `curl` or Postman to interact with the API.

**Note:** After running the server for the first time, you can load the sample data by running the `loaddata` command as described in the "Loading Fixtures" section.

**Example:**

- **Get a list of all providers:**
   ```bash
   curl http://localhost:8000/api/v1/providers/
   ```
- **Get a list of all providers that serve a specific location:**
   ```bash
   curl http://localhost:8000/api/v1/providers/get-providers-in-area/?lat=34.0522&lng=-118.2437
   ```

## API Documentation

The API documentation is available at `http://localhost:8000/swagger/`.

## Loading Fixtures

To load the sample data, run the following command:

```bash
python manage.py loaddata initial_data
```

## Database

The project uses PostgreSQL with PostGIS for storing and querying geographical data. The database schema is defined in `app/providers/models.py`.

## Cache

The project uses Django's caching framework to cache the results of geo-pricing queries. The `ServiceAreaViewSet` is cached for two hours to improve performance. The cache is automatically invalidated whenever a `ServiceArea` is saved or deleted, ensuring that the results of the geo-query endpoint are always up-to-date. The cache is configured in `mozio_geo/settings.py`.

## Tests

The project includes a suite of unit tests to ensure the correctness of the API. To run the tests, use the following command:
```bash
python manage.py test
```

## License

This project is licensed under the MIT License.
