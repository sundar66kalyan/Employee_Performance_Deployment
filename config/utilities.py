"""
=========================================================
Utility Functions
=========================================================
"""

import pandas as pd


def separator(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def dataset_summary(df):
    separator("Dataset Shape")
    print(df.shape)

    separator("Data Types")
    print(df.dtypes)


def missing_report(df):
    return pd.DataFrame({
        "Missing Values": df.isnull().sum(),
        "Percentage": (df.isnull().mean() * 100).round(2)
    })


def duplicate_report(df):
    return df.duplicated().sum()


def save_dataframe(df, path):
    df.to_csv(path, index=False)
    print(f"Data saved to: {path}")


def load_dataframe(path):
    return pd.read_csv(path)