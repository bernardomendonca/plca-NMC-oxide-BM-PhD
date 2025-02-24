# Import BW25 packages.
import bw2data as bd
import bw2calc as bc
import bw2io as bi
import bw2analyzer as bwa
from collections import defaultdict
import pandas as pd
import numpy as np
import textwrap
from collections import defaultdict
import matplotlib.pyplot as plt
import os


from database_setup import find_activity_by_name_product_location
from database_setup import find_activity_by_id
from lifecycle import run_comprehensive_lcia


def modify_activity_permanently(activity, scaling_coefficients, methods_list):
    """
    Permanently modify biosphere exchanges in an activity based on scaling coefficients,
    and run LCIA.

    Parameters:
    - activity: The activity to modify.
    - scaling_coefficients: A dictionary with keys as exchange names (sub_activity)
                            and values as scaling factors.
    - methods_list: A list of tuples representing the impact assessment methods.

    Returns:
    - results_after: LCIA results after the modifications.
    """
    if not scaling_coefficients:
        print("No scaling coefficients provided. Skipping modifications.")
        # Run LCIA without modifications
        results_after = run_comprehensive_lcia(activity, methods_list)
        return results_after

    print("\nApplying scaling coefficients to biosphere exchanges permanently...")
    modified_exchanges = []

    # Modify and save the exchanges permanently
    for exc in activity.exchanges():
        if exc['type'] == 'biosphere':
            # Get the exchange name (biosphere flow name)
            exchange_name = exc.input['name']

            if exchange_name in scaling_coefficients:
                original_amount = exc['amount']
                scaling_factor = scaling_coefficients[exchange_name]
                new_amount = original_amount * scaling_factor  # Calculate new amount

                # Modify the exchange and save it
                exc['amount'] = new_amount
                exc.save()  # Save changes to the database

                modified_exchanges.append((exc, original_amount))  # Store for reporting
                print(f"Modified exchange '{exchange_name}' "
                      f"from amount {original_amount} to new amount: {new_amount}")
            else:
                # No modification needed for this exchange
                pass  # You can print a message if desired

    # Run LCIA after modification
    print("\nLCIA after modification:")
    results_after = run_comprehensive_lcia(activity, methods_list)

    print("Modification complete. The changes have been saved to the database permanently.")

    return results_after  # Return the results from LCIA after modification


def modify_activity_temporarily(activity, scaling_coefficients, methods_list):
    """
    Temporarily modify biosphere exchanges in an activity based on scaling coefficients,
    run LCIA, and revert the changes.

    Parameters:
    - activity: The activity to modify temporarily.
    - scaling_coefficients: A dictionary with keys as exchange names (sub_activity)
                            and values as scaling factors.
    - methods_list: A list of tuples representing the impact assessment methods.

    Returns:
    - results_after: LCIA results after the temporary modifications.
    """
    if not scaling_coefficients:
        print("No scaling coefficients provided. Skipping modifications.")
        # Run LCIA without modifications
        results_after = run_comprehensive_lcia(activity, methods_list)
        return results_after

    print("\nApplying temporary scaling coefficients to biosphere exchanges...")
    original_exchanges = []

    # Store the original exchanges and modify them
    for exc in activity.exchanges():
        if exc['type'] == 'biosphere':
            # Save the original amount
            original_amount = exc['amount']
            original_exchanges.append((exc, original_amount))

            # Get the exchange name (biosphere flow name)
            exchange_name = exc.input['name']

            if exchange_name in scaling_coefficients:
                scaling_factor = scaling_coefficients[exchange_name]
                new_amount = original_amount * scaling_factor  # Calculate new amount

                # Modify the exchange and save it
                exc['amount'] = new_amount
                exc.save()  # Save changes to the database

                print(f"Temporarily modified exchange '{exchange_name}' "
                      f"from amount {original_amount} to new amount: {new_amount}")
            else:
                # No modification needed for this exchange
                pass  # You can print a message if desired

    # Run LCIA after modification
    print("\nLCIA after temporary modification:")
    results_after = run_comprehensive_lcia(activity, methods_list)

    # Revert the exchanges back to original amounts
    print("\nReverting exchanges back to original values...")
    for exc, original_amount in original_exchanges:
        exc['amount'] = original_amount
        exc.save()  # Save changes to the database

    print("Reversion complete.")

    return results_after  # Return the results from LCIA after modification


def modify_activities_in_databases(project_name, databases, years, activity_name, reference_product, location, methods_list, modify_permanently=False, df=None):
    """
    Modify specified biosphere exchanges in the given databases based on coefficients for each year.
    Collect and store results for comparison.

    Parameters:
    - project_name: Name of the Brightway2 project.
    - databases: List of database names.
    - years: List of years corresponding to the databases.
    - activity_name: Name of the main activity to modify.
    - reference_product: Reference product of the main activity.
    - location: Location of the main activity.
    - methods_list: List of impact assessment methods.
    - modify_permanently: Boolean indicating whether to modify permanently or temporarily.
    - df: DataFrame containing the sub-activities and coefficients (optional).

    Returns:
    - results_df: A pandas DataFrame containing the results from all scenarios.
    """
    import pandas as pd
    import bw2data as bd

    # Initialize a list to collect results
    results_list = []

    # Ensure that databases and years lists are of same length
    assert len(databases) == len(years), "Databases and years lists must be of the same length."

    # Loop through each database and corresponding year
    for db_name, year in zip(databases, years):
        print(f"\nProcessing database '{db_name}' for year {year}...")

        # Set the project
        bd.projects.set_current(project_name)

        # Ensure the database is loaded
        if db_name not in bd.databases:
            print(f"Database '{db_name}' not found in the current project.")
            continue

        # Find the activity
        try:
            activity = find_activity_by_name_product_location(db_name, activity_name, reference_product, location)
            print(f"Found activity '{activity_name}' in database '{db_name}'.")
        except ValueError as e:
            print(e)
            continue  # Skip to next database if activity not found

        # Run LCIA before modification
        print("\nLCIA before modification:")
        results_before = run_comprehensive_lcia(activity, methods_list)

        # Check if df (coefficients DataFrame) is provided and contains modifications
        if df is not None and not df.empty:
            # Filter the DataFrame for the activity and VSI_modify == True
            df_activity = df[
                (df['activity_name'] == activity_name) &
                (df['activity_location'] == location) &
                (df['VSI_modify'] == True)
            ]

            # Proceed only if there are modifications to apply
            if not df_activity.empty:
                # Get the coefficient column for the current year
                coeff_column = f'coeff_{year}'
                if coeff_column not in df_activity.columns:
                    print(f"Coefficient column '{coeff_column}' not found in DataFrame.")
                    # Since no modifications, set results_after same as results_before
                    results_after = results_before
                else:
                    # Prepare scaling coefficients dictionary for biosphere exchanges
                    scaling_coefficients = {}
                    for idx, row in df_activity.iterrows():
                        # Get the sub_activity (biosphere exchange name)
                        sub_activity_name = row['sub_activity']

                        # Get the scaling coefficient
                        scaling_coefficient = row[coeff_column]

                        # Ensure the scaling coefficient is a valid number
                        if pd.isnull(scaling_coefficient):
                            print(f"Scaling coefficient for sub_activity '{sub_activity_name}' is NaN. Skipping.")
                            continue

                        scaling_coefficients[sub_activity_name] = scaling_coefficient

                    if not scaling_coefficients:
                        print(f"No valid scaling coefficients found for activity '{activity_name}' in database '{db_name}'.")
                        # Since no modifications, set results_after same as results_before
                        results_after = results_before
                    else:
                        # Modify biosphere exchanges using the updated functions
                        if modify_permanently:
                            results_after = modify_activity_permanently(
                                activity, scaling_coefficients, methods_list
                            )
                        else:
                            results_after = modify_activity_temporarily(
                                activity, scaling_coefficients, methods_list
                            )
            else:
                print(f"No biosphere exchanges to modify for activity '{activity_name}' in database '{db_name}'.")
                # Since no modifications, set results_after same as results_before
                results_after = results_before
        else:
            print(f"No modifications to apply for activity '{activity_name}' in database '{db_name}'.")
            # Since no modifications, set results_after same as results_before
            results_after = results_before

        # Collect results for each method
        for method in methods_list:
            score_before = results_before.get(method, None)
            score_after = results_after.get(method, None)
            if score_before is not None and score_after is not None:
                difference = score_after - score_before
                percent_change = (difference / score_before) * 100 if score_before != 0 else float('inf')
                results_list.append({
                    'Database': db_name,
                    'Year': year,
                    'Activity': activity_name,
                    'Method': method,
                    'Score Before': score_before,
                    'Score After': score_after,
                    'Difference': difference,
                    'Percentage Change': percent_change
                })
            else:
                print(f"Results not available for method: {method}")

        print(f"Modifications and analysis completed for activity '{activity_name}' in database '{db_name}'.")

    # Create a DataFrame from the results list
    results_df = pd.DataFrame(results_list)

    return results_df


def process_all_csvs(project_name, input_folder, methods_list, databases, years, modify_permanently=False):
    """
    Loops through all CSV files in the input folder and modifies corresponding activities
    in the specified databases across multiple years.

    Args:
        input_folder (str): Path to the folder containing the input CSV files. (pre-definied as /input_coefficients for now)
        methods_list (list): List of LCIA methods to be used.
        databases (list): List of databases to be modified.
        years (list): List of years to apply the changes.

    Returns:
        pd.DataFrame: Combined results for all processed activities.
    """
    # Prepare an empty DataFrame to store combined results
    combined_results = pd.DataFrame()

    # Loop through all CSV files in the input folder
    for file_name in os.listdir(input_folder):
        print(f'Processing activity from: {file_name}')
        if file_name.endswith('.csv'):
            # Read the CSV file
            csv_file = os.path.join(input_folder, file_name)
            coeff_df = pd.read_csv(csv_file)

            # Ensure 'VSI_modify' is a boolean
            coeff_df['VSI_modify'] = coeff_df['VSI_modify'].fillna(False).astype(bool)

            # Extract activity details
            activity_id = file_name.replace('.csv', '')  # Extract activity ID from file name
            
            ## BIG WARNING! ##
            # I'm not sure if this might cause issues in the future, but I'm considering the same activity ID across databases
            # Right now, I've checked and when new DBs are generated, they replicate the original activity ID, so this works.
            # Might not be the case in the future!!

            db_name = databases[0]
            activity = find_activity_by_id(db_name, activity_id)
            activity_name = activity.get('name')
            location = activity.get('location')
            reference_product = activity.get('reference product')
            project_name = project_name
            
            # Call the function to modify activities and collect LCIA results
            result_df = modify_activities_in_databases(
                project_name,
                databases, 
                years,
                activity_name, 
                reference_product, 
                location,
                methods_list, 
                modify_permanently=modify_permanently,
                df=coeff_df
            )

            # I need to preserve activity_id for the case in which we get multiple activities with the same name:
            result_df['activity_id'] = activity_id

            # Append results to the combined DataFrame
            combined_results = pd.concat([combined_results, result_df], ignore_index=True)

    return combined_results



def logistic_interpolation(x, x1, y1, x2, y2):
    """
    Perform logistic interpolation for a given x value.

    Parameters:
    - x: The year to interpolate (e.g., 2030).
    - x1: The first known year (e.g., 2025).
    - y1: The coefficient value for x1.
    - x2: The second known year (e.g., 2040).
    - y2: The coefficient value for x2.

    Returns:
    - Interpolated coefficient value for year x.
    """
    # Logistic function parameters
    L = y2  # Upper asymptote
    k = 1 / (x2 - x1)  # Growth rate
    x0 = (x1 + x2) / 2  # Midpoint

    # Logistic function
    return L / (1 + np.exp(-k * (x - x0)))


def process_all_csvs_interpolate(project_name, input_folder, methods_list, databases, years, modify_permanently=False):
    """
    Loops through all CSV files in the input folder and modifies corresponding activities
    in the specified databases across multiple years, interpolating missing coefficients.

    Args:
        input_folder (str): Path to the folder containing the input CSV files.
        methods_list (list): List of LCIA methods to be used.
        databases (list): List of databases to be modified.
        years (list): List of years to apply the changes.
        modify_permanently (bool): Whether to make the changes permanent.

    Returns:
        pd.DataFrame: Combined results for all processed activities.
    """
    # Prepare an empty DataFrame to store combined results
    combined_results = pd.DataFrame()

    # Loop through all CSV files in the input folder
    for file_name in os.listdir(input_folder):
        print(f'Processing activity from: {file_name}')
        if file_name.endswith('.csv'):
            # Read the CSV file
            csv_file = os.path.join(input_folder, file_name)
            coeff_df = pd.read_csv(csv_file)

            # Ensure 'VSI_modify' is a boolean
            coeff_df['VSI_modify'] = coeff_df['VSI_modify'].fillna(False).astype(bool)

            # Interpolate missing coefficients for each row
            for index, row in coeff_df.iterrows():
                # Get known coefficient values
                coeff_2025 = row['coeff_2025']
                coeff_2040 = row['coeff_2040']

                # Interpolate missing coefficients using logistic function
                if np.isnan(row.get('coeff_2030', np.nan)):
                    coeff_df.at[index, 'coeff_2030'] = logistic_interpolation(2030, 2025, coeff_2025, 2040, coeff_2040)
                if np.isnan(row.get('coeff_2035', np.nan)):
                    coeff_df.at[index, 'coeff_2035'] = logistic_interpolation(2035, 2025, coeff_2025, 2040, coeff_2040)

            # Extract activity details
            activity_id = file_name.replace('.csv', '')  # Extract activity ID from file name
            
            ## BIG WARNING! ##
            # I'm not sure if this might cause issues in the future, but I'm considering the same activity ID across databases
            # Right now, I've checked and when new DBs are generated, they replicate the original activity ID, so this works.
            # Might not be the case in the future!!
            
            db_name = databases[0]
            activity = find_activity_by_id(db_name, activity_id)
            activity_name = activity.get('name')
            location = activity.get('location')
            reference_product = activity.get('reference product')
            project_name = project_name

            # Call the function to modify activities and collect LCIA results
            result_df = modify_activities_in_databases(
                project_name, 
                databases, 
                years,
                activity_name, 
                reference_product, 
                location,
                methods_list, 
                modify_permanently=modify_permanently,
                df=coeff_df
            )

            # I need to preserve activity_id for the case in which we get multiple activities with the same name:
            result_df['activity_id'] = activity_id

            # Append results to the combined DataFrame
            combined_results = pd.concat([combined_results, result_df], ignore_index=True)

    return combined_results