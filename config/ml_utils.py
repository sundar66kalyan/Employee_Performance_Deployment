import pandas as pd

def update_results(results_df, result, result_file):
    """
    Add or update a model's performance in the master comparison table.
    """

    model_name = result["Model"]

    # Convert dictionary to single-row DataFrame
    new_row = pd.DataFrame([result])

    # Remove old record if it exists
    results_df = results_df[
        results_df["Model"] != model_name
    ]

    # Append new record
    results_df = pd.concat(
        [results_df, new_row],
        ignore_index=True
    )

    # Sort alphabetically (optional)
    results_df = results_df.sort_values(
        by="Model"
    ).reset_index(drop=True)

    # Save CSV
    results_df.to_csv(
        result_file,
        index=False
    )

    print(f"{model_name} updated successfully.")

    return results_df