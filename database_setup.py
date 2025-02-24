# Import BW25 packages.
import bw2data as bd
import bw2io as bi
import bw2calc as bc
import bw2analyzer as bwa

import pandas as pd
import numpy as np

import textwrap

from collections import defaultdict

import matplotlib.pyplot as plt

import os
import ast


def find_activity_by_name_product_location(db_name, activity_name, reference_product=None, location=None):
    """
    Find an activity by name, reference product, and location in a given database.
    
    Parameters:
    - db_name: The name of the database to search.
    - activity_name: The name of the activity to search for.
    - reference_product: The reference product to filter the search (optional).
    - location: The location to filter the search (optional).
    
    Returns:
    - activity: The activity object found in the database.
    """
    db = bd.Database(db_name)
    search_results = db.search(activity_name)
    
    if not search_results:
        raise ValueError(f"Activity '{activity_name}' not found in database '{db_name}'")
    
    # Filter by reference product if provided
    if reference_product:
        search_results = [
            act for act in search_results if act['reference product'] == reference_product
        ]
        
        if not search_results:
            raise ValueError(f"No activity found with reference product '{reference_product}' for '{activity_name}'")
    
    # Filter by location if provided
    if location:
        search_results = [
            act for act in search_results if act['location'] == location
        ]
        
        if not search_results:
            raise ValueError(f"No activity found with location '{location}' for '{activity_name}' and '{reference_product}'")
    
    # Return the first match that has the correct filters applied
    return search_results[0]



def find_activity_by_id(db_name, activity_id):

    db = bd.Database(db_name)
    activity = db.get(activity_id)

    if not activity:
        raise ValueError(f"Activity ID '{activity_id}' not found in database '{db_name}'")


    print(f'activity recovered: {activity}')
    return activity



def results_to_dataframe(results, project_name, db_name):
    """
    Converts the results dictionary into a pandas DataFrame, including additional details like
    project name, database name, activity information, exchange details, and splits the compartment
    into compartment and sub_compartment.

    Parameters:
    - results: Dictionary containing the calculation results.
    - project_name: Name of the Brightway2 project.
    - db_name: Name of the database used.

    Returns:
    - df: A pandas DataFrame with the structured results.
    """
    import pandas as pd

    # Convert dictionary to list of rows
    rows = []
    for key, result in results.items():
        activity_name = key[0]
        method = key[2]  # Ensure this is the method tuple (method, category, indicator)
        activity = result['activity']
        exchange_list = result['impacts']

        # Extract activity attributes
        activity_unit = activity.get('unit', None)
        activity_location = activity.get('location', None)
        activity_code = activity.get('code', None)
        activity_database = activity.get('database', None)
        activity_id = (activity_database, activity_code)  # Unique ID for the main activity
        activity_categories = ' | '.join(activity.get('categories', ())) if 'categories' in activity else None

        # Include production exchange details if needed
        production_exchanges = list(activity.production())
        if production_exchanges:
            production_exchange = production_exchanges[0]
            production_amount = production_exchange['amount']
            production_unit = production_exchange.input.get('unit', None)
            production_location = production_exchange.input.get('location', None)
        else:
            production_amount = None
            production_unit = None
            production_location = None

        # Calculate total impact for the category
        total_impact = sum(exchange['impact'] for exchange in exchange_list)
        
        for exchange_details in exchange_list:
            # Handle compartment and sub_compartment
            if 'compartment' in exchange_details and exchange_details['compartment']:
                compartment_tuple = exchange_details['compartment']
                if len(compartment_tuple) >= 1:
                    compartment = compartment_tuple[0]
                    if len(compartment_tuple) > 1:
                        sub_compartment = ' | '.join(compartment_tuple[1:])
                    else:
                        sub_compartment = None
                else:
                    compartment = None
                    sub_compartment = None
            else:
                compartment = None
                sub_compartment = None

            # Check the length of method to avoid 'index out of range' error
            if len(method) == 3:
                impact_method, impact_category, impact_indicator = method
            elif len(method) == 2:
                impact_method, impact_category = method
                impact_indicator = None  # Default if the third element is missing
            elif len(method) == 1:
                impact_method = method[0]
                impact_category = None
                impact_indicator = None

            row = {
                'project_name': project_name,          # Include project name
                'db_name': db_name,                    # Include database name
                'activity_id': activity_id,            # Unique ID for the main activity
                'activity_name': activity_name,
                'activity_unit': activity_unit,
                'activity_location': activity_location,
                'impact_method': impact_method,
                'impact_category': impact_category,
                'impact_indicator': impact_indicator,
                'sub_activity_id': exchange_details['exchange_id'],  # Unique ID for sub-activity
                'sub_activity': exchange_details['exchange_name'],
                'sub_activity_unit': exchange_details['exchange_unit'],
                'sub_activity_location': exchange_details['exchange_location'],
                'value': float(exchange_details['impact']),
                'percentage': float(exchange_details['impact'] / total_impact * 100 if total_impact > 0 else 0),  # Include percentage
                'total_impact': float(total_impact),   # Include total impact for the category
                'exchange_type': exchange_details['type'],
                'compartment': compartment,
                'sub_compartment': sub_compartment,
                'production_amount': production_amount,
                'production_unit': production_unit,
                'production_location': production_location,
                'activity_categories': activity_categories
            }
            rows.append(row)

    # Create DataFrame
    df = pd.DataFrame(rows)
    return df



def convert_excel_to_csvs(input_excel, output_folder):
    """
    Converts specific tabs in an Excel file into separate CSV files,
    saving them in a folder named 'input_coefficients'.
    Extracts only the alphanumeric part of 'activity_id' for file names.

    Args:
        input_excel (str): Path to the input Excel file.
        
    Returns:
        None
    """
    # Define the output folder
    output_folder = output_folder
    
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Load the Excel file
    excel_data = pd.ExcelFile(input_excel)
    
    # Filter sheets that start with 'EF'
    ## TBD -> Change this to a variable
    relevant_sheets = [sheet for sheet in excel_data.sheet_names if sheet.startswith('EF Contribution')]
    
    for sheet in relevant_sheets:
        # Read the sheet into a DataFrame
        df = pd.read_excel(input_excel, sheet_name=sheet)
        
        # Check if 'activity_id' column exists
        if 'activity_id' not in df.columns:
            print(f"Skipping sheet '{sheet}' as it doesn't contain 'activity_id'")
            continue
        
        # Extract the value for the file name
        activity_id = df['activity_id'].iloc[0]  # Assuming the first row contains the name
        
        # Handle cases where 'activity_id' is a tuple or string representation of a tuple
        if isinstance(activity_id, tuple):
            activity_id = activity_id[1]  # Extract second element if it's a tuple
        elif isinstance(activity_id, str) and activity_id.startswith("("):
            try:
                # Safely parse the string into a tuple
                parsed_tuple = ast.literal_eval(activity_id)
                if isinstance(parsed_tuple, tuple) and len(parsed_tuple) > 1:
                    activity_id = parsed_tuple[1]
            except (ValueError, SyntaxError):
                print(f"Unable to parse 'activity_id': {activity_id}")
                continue
        
        # Define the output file path
        output_file = os.path.join(output_folder, f"{activity_id}.csv")
        
        # Save the DataFrame as a CSV
        df.to_csv(output_file, index=False)
        print(f"Saved sheet '{sheet}' as '{output_file}'")




# Creating my databases with suffix
def scenario_db_name(model, pathway, year, suffix):
    return f"EI38_cutoff_{model}_{pathway}_{year}_{suffix}"