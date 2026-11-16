# E-commerce Data Engineering | Databricks Lakehouse

## Overview

This personal data engineering project processes e-commerce order transactions into clean, analytics-ready datasets using a Bronze, Silver and Gold lakehouse design. It focuses on order deduplication, reliable repeat processing and daily revenue reporting.

The repository contains a local Python implementation, a PySpark notebook and Databricks job configuration. All source data is synthetic.

## Technology Stack

- Azure Databricks, Apache Spark (PySpark) and Delta Lake
- Python and SQLite for local processing and validation
- Databricks Asset Bundles for job configuration
- Git and GitHub for version control

## Data Processing

| Layer | Responsibilities |
| --- | --- |
| Bronze | Ingest raw order transactions and preserve source records. |
| Silver | Clean order data, handle duplicates and identify the latest order state using event timestamps. |
| Gold | Aggregate daily revenue and paid-order metrics, excluding cancelled orders from paid revenue. |

## Data Quality and Reliability

- Order deduplication and latest-record selection.
- Repeat processing without duplicate writes in the local implementation.
- Order cancellation handling and revenue validation.
- Automated tests for core business rules.

## Repository Structure

| Path | Description |
| --- | --- |
| `data/` | Synthetic order data and dataset documentation |
| `notebooks/` | PySpark and Delta Lake notebook |
| `resources/` | Databricks job configuration |
| `src/` | Local Python implementation |
| `tests/` | Automated tests |
| `databricks.yml` | Databricks Asset Bundle configuration |

## Local Execution

Run the following commands from the repository root using Python 3:

```bash
python src/local_demo.py
python -m unittest discover -s tests -v
```

## Implementation Status

The local Python tests passed in the initial development environment. The PySpark notebook and deployment configuration are included; execution and deployment in a live Azure Databricks workspace are pending validation.

## Planned Enhancements

- Incremental ingestion using Delta MERGE.
- SCD Type 2 for historical dimension tracking.
- Automated CI/CD, pipeline monitoring and alerting.
- Power BI integration for business reporting.
