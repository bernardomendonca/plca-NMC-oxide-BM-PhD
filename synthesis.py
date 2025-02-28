import pandas as pd

def load_csv(file_path):
    """Load CSV file into a DataFrame."""
    return pd.read_csv(file_path)

def filter_activities(df, activities):
    """Filter DataFrame for the specified activities."""
    return df[df['Activity'].isin([act[0] for act in activities])]

def extract_year_data(df, year, score_column):
    """Extract data for a specific year and assign the correct score column."""
    return df[df['Year'] == year][['Activity', 'Method', score_column]]

def compute_changes(baseline_df, vsi_df, activities):
    """
    Compare impact changes between first and last year for each activity and category.
    

    [Note BM: Need to significantly improve this]
    - Baseline uses 'Score Before'
    - VSI uses 'Score After'
    
    Returns a summary DataFrame.
    """
    results = []

    for activity, location in activities:
        # Extract Baseline data
        baseline_2025 = extract_year_data(baseline_df[baseline_df['Activity'] == activity], 2025, 'Score Before')
        baseline_2040 = extract_year_data(baseline_df[baseline_df['Activity'] == activity], 2040, 'Score Before')

        # Extract VSI data
        vsi_2025 = extract_year_data(vsi_df[vsi_df['Activity'] == activity], 2025, 'Score After')
        vsi_2040 = extract_year_data(vsi_df[vsi_df['Activity'] == activity], 2040, 'Score After')

        for method in baseline_2025['Method'].unique():
            base_2025 = baseline_2025[baseline_2025['Method'] == method]['Score Before'].values
            base_2040 = baseline_2040[baseline_2040['Method'] == method]['Score Before'].values
            vsi_2025_val = vsi_2025[vsi_2025['Method'] == method]['Score After'].values
            vsi_2040_val = vsi_2040[vsi_2040['Method'] == method]['Score After'].values

            if len(base_2025) > 0 and len(base_2040) > 0:
                base_change = base_2040[0] - base_2025[0]
                base_pct_change = (base_change / base_2025[0]) * 100 if base_2025[0] != 0 else 0
            else:
                base_change, base_pct_change = None, None

            if len(vsi_2025_val) > 0 and len(vsi_2040_val) > 0:
                vsi_change = vsi_2040_val[0] - vsi_2025_val[0]
                vsi_pct_change = (vsi_change / vsi_2025_val[0]) * 100 if vsi_2025_val[0] != 0 else 0
            else:
                vsi_change, vsi_pct_change = None, None

            if len(base_2040) > 0 and len(vsi_2040_val) > 0:
                vsi_to_baseline_change = vsi_2040_val[0] - base_2040[0]
                vsi_to_baseline_pct_change = (vsi_pct_change - base_pct_change)

            results.append({
                "Activity": activity,
                "Location": location,
                "Impact Category": method,
                "Baseline 2025": base_2025[0] if len(base_2025) > 0 else None,
                "Baseline 2040": base_2040[0] if len(base_2040) > 0 else None,
                "Baseline Change": base_change,
                "Baseline % Change": base_pct_change,
                "VSI 2025": vsi_2025_val[0] if len(vsi_2025_val) > 0 else None,
                "VSI 2040": vsi_2040_val[0] if len(vsi_2040_val) > 0 else None,
                "VSI Change": vsi_change,
                "VSI % Change": vsi_pct_change,
                "VSI to baseline change": vsi_to_baseline_change,
                "VSI to baseline change %": vsi_to_baseline_pct_change
            })

    return pd.DataFrame(results)

def analyze_impacts(baseline_file, vsi_file, activities):
    """Main function to load data, filter activities, and compute changes."""
    baseline_df = load_csv(baseline_file)
    vsi_df = load_csv(vsi_file)

    baseline_df = filter_activities(baseline_df, activities)
    vsi_df = filter_activities(vsi_df, activities)

    results_df = compute_changes(baseline_df, vsi_df, activities)

    return results_df
