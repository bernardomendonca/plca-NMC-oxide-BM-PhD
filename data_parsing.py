import pandas as pd
import os

def combine_csvs_into_excel(
    folder_path, 
    csv_list, 
    output_file, 
    activity_col="activity_id"
):
    import os
    import pandas as pd

    df_list = []
    for csv_name in csv_list:
        full_path = os.path.join(folder_path, csv_name)
        df = pd.read_csv(full_path)
        df_list.append(df)
    
    # Concatenate all CSV data
    df_combined = pd.concat(df_list, ignore_index=True)
    
    # Create Excel writer
    writer = pd.ExcelWriter(output_file, engine="openpyxl")

    # Group by your chosen column
    grouped = df_combined.groupby(activity_col)

    # Enumerate each group, starting from 1
    for i, (idx_value, subdf) in enumerate(grouped, start=1):
        # Instead of using idx_value in the sheet name,
        # use a simple sequential index i
        sheet_name = f"EF Contributions_{i}"

        # Write group to sheet
        subdf.to_excel(writer, sheet_name=sheet_name, index=False)

    # Close the writer (instead of .save())
    writer.close()
    print(f"Excel file saved as: {output_file}")

def combine_csvs_in_order(
    folder_path,
    csv_list,
    output_file,
    activity_col="activity_id"
):
    """
    Reads each CSV in `csv_list` in order, groups by `activity_col`,
    and writes each group to a new Excel sheet. The sheets for the
    first CSV appear first, followed by the sheets from the second CSV, etc.

    Sheet names are "File{i}_Group{j}", where:
      - i = index of the CSV file in `csv_list` (1-based)
      - j = index of the group within that CSV (also 1-based)

    Parameters
    ----------
    folder_path : str
        Path to the folder containing your CSV files.
    csv_list : list of str
        Filenames of the CSVs to process, in the exact order desired.
    output_file : str
        Path (including filename) for the resulting Excel file.
    activity_col : str
        The column name in the CSV(s) to group by. Defaults to 'activity_id'.
    """
    writer = pd.ExcelWriter(output_file, engine="openpyxl")

    # Go through each CSV in the provided order
    for csv_idx, csv_name in enumerate(csv_list, start=1):
        full_path = os.path.join(folder_path, csv_name)
        df = pd.read_csv(full_path)

        # Group rows by the given column
        grouped = df.groupby(activity_col)

        # Write each group to a separate sheet
        for group_idx, (group_key, subdf) in enumerate(grouped, start=1):
            sheet_name = f"File{csv_idx}_Group{group_idx}"
            subdf.to_excel(writer, sheet_name=sheet_name, index=False)

    writer.close()
    print(f"Excel file saved as: {output_file}")
