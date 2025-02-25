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

from database_setup import find_activity_by_name_product_location


##########################
### LIFECYCLE ANALYSIS ###
##########################

def run_comprehensive_lcia(activity, methods_list):
    """
    Perform a comprehensive LCIA for a given activity across multiple impact categories.
    
    Parameters:
    - activity: The specific activity for which the LCIA is to be performed.
    - methods_list: A list of tuples representing the impact assessment methods.

    Returns:
    - lca_results: A dictionary with methods as keys and their corresponding LCIA scores as values.
    """

    # Define the functional unit (e.g., 1 unit of the activity)
    functional_unit = {activity: 1}

    # Initialize a dictionary to store the results
    lca_results = defaultdict(float)

    # Loop over all impact categories in the method
    for method in methods_list:
        # Run LCI and LCIA
        lca = bc.LCA(functional_unit, method)
        lca.lci()
        lca.lcia()
        
        # Store the result for each category
        lca_results[method] = lca.score

    # Output the results
    for category, score in lca_results.items():
        print(f"{category}: {score}")
    
    return lca_results


def run_comparative_lcia(activities_list, db_name, methods_list, reference_product=None):
## Note that we CAN'T use dictionaries for the list of activities. 
## This is due to how python handles dictionaries - If they have the same key (e.g. Product A production), it keeps only the last entry.
## We'll use tuples, then

    """
    Perform LCIA for a list of activities and return the results.
    
    Parameters:
    - activities_list: A list of tuples where each tuple contains an activity name and a location.
    - db_name: The name of the database.
    - methods_list: A list of tuples representing the impact assessment methods.
    
    Returns:
    - comparative_results: A dictionary with activity names as keys and LCIA results as values.
    """
    comparative_results = {}

    for activity_name, location in activities_list:
        # Find the activity using the existing function
        activity = find_activity_by_name_product_location(db_name, activity_name, reference_product, location)
        
        # Run LCIA for the activity
        lcia_results = run_comprehensive_lcia(activity, methods_list)
        
        # Store the results
        comparative_results[f"{activity_name} ({location})"] = lcia_results
    
    return comparative_results


#########################
### EXCHANGE ANALYSIS ###
#########################

def calculate_exchange_impacts(activity, method):
    """
    Function to calculate and sort the impacts of both technosphere and biosphere exchanges for a given activity.
    It also calculates the percentage contribution of each exchange's impact to the total impact.

    Parameters:
    - activity: The activity for which the impacts of exchanges are calculated.
    - method: The LCIA method used to calculate the impacts.

    Returns:
    - A sorted list of dictionaries containing exchange details, their corresponding impacts, 
      and their percentage contribution to the total impact, in descending order.
    """
    # List to track the impact of each exchange
    exchange_impacts = []
    total_impact = 0  # Track total impact for the activity

    # Step 1: Setup and run the LCA for the entire activity
    lca = bc.LCA({activity: 1}, method)
    lca.lci()
    lca.lcia()

    # Step 2: Iterate over each exchange and calculate the total impact
    for exchange in activity.exchanges():
        try:
            exchange_type = exchange['type']

            if exchange_type == 'biosphere':
                # For biosphere flows, the exchange input is a biosphere flow
                biosphere_flow = exchange.input
                # Get the biosphere flow index in the biosphere dictionary
                bio_flow_index = lca.biosphere_dict[biosphere_flow.key]
                # Get the impact contribution
                total_impact_contribution = lca.characterized_inventory[bio_flow_index, :].sum()
                total_impact += total_impact_contribution  # Add to total impact

                exchange_details = {
                    'exchange_name': biosphere_flow['name'],
                    'exchange_unit': biosphere_flow['unit'],
                    'exchange_location': biosphere_flow.get('location', None),
                    'exchange_id': biosphere_flow.key,    # Add unique ID
                    'impact': total_impact_contribution,
                    'type': exchange_type,
                    'compartment': biosphere_flow['categories']
                }
                exchange_impacts.append(exchange_details)

            elif exchange_type == 'technosphere':
                # For technosphere exchanges, create a new LCA for the exchange
                technosphere_input = exchange.input
                amount = exchange['amount']
                # Create an LCA object for the technosphere input
                technosphere_lca = bc.LCA({technosphere_input: amount}, method)
                technosphere_lca.lci()
                technosphere_lca.lcia()
                # Get the impact
                impact = technosphere_lca.score
                total_impact += impact  # Add to total impact

                exchange_details = {
                    'exchange_name': technosphere_input['name'],
                    'exchange_unit': technosphere_input['unit'],
                    'exchange_location': technosphere_input.get('location', None),
                    'exchange_id': technosphere_input.key,  # Add unique ID
                    'impact': impact,
                    'type': exchange_type,
                    'compartment': None  # Technosphere exchanges don't have compartments
                }
                exchange_impacts.append(exchange_details)

            else:
                # Handle other exchange types if necessary
                pass

        except Exception as e:
            print(f"Failed to compute LCA for exchange {exchange.input['name']} due to {e}")

    # Step 3: Calculate percentage contribution for each exchange
    for exchange_details in exchange_impacts:
        exchange_details['percentage'] = (exchange_details['impact'] / total_impact) * 100 if total_impact > 0 else 0

    # Step 4: Sort and return the impacts to find the highest contributors
    sorted_impacts = sorted(exchange_impacts, key=lambda item: item['impact'], reverse=True)

    return sorted_impacts


def calculate_impacts_for_activities(activities_list, methods_list, database_name, reference_product=None):
    """
    Function to loop through a range of activities and LCIA methods, calculate the impacts of exchanges,
    and return the results.

    Parameters:
    - activities_list: List of tuples where each tuple contains an activity name and its location.
    - methods_list: List of LCIA methods (tuples) used for calculating impacts.
    - database_name: The name of the database containing the activities.
    - reference_product: Optional reference product for filtering activity results.

    Returns:
    - A dictionary containing activity, method, and sorted impacts for each combination.
    """
    results = {}

    # Loop through each activity and its location (tuple)
    for activity_name, location in activities_list:
        try:
            # Find the activity using the find_activity_by_name_product_location function
            activity = find_activity_by_name_product_location(database_name, activity_name, reference_product, location)
            
            # Loop through each method
            for method in methods_list:
                print(f"\n -- Calculating impacts for activity '{activity_name}' in location '{location}' using method '{method}'...")

                # Call the calculate_exchange_impacts function
                try:
                    sorted_impacts = calculate_exchange_impacts(activity, method)
                    
                    # Store results in the dictionary along with the activity object
                    results[(activity_name, location, method)] = {
                        'activity': activity,
                        'impacts': sorted_impacts
                    }

                    # Optional: print the top results
                    print(f"\n ---- Top impacts for activity '{activity_name}' in location '{location}' and method '{method}':")
                    for exchange in sorted_impacts[:5]:  # Show top 5 for brevity
                        print(f"Exchange: {exchange['exchange_name']}, Type: {exchange['type']}, "
                              f"Compartment: {exchange['compartment']}, Impact: {exchange['impact']}")

                except Exception as e:
                    print(f"\n -- Failed to calculate impacts for {activity_name} in location {location} using {method} due to: {e}")
        except ValueError as e:
            print(e)

    return results


def find_most_impactful_exchanges(lca, top_n=2):
    """
    Find the most impactful exchanges (both technosphere and biosphere) from a characterized LCA.
    
    Parameters:
    - lca: A Brightway2 LCA object that has already been run.
    - top_n: Number of top contributors to return.
    
    Returns:
    - A list of tuples containing the top N most impactful exchanges and their contributions.
    """
    # Initialize a list to store contributions
    exchange_contributions = []
    
    # Get the reverse dictionaries for technosphere and biosphere
    rev_techno, rev_prod, rev_bio = lca.reverse_dict()

    # Loop over the non-zero elements of the characterized inventory
    for row, col in zip(*lca.characterized_inventory.nonzero()):
        contribution = lca.characterized_inventory[row, col]
        
        # Check if this is a biosphere or technosphere exchange
        if col in rev_bio:
            # Biosphere flow
            flow = rev_bio[col]
            flow_name = bd.get_activity(flow)["name"]
            exchange_contributions.append((contribution, flow_name, "biosphere"))
        else:
            # Technosphere flow (process contribution)
            process = rev_techno[col]
            process_name = bd.get_activity(process)["name"]
            exchange_contributions.append((contribution, process_name, "technosphere"))

    # Sort contributions by absolute impact (descending)
    exchange_contributions.sort(key=lambda x: abs(x[0]), reverse=True)
    
    return exchange_contributions[:top_n]