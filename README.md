# Real Estate ESG Readiness & Multifamily Building Performance Analytics

This project uses Python to review and summarize a multifamily real estate sustainability workbook. The workbook brings together property data, monthly energy use, water use, waste data, emissions factors, benchmark targets, climate risk indicators, environmental justice context, retrofit options, and a GRESB-style evidence checklist.

The goal is simple: turn a structured Excel workbook into cleaner, more useful outputs that can support ESG reporting readiness, building-performance review, and early-stage decarbonization planning.

## Why I Built This

Real estate sustainability work often starts with scattered workbook data. Before a portfolio can be used for reporting, benchmarking, retrofit planning, or dashboard development, the data needs to be checked, organized, and summarized.

This project shows that workflow in practice. It focuses on the early but important step of moving from workbook-based data to clean Python-generated tables and charts.

## Project Scope

This repository focuses on a multifamily real estate portfolio workbook. The current analysis supports ESG readiness and building-performance review at the property level.

The workbook includes:

* Property and asset profile data
* Monthly energy consumption and utility cost
* Monthly water consumption and sewer cost
* Waste generation and diversion data
* Emissions factors
* Benchmark targets
* Climate risk indicators
* Environmental justice context
* Retrofit options
* GRESB-style evidence checklist items

This project is not presented as a full national real estate benchmark dataset. The current workbook supports multifamily-focused ESG readiness analysis.

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
│   ├── raw/
│   │   └── GRESB_Primary_Data_and_Analysis_Guide.xlsx
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

## Current Python Workflow

The main script reads the workbook, checks its structure, cleans column names, summarizes key sheets, and exports analysis outputs.

Current outputs include:

* Workbook sheet summary
* Asset summary
* Property type summary
* Benchmark metric summary
* Site EUI benchmark ranking
* Carbon-related benchmark records
* Data center benchmark records, where available in the workbook
* Retrofit options profile
* GRESB area summary
* Executive summary findings
* Initial benchmark charts

Generated files are saved in:

```text
outputs/tables/
outputs/charts/
```

## Workbook Sheets Reviewed

The workbook currently includes these sheets:

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

## Methodology

The analysis follows a practical workflow:

1. Read the Excel workbook.
2. Inspect sheet names, row counts, column counts, and fields.
3. Standardize column names for easier analysis.
4. Summarize asset and property-type data.
5. Review benchmark metrics and Site EUI targets.
6. Extract carbon-related benchmark records.
7. Identify data center-related records when they are present in the workbook.
8. Profile retrofit options.
9. Summarize GRESB-style evidence categories.
10. Export clean tables and charts for portfolio review.

## Current Findings

The workbook is structured for multifamily ESG readiness and building-performance analysis. It includes the core data categories needed for a GRESB-style preparation workflow: asset data, utility performance, emissions factors, benchmarks, climate risk, environmental justice indicators, retrofit options, and evidence tracking.

The benchmark data currently visible in the workbook is focused on multifamily housing. For that reason, this repository is positioned as a multifamily ESG readiness and building-performance analytics project.

This repository should not be described as a 103,000-record or 89,634-asset benchmarking project unless the separate source dataset for that larger analysis is added and analyzed here.

## Example Outputs

Current table outputs include:

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

Current chart outputs include:

* `top_property_types_by_site_eui.png`
* `benchmark_metrics_record_count.png`
* `top_property_types_by_asset_count.png`

## Data Note

This project uses workbook-based project data for demonstration and portfolio-development purposes. Sensitive, proprietary, or tenant-level data should not be uploaded publicly.

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

Outputs will be saved to:

```text
outputs/tables/
outputs/charts/
```

## Why This Project Matters

GRESB-style reporting and real estate decarbonization planning depend on clean and traceable data. This project demonstrates how a sustainability workbook can be reviewed and converted into structured outputs that are easier to use for reporting readiness, portfolio review, and future dashboard development.

The current version is an early-stage analytics workflow. It sets the foundation for deeper property-level analysis, including Site EUI, emissions intensity, utility cost, waste diversion, data-readiness checks, and retrofit prioritization.

## Next Development Steps

Planned next steps include:

* Build property-level energy, water, waste, and emissions summaries
* Merge asset data with monthly utility and waste records
* Calculate Site EUI and carbon intensity by property
* Rank properties by performance and data-readiness risk
* Add retrofit prioritization outputs
* Create Power BI dashboard visuals
* Add a short methodology note for GRESB-style reporting readiness
