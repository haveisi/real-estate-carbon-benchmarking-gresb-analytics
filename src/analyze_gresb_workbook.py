import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "GRESB_Primary_Data_and_Analysis_Guide.xlsx"

OUTPUT_TABLES = PROJECT_ROOT / "outputs" / "tables"
OUTPUT_TABLES.mkdir(parents=True, exist_ok=True)
OUTPUT_CHARTS = PROJECT_ROOT / "outputs" / "charts"
OUTPUT_CHARTS.mkdir(parents=True, exist_ok=True)

def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names for analysis."""
    df = df.copy()
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df


def read_sheet(sheet_name: str) -> pd.DataFrame:
    """Read one sheet and clean column names."""
    df = pd.read_excel(RAW_FILE, sheet_name=sheet_name)
    return clean_columns(df)


def main():
    if not RAW_FILE.exists():
        raise FileNotFoundError(f"Workbook not found: {RAW_FILE}")

    # Read key sheets
    asset_master = read_sheet("01_asset_master")
    energy_monthly = read_sheet("02_energy_monthly")
    water_monthly = read_sheet("03_water_monthly")
    waste_monthly = read_sheet("04_waste_monthly")
    benchmark_data = read_sheet("06_benchmark_data")
    retrofit_options = read_sheet("10_retrofit_options")
    gresb_checklist = read_sheet("11_gresb_evidence_checklist")

    # 1. Asset summary
    asset_summary = pd.DataFrame({
        "metric": [
            "Total asset records",
            "Unique properties",
            "Unique cities",
            "Unique counties",
            "Unique property types"
        ],
        "value": [
            len(asset_master),
            asset_master["property_id"].nunique() if "property_id" in asset_master.columns else None,
            asset_master["city"].nunique() if "city" in asset_master.columns else None,
            asset_master["county"].nunique() if "county" in asset_master.columns else None,
            asset_master["property_type"].nunique() if "property_type" in asset_master.columns else None,
        ]
    })

    asset_summary.to_csv(OUTPUT_TABLES / "asset_summary.csv", index=False)

    # 2. Property type summary
    if "property_type" in asset_master.columns:
        property_type_summary = (
            asset_master
            .groupby("property_type", dropna=False)
            .agg(
                asset_count=("property_id", "nunique"),
                total_floor_area_sqft=("gross_floor_area_sqft", "sum"),
                average_floor_area_sqft=("gross_floor_area_sqft", "mean"),
                total_units=("units", "sum")
            )
            .reset_index()
            .sort_values("asset_count", ascending=False)
        )

        property_type_summary.to_csv(
            OUTPUT_TABLES / "property_type_summary.csv",
            index=False
        )

    # 3. Benchmark metric summary
    benchmark_metric_summary = (
        benchmark_data
        .groupby(["category", "benchmark_metric"], dropna=False)
        .size()
        .reset_index(name="record_count")
        .sort_values("record_count", ascending=False)
    )

    benchmark_metric_summary.to_csv(
        OUTPUT_TABLES / "benchmark_metric_summary.csv",
        index=False
    )

    # 4. Site EUI benchmarks
    if "benchmark_metric" in benchmark_data.columns:
        site_eui = benchmark_data[
            benchmark_data["benchmark_metric"]
            .astype(str)
            .str.contains("site eui", case=False, na=False)
        ].copy()

        if "benchmark_value" in site_eui.columns:
            site_eui["benchmark_value"] = pd.to_numeric(
                site_eui["benchmark_value"],
                errors="coerce"
            )

        site_eui_ranked = site_eui.sort_values(
            "benchmark_value",
            ascending=False
        )

        site_eui_ranked.to_csv(
            OUTPUT_TABLES / "site_eui_benchmarks_ranked.csv",
            index=False
        )

    # 5. Carbon intensity benchmarks
    carbon_intensity = benchmark_data[
        benchmark_data.astype(str).apply(
            lambda row: row.str.contains("carbon", case=False, na=False).any(),
            axis=1
        )
    ].copy()

    carbon_intensity.to_csv(
        OUTPUT_TABLES / "carbon_related_benchmark_records.csv",
        index=False
    )

    # 6. Data center benchmark records
    data_centers = benchmark_data[
        benchmark_data["property_type"]
        .astype(str)
        .str.contains("data center", case=False, na=False)
    ].copy()

    data_centers.to_csv(
        OUTPUT_TABLES / "data_center_benchmark_records.csv",
        index=False
    )

    # 7. Retrofit options summary
    retrofit_summary = retrofit_options.describe(include="all").transpose()
    retrofit_summary.to_csv(
        OUTPUT_TABLES / "retrofit_options_profile.csv"
    )

    # 8. GRESB checklist summary
    if "gresb_area" in gresb_checklist.columns:
        gresb_area_summary = (
            gresb_checklist
            .groupby("gresb_area", dropna=False)
            .size()
            .reset_index(name="indicator_count")
            .sort_values("indicator_count", ascending=False)
        )

        gresb_area_summary.to_csv(
            OUTPUT_TABLES / "gresb_area_summary.csv",
            index=False
        )
    # 9. Chart: Top property types by Site EUI
    if "site_eui_ranked" in locals() and not site_eui_ranked.empty:
        top_site_eui = site_eui_ranked.head(15).copy()

        plt.figure(figsize=(10, 7))
        plt.barh(top_site_eui["property_type"], top_site_eui["benchmark_value"])
        plt.xlabel("Site EUI")
        plt.ylabel("Property Type")
        plt.title("Top Property Types by Site EUI")
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig(OUTPUT_CHARTS / "top_property_types_by_site_eui.png", dpi=300)
        plt.close()

    # 10. Chart: Benchmark records by metric
    if not benchmark_metric_summary.empty:
        metric_counts = (
            benchmark_metric_summary
            .groupby("benchmark_metric")["record_count"]
            .sum()
            .sort_values(ascending=False)
            .head(15)
        )

        plt.figure(figsize=(10, 7))
        plt.barh(metric_counts.index.astype(str), metric_counts.values)
        plt.xlabel("Record Count")
        plt.ylabel("Benchmark Metric")
        plt.title("Top Benchmark Metrics by Record Count")
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig(OUTPUT_CHARTS / "benchmark_metrics_record_count.png", dpi=300)
        plt.close()

    # 11. Chart: Property type asset count
    if "property_type_summary" in locals() and not property_type_summary.empty:
        top_property_types = property_type_summary.head(15).copy()

        plt.figure(figsize=(10, 7))
        plt.barh(top_property_types["property_type"], top_property_types["asset_count"])
        plt.xlabel("Asset Count")
        plt.ylabel("Property Type")
        plt.title("Top Property Types by Asset Count")
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig(OUTPUT_CHARTS / "top_property_types_by_asset_count.png", dpi=300)
        plt.close()

    # 12. Executive summary
    executive_summary = []

    executive_summary.append({
        "finding": "Workbook structure",
        "summary": "The workbook contains asset, energy, water, waste, emissions factor, benchmark, climate risk, EJ/CEJST, retrofit, and GRESB evidence checklist sheets."
    })

    executive_summary.append({
        "finding": "Asset coverage",
        "summary": f"The asset master includes {asset_master['property_id'].nunique()} unique properties across {asset_master['property_type'].nunique()} property types."
    })

    executive_summary.append({
        "finding": "Benchmark coverage",
        "summary": f"The benchmark dataset includes {len(benchmark_data)} benchmark records across {benchmark_data['property_type'].nunique()} property types."
    })

    if "data_centers" in locals():
        executive_summary.append({
            "finding": "Data center benchmarking",
            "summary": f"The benchmark data includes {len(data_centers)} data center-related benchmark records for focused carbon and energy-intensity review."
        })

    if "site_eui_ranked" in locals() and not site_eui_ranked.empty:
        top_property = site_eui_ranked.iloc[0]["property_type"]
        top_value = site_eui_ranked.iloc[0]["benchmark_value"]

        executive_summary.append({
            "finding": "Highest Site EUI benchmark",
            "summary": f"The highest Site EUI benchmark in the dataset is for {top_property}, with a value of {top_value}."
        })

    executive_summary_df = pd.DataFrame(executive_summary)

    executive_summary_df.to_csv(
        OUTPUT_TABLES / "executive_summary_findings.csv",
        index=False
    )

    # 13. Energy summary by property
    energy_summary = (
        energy_monthly
        .groupby(["property_id", "property_name"], dropna=False)
        .agg(
            annual_electricity_kwh=("electricity_kwh", "sum"),
            annual_natural_gas_therms=("natural_gas_therms", "sum"),
            annual_electricity_cost_usd=("electricity_cost_usd", "sum"),
            annual_gas_cost_usd=("natural_gas_cost_usd", "sum"),
            months_with_energy_data=("month", "nunique")
        )
        .reset_index()
    )

    energy_summary.to_csv(
        OUTPUT_TABLES / "energy_summary_by_property.csv",
        index=False
    )

    # 14. Water summary by property
    water_summary = (
        water_monthly
        .groupby(["property_id", "property_name"], dropna=False)
        .agg(
            annual_water_gallons=("water_gallons", "sum"),
            annual_water_cost_usd=("water_cost_usd", "sum"),
            annual_sewer_cost_usd=("sewer_cost_usd", "sum"),
            months_with_water_data=("month", "nunique")
        )
        .reset_index()
    )

    water_summary["annual_total_water_sewer_cost_usd"] = (
        water_summary["annual_water_cost_usd"] +
        water_summary["annual_sewer_cost_usd"]
    )

    water_summary.to_csv(
        OUTPUT_TABLES / "water_summary_by_property.csv",
        index=False
    )

    # 15. Waste summary by property
    waste_summary = (
        waste_monthly
        .groupby(["property_id", "property_name"], dropna=False)
        .agg(
            annual_landfill_tons=("landfill_tons", "sum"),
            annual_recycling_tons=("recycling_tons", "sum"),
            annual_compost_tons=("compost_tons", "sum"),
            annual_waste_cost_usd=("waste_cost_usd", "sum"),
            months_with_waste_data=("month", "nunique")
        )
        .reset_index()
    )

    waste_summary["annual_total_waste_tons"] = (
        waste_summary["annual_landfill_tons"] +
        waste_summary["annual_recycling_tons"] +
        waste_summary["annual_compost_tons"]
    )

    waste_summary["diverted_waste_tons"] = (
        waste_summary["annual_recycling_tons"] +
        waste_summary["annual_compost_tons"]
    )

    waste_summary["waste_diversion_rate"] = (
        waste_summary["diverted_waste_tons"] /
        waste_summary["annual_total_waste_tons"]
    )

    waste_summary.to_csv(
        OUTPUT_TABLES / "waste_summary_by_property.csv",
        index=False
    )

    # 13. Energy summary by property
    energy_summary = (
        energy_monthly
        .groupby(["property_id", "property_name"], dropna=False)
        .agg(
            annual_electricity_kwh=("electricity_kwh", "sum"),
            annual_natural_gas_therms=("natural_gas_therms", "sum"),
            annual_electricity_cost_usd=("electricity_cost_usd", "sum"),
            annual_gas_cost_usd=("natural_gas_cost_usd", "sum"),
            months_with_energy_data=("month", "nunique")
        )
        .reset_index()
    )

    energy_summary["annual_total_energy_cost_usd"] = (
        energy_summary["annual_electricity_cost_usd"] +
        energy_summary["annual_gas_cost_usd"]
    )

    # 14. Water summary by property
    water_summary = (
        water_monthly
        .groupby(["property_id", "property_name"], dropna=False)
        .agg(
            annual_water_gallons=("water_gallons", "sum"),
            annual_water_cost_usd=("water_cost_usd", "sum"),
            annual_sewer_cost_usd=("sewer_cost_usd", "sum"),
            months_with_water_data=("month", "nunique")
        )
        .reset_index()
    )

    water_summary["annual_total_water_sewer_cost_usd"] = (
        water_summary["annual_water_cost_usd"] +
        water_summary["annual_sewer_cost_usd"]
    )

    # 15. Waste summary by property
    waste_summary = (
        waste_monthly
        .groupby(["property_id", "property_name"], dropna=False)
        .agg(
            annual_landfill_tons=("landfill_tons", "sum"),
            annual_recycling_tons=("recycling_tons", "sum"),
            annual_compost_tons=("compost_tons", "sum"),
            annual_waste_cost_usd=("waste_cost_usd", "sum"),
            months_with_waste_data=("month", "nunique")
        )
        .reset_index()
    )

    waste_summary["annual_total_waste_tons"] = (
        waste_summary["annual_landfill_tons"] +
        waste_summary["annual_recycling_tons"] +
        waste_summary["annual_compost_tons"]
    )

    waste_summary["diverted_waste_tons"] = (
        waste_summary["annual_recycling_tons"] +
        waste_summary["annual_compost_tons"]
    )

    waste_summary["waste_diversion_rate"] = (
        waste_summary["diverted_waste_tons"] /
        waste_summary["annual_total_waste_tons"]
    )

    # 16. Merge asset, energy, water, and waste summaries
    property_performance = (
        asset_master
        .merge(energy_summary, on=["property_id", "property_name"], how="left")
        .merge(water_summary, on=["property_id", "property_name"], how="left")
        .merge(waste_summary, on=["property_id", "property_name"], how="left")
    )

    # 17. Calculate energy intensity and utility cost metrics
    property_performance["electricity_kbtu"] = (
        property_performance["annual_electricity_kwh"] * 3.412
    )

    property_performance["natural_gas_kbtu"] = (
        property_performance["annual_natural_gas_therms"] * 100
    )

    property_performance["total_energy_kbtu"] = (
        property_performance["electricity_kbtu"] +
        property_performance["natural_gas_kbtu"]
    )

    property_performance["site_eui_kbtu_sqft"] = (
        property_performance["total_energy_kbtu"] /
        property_performance["gross_floor_area_sqft"]
    )

    property_performance["energy_cost_per_unit"] = (
        property_performance["annual_total_energy_cost_usd"] /
        property_performance["units"]
    )

    property_performance["water_cost_per_unit"] = (
        property_performance["annual_total_water_sewer_cost_usd"] /
        property_performance["units"]
    )

    property_performance["waste_cost_per_unit"] = (
        property_performance["annual_waste_cost_usd"] /
        property_performance["units"]
    )

    property_performance["total_utility_cost_per_unit"] = (
        property_performance["energy_cost_per_unit"] +
        property_performance["water_cost_per_unit"] +
        property_performance["waste_cost_per_unit"]
    )

    # 18. Create simple performance flags
    property_performance["energy_performance_flag"] = property_performance[
        "site_eui_kbtu_sqft"
    ].apply(
        lambda x: "High Energy Use" if x >= 60 else "Moderate/Lower Energy Use"
    )

    property_performance["waste_diversion_flag"] = property_performance[
        "waste_diversion_rate"
    ].apply(
        lambda x: "Weak Diversion" if x < 0.30 else "Moderate/Strong Diversion"
    )

    property_performance["utility_cost_flag"] = property_performance[
        "total_utility_cost_per_unit"
    ].apply(
        lambda x: "High Utility Cost" if x >= 900 else "Moderate/Lower Utility Cost"
    )

    # 19. Export main property performance output
    property_performance.to_csv(
        OUTPUT_TABLES / "property_performance_summary.csv",
        index=False
    )

    # 20. Create priority score
    property_performance["priority_score"] = (
        property_performance["energy_performance_flag"].eq("High Energy Use").astype(int) +
        property_performance["waste_diversion_flag"].eq("Weak Diversion").astype(int) +
        property_performance["utility_cost_flag"].eq("High Utility Cost").astype(int)
    )

    property_performance["priority_flag"] = property_performance[
        "priority_score"
    ].apply(
        lambda x: "High Priority" if x >= 3 else
        "Medium Priority" if x == 2 else
        "Lower Priority"
    )

    property_priority = property_performance.sort_values(
        ["priority_score", "site_eui_kbtu_sqft", "total_utility_cost_per_unit"],
        ascending=[False, False, False]
    )

    property_priority.to_csv(
        OUTPUT_TABLES / "property_priority_ranking.csv",
        index=False
    )

    # 21. Chart: Site EUI by property
    site_eui_chart = property_priority.sort_values(
        "site_eui_kbtu_sqft",
        ascending=False
    )

    plt.figure(figsize=(10, 7))
    plt.barh(site_eui_chart["property_name"], site_eui_chart["site_eui_kbtu_sqft"])
    plt.xlabel("Site EUI (kBtu/sqft)")
    plt.ylabel("Property")
    plt.title("Site EUI by Property")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(OUTPUT_CHARTS / "site_eui_by_property.png", dpi=300)
    plt.close()

    # 22. Chart: Total utility cost per unit
    utility_cost_chart = property_priority.sort_values(
        "total_utility_cost_per_unit",
        ascending=False
    )

    plt.figure(figsize=(10, 7))
    plt.barh(
        utility_cost_chart["property_name"],
        utility_cost_chart["total_utility_cost_per_unit"]
    )
    plt.xlabel("Total Utility Cost per Unit ($)")
    plt.ylabel("Property")
    plt.title("Total Utility Cost per Unit by Property")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(OUTPUT_CHARTS / "utility_cost_per_unit_by_property.png", dpi=300)
    plt.close()

    # 23. Chart: Waste diversion rate
    waste_chart = property_priority.sort_values(
        "waste_diversion_rate",
        ascending=True
    )

    plt.figure(figsize=(10, 7))
    plt.barh(waste_chart["property_name"], waste_chart["waste_diversion_rate"])
    plt.xlabel("Waste Diversion Rate")
    plt.ylabel("Property")
    plt.title("Waste Diversion Rate by Property")
    plt.tight_layout()
    plt.savefig(OUTPUT_CHARTS / "waste_diversion_rate_by_property.png", dpi=300)
    plt.close()


    # 24. Emissions analysis by property
    # Assumptions:
    # - Electricity factor is in kg CO2e per kWh
    # - Natural gas factor is in kg CO2e per therm
    # - If the emissions factor sheet has different names, these default values are used

    electricity_factor_kgco2e_kwh = 0.527779
    natural_gas_factor_kgco2e_therm = 5.31145

    property_performance["scope2_electricity_emissions_tco2e"] = (
        property_performance["annual_electricity_kwh"]
        * electricity_factor_kgco2e_kwh
        / 1000
    )

    property_performance["scope1_natural_gas_emissions_tco2e"] = (
        property_performance["annual_natural_gas_therms"]
        * natural_gas_factor_kgco2e_therm
        / 1000
    )

    property_performance["total_scope1_scope2_emissions_tco2e"] = (
        property_performance["scope2_electricity_emissions_tco2e"]
        + property_performance["scope1_natural_gas_emissions_tco2e"]
    )

    property_performance["emissions_intensity_kgco2e_sqft"] = (
        property_performance["total_scope1_scope2_emissions_tco2e"]
        * 1000
        / property_performance["gross_floor_area_sqft"]
    )

    property_performance["emissions_per_unit_tco2e"] = (
        property_performance["total_scope1_scope2_emissions_tco2e"]
        / property_performance["units"]
    )

    property_performance["carbon_performance_flag"] = property_performance[
        "emissions_intensity_kgco2e_sqft"
    ].apply(
        lambda x: "High Carbon Intensity" if x >= 6 else
        "Moderate Carbon Intensity" if x >= 5 else
        "Lower Carbon Intensity"
    )

    property_emissions = property_performance[
        [
            "property_id",
            "property_name",
            "city",
            "county",
            "state",
            "gross_floor_area_sqft",
            "units",
            "annual_electricity_kwh",
            "annual_natural_gas_therms",
            "scope2_electricity_emissions_tco2e",
            "scope1_natural_gas_emissions_tco2e",
            "total_scope1_scope2_emissions_tco2e",
            "emissions_intensity_kgco2e_sqft",
            "emissions_per_unit_tco2e",
            "carbon_performance_flag"
        ]
    ].sort_values(
        "total_scope1_scope2_emissions_tco2e",
        ascending=False
    )

    property_emissions.to_csv(
        OUTPUT_TABLES / "property_emissions_summary.csv",
        index=False
    )

    # 25. Chart: Total Scope 1 and Scope 2 emissions by property
    emissions_chart = property_emissions.sort_values(
        "total_scope1_scope2_emissions_tco2e",
        ascending=False
    )

    plt.figure(figsize=(10, 7))
    plt.barh(
        emissions_chart["property_name"],
        emissions_chart["total_scope1_scope2_emissions_tco2e"]
    )
    plt.xlabel("Total Scope 1 + Scope 2 Emissions (tCO2e)")
    plt.ylabel("Property")
    plt.title("Total Scope 1 and Scope 2 Emissions by Property")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(OUTPUT_CHARTS / "emissions_by_property.png", dpi=300)
    plt.close()

    # 26. Chart: Carbon intensity by property
    carbon_intensity_chart = property_emissions.sort_values(
        "emissions_intensity_kgco2e_sqft",
        ascending=False
    )

    plt.figure(figsize=(10, 7))
    plt.barh(
        carbon_intensity_chart["property_name"],
        carbon_intensity_chart["emissions_intensity_kgco2e_sqft"]
    )
    plt.xlabel("Carbon Intensity (kg CO2e/sqft)")
    plt.ylabel("Property")
    plt.title("Carbon Intensity by Property")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(OUTPUT_CHARTS / "carbon_intensity_by_property.png", dpi=300)
    plt.close()
    print("Analysis completed.")
    print(f"Outputs saved to: {OUTPUT_TABLES}")


if __name__ == "__main__":
    main()