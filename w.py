import pandas as pd
import numpy as np

# ============================================================
# 1. LOAD ORIGINAL DATASET
# ============================================================

file_path = r"orignal.csv"

df = pd.read_csv(file_path)

print("Original rows:", len(df))


# ============================================================
# 2. CLEAN PRICE
# ============================================================

df["Price"] = (
    df["Price"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.strip()
)

df["Price"] = pd.to_numeric(
    df["Price"],
    errors="coerce"
)


# ============================================================
# 3. SAVE ORIGINAL PRICE
# ============================================================

# This is our safety copy.
df["Price_Original"] = df["Price"]


# ============================================================
# 4. REAL-WORLD ORGANISATION BENCHMARKS
#    USD MILLION PER MISSION
# ============================================================

org_benchmark = {

    "SpaceX": 57.5,
    "CASC": 40.33,
    "Roscosmos": 50.0,
    "ULA": 187.4,
    "JAXA": 59.33,
    "Northrop": 53.67,
    "ExPace": 6.0,
    "IAI": 30.0,
    "Rocket Lab": 7.5,
    "Virgin Orbit": 12.0,
    "VKS RF": 90.0,
    "MHI": 90.0,

    # No reliable comparable public benchmark
    "IRGC": np.nan,

    "Arianespace": 107.29,
    "ISA": 30.0,
    "Blue Origin": 68.0,
    "ISRO": 20.0,
    "Exos": 0.30,
    "ILS": 65.0,
    "i-Space": 5.0,
    "OneSpace": 3.10,
    "Landspace": 25.0,
    "Eurockot": 35.0,
    "Land Launch": 42.5,
    "CASIC": 6.0,

    # Deliberately left out because the public figure
    # is programme expenditure, not comparable launch price
    "KCST": np.nan,

    "Sandia": np.nan,

    "Kosmotras": 30.0,
    "Khrunichev": 72.5,
    "Sea Launch": 90.0,
    "KARI": 30.0,
    "ESA": 107.29,
    "NASA": 1003.33,
    "Boeing": 137.0,
    "ISAS": 70.0,

    "SRC": np.nan,

    "MITT": 9.0,
    "Lockheed": 153.0,
    "AEB": 6.5,
    "Starsem": 50.0,
    "RVSN USSR": 27.0,
    "EER": 20.0,
    "General Dynamics": 85.0,
    "Martin Marietta": 225.0,
    "Yuzhmash": 42.5,
    "Douglas": 50.0,
    "ASI": 41.0,
    "US Air Force": 350.0,
    "CNES": 107.29,
    "CECLES": np.nan,
    "RAE": 8.0,
    "UT": 90.0,
    "OKB-586": 42.5,

    # Dataset has encoding corruption in this organisation name
    "Arm??e de l'Air": 12.4,

    "US Navy": 8.91
}


# ============================================================
# 5. CLEAN ORGANISATION NAMES
# ============================================================

df["Organisation"] = (
    df["Organisation"]
    .astype(str)
    .str.strip()
)


# ============================================================
# 6. MAP EXTERNAL BENCHMARK
# ============================================================

df["External_Benchmark_M"] = (
    df["Organisation"]
    .map(org_benchmark)
)


# ============================================================
# 7. IMPUTE ONLY NULL PRICES
# ============================================================

missing_before = df["Price"].isna().sum()

imputation_mask = (
    df["Price"].isna()
    & df["External_Benchmark_M"].notna()
)

df.loc[
    imputation_mask,
    "Price"
] = df.loc[
    imputation_mask,
    "External_Benchmark_M"
]


# ============================================================
# 8. CREATE SOURCE FLAG
# ============================================================

df["Price_Source"] = np.where(
    df["Price_Original"].notna(),
    "Original Observed",
    np.where(
        df["External_Benchmark_M"].notna(),
        "Real-World Organisation Benchmark",
        "Still Missing"
    )
)


# ============================================================
# 9. CHECK WHAT HAPPENED
# ============================================================

missing_after = df["Price"].isna().sum()

imputed_count = (
    df["Price_Source"]
    == "Real-World Organisation Benchmark"
).sum()

original_count = (
    df["Price_Source"]
    == "Original Observed"
).sum()


print("\n" + "=" * 70)
print("PRICE IMPUTATION RESULTS")
print("=" * 70)

print(f"Total missions              : {len(df):,}")
print(f"Original observed prices    : {original_count:,}")
print(f"Original missing prices     : {missing_before:,}")
print(f"Successfully imputed       : {imputed_count:,}")
print(f"Still missing              : {missing_after:,}")


# ============================================================
# 10. SHOW UNRESOLVED ORGANISATIONS
# ============================================================

unresolved = (
    df.loc[
        df["Price"].isna(),
        "Organisation"
    ]
    .value_counts()
)

print("\n" + "=" * 70)
print("STILL MISSING PRICE")
print("=" * 70)

print(unresolved)


# ============================================================
# 11. CRITICAL SAFETY CHECK
# ============================================================

# Verify that NO originally known Price was changed.

known_mask = df["Price_Original"].notna()

changed_known_prices = (
    df.loc[known_mask, "Price"]
    != df.loc[known_mask, "Price_Original"]
).sum()

print("\n" + "=" * 70)
print("SAFETY CHECK")
print("=" * 70)

print(
    "Originally known prices changed:",
    changed_known_prices
)

assert changed_known_prices == 0, \
    "STOP: An originally observed Price was modified."


# ============================================================
# 12. SAVE FINAL DATASET
# ============================================================

output_file = "Space_Mission_Data_RealWorld_Imputed.csv"

df.to_csv(
    output_file,
    index=False
)

print("\nSaved:", output_file)


# ============================================================
# 13. FINAL PRICE SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("FINAL PRICE SUMMARY")
print("=" * 70)

print(df["Price"].describe())