# Real Estate ESG Readiness & Multifamily Building Performance Analytics

This project uses Python to review and summarize a multifamily real estate sustainability workbook. The workbook includes property data, monthly energy use, water use, waste data, emissions factors, benchmark targets, climate risk indicators, environmental justice context, retrofit options, and a GRESB-style evidence checklist.

The purpose of the project is to turn workbook-based sustainability data into cleaner outputs that can support ESG reporting readiness, building-performance review, and early-stage decarbonization planning.

## Why This Project Matters

Real estate ESG reporting depends on clean and traceable data. Before a portfolio can be used for GRESB-style reporting, benchmarking, retrofit planning, or dashboard development, the underlying data needs to be checked, organized, and summarized.

This project demonstrates that early analytics workflow: moving from a structured Excel workbook to Python-generated tables and charts that are easier to review, share, and build on.

## Project Scope

The current workbook supports multifamily-focused ESG readiness and building-performance analysis. It is not presented as a full national real estate benchmark dataset.

The analysis covers:

* Property and asset profile data
* Monthly energy consumption and utility cost
* Monthly water consumption and sewer cost
* Waste generation and diversion
* Emissions factors
* Benchmark targets
* Climate risk indicators
* Environmental justice context
* Retrofit options
* GRESB-style evidence checklist items

## Tools Used

* Python
* pandas
* openpyxl
* matplotlib
* Excel
* PyCharm
* GitHub

## Repository Structure

```text
real-estate-carbon-benchmarking-gresb-analytics/
│
├── data/
│   ├── raw/              # Local raw workbook location; not committed if excluded by .gitignore
│   └── processed/
│
├── outputs/
│   ├── tables/
│   └── charts/
│
├── src/
│   └── analyze_gresb_workbook.py
│
├── docs/
├── images/
├── README.md
├── requirements.txt
└── .gitignore
```

## Current Workflow

The main Python script:

1. Reads the Excel workbook.
2. Inspects worksheet names, row counts, column counts, and fields.
3. Standardizes column names.
4. Summarizes key workbook sheets.
5. Reviews benchmark metrics and Site EUI targets.
6. Extracts carbon-related benchmark records.
7. Identifies data-center-related records when present.
8. Profiles retrofit options.
9. Summarizes GRESB-style evidence categories.
10. Exports clean tables and charts for review.

## Workbook Sheets Reviewed

The workbook currently includes:

* `01_asset_master`
* `02_energy_monthly`
* `03_water_monthly`
* `04_waste_monthly`
* `05_emission_factors`
* `06_benchmark_data`
* `07_community_acs`
* `08_climate_risk_fema`
* `09_ej_cejst`
* `10_retrofit_options`
* `11_gresb_evidence_checklist`
* `02_energy_summary_template`
* `Calculation_Guide`
* `Data_Dictionary`

## Current Outputs

Generated table outputs include:

* `workbook_sheet_summary.csv`
* `asset_summary.csv`
* `property_type_summary.csv`
* `benchmark_metric_summary.csv`
* `site_eui_benchmarks_ranked.csv`
* `carbon_related_benchmark_records.csv`
* `data_center_benchmark_records.csv`
* `retrofit_options_profile.csv`
* `gresb_area_summary.csv`
* `executive_summary_findings.csv`

Generated chart outputs include:

* `top_property_types_by_site_eui.png`
* `benchmark_metrics_record_count.png`
* `top_property_types_by_asset_count.png`

Outputs are saved in:

```text
outputs/tables/
outputs/charts/
```

## Current Findings

The workbook is structured for multifamily ESG readiness and building-performance analysis. It includes the core data categories needed for a GRESB-style preparation workflow, including asset data, utility performance, emissions factors, benchmarks, climate risk, environmental justice indicators, retrofit options, and evidence tracking.

The benchmark data currently visible in the workbook is focused on multifamily housing. For that reason, this repository is positioned as a multifamily ESG readiness and building-performance analytics project.

This repository should not be described as a 103,000-record or 89,634-asset benchmarking project unless the separate source dataset for that larger analysis is added and analyzed here.

## Data Note

This project uses workbook-based data for demonstration and portfolio-development purposes. Sensitive, proprietary, or tenant-level data should not be uploaded publicly.

Public GitHub materials should use anonymized, simulated, or summary-level outputs unless the original source data is confirmed to be public and shareable.

## How to Run the Analysis

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate the environment:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run the analysis:

```powershell
python src\analyze_gresb_workbook.py
```

## Next Development Steps

Planned next steps include:

* Build property-level energy, water, waste, and emissions summaries
* Merge asset data with monthly utility and waste records
* Calculate Site EUI and carbon intensity by property
* Rank properties by performance and data-readiness risk
* Add retrofit prioritization outputs
* Create Power BI dashboard visuals
* Add a short methodology note for GRESB-style reporting readiness
