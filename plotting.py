import numpy as np
import pandas as pd
import seaborn as sns
import textwrap
import matplotlib.pyplot as plt



def plot_lcia_radar_log(lcia_results, activity_name, reference_product=None, location=None, wrap_width=20):
    """
    Plot LCIA results as a radar chart with logarithmic values using Matplotlib and annotate with actual values
    underneath the impact category labels.
    
    Parameters:
    - lcia_results: A dictionary with impact categories as keys (tuples) and scores as values.
    - activity_name: The name of the activity (for the title).
    - wrap_width: The width (number of characters) at which to wrap the labels.
    """
    # Extract only the second element of each impact category for labels
    categories = [textwrap.fill(key[1], wrap_width) for key in lcia_results.keys()]
    scores = list(lcia_results.values())
    
    # Apply logarithmic transformation
    log_scores = np.log10(scores)
    
    # Number of variables
    N = len(categories)

    # Angle of each axis
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()

    # Complete the loop by repeating the first angle and score (but not the category)
    log_scores = np.concatenate((log_scores, [log_scores[0]]))
    angles += angles[:1]

    # Plot data
    fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(polar=True))
    ax.fill(angles, log_scores, color='blue', alpha=0.25)
    ax.plot(angles, log_scores, color='blue', linewidth=2)

    # Annotate each point with the actual value underneath the labels
    for i, (angle, score, category) in enumerate(zip(angles[:-1], log_scores[:-1], categories)):
        ax.text(angle, score - 0.3, f'{scores[i]:.2e}', horizontalalignment='center', size=10, color='black',
                verticalalignment='top')

    # Labels
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10)

    # Adjust for better layout
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    
    # Add a title
    plt.title(f'LCIA Results for {activity_name} (Log Scale) \n ref:{reference_product} \n  loc:{location}', size=14, color='blue', y=1.1)

    plt.show()


def plot_comparative_radar_log_with_colored_table(comparative_results, methods_list, wrap_width=20, header_wrap_width=15, table_font_size=10):
    """
    Plot comparative LCIA results for multiple activities on a radar chart with logarithmic values,
    and include a table with colored headers (without text) matching the radar plot legend.
    
    Parameters:
    - comparative_results: A dictionary with activity names as keys and LCIA results as values.
    - methods_list: A list of tuples representing the impact assessment methods.
    - wrap_width: The width (number of characters) at which to wrap the impact category labels.
    - header_wrap_width: The width (number of characters) at which to wrap the header (activity names).
    """
    categories = [textwrap.fill(method[1], wrap_width) for method in methods_list]
    N = len(categories)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()

    # Initialize the plot with a larger size
    fig, ax = plt.subplots(figsize=(20, 15), subplot_kw=dict(polar=True))

    colors = []
    
    # Plot data for each activity and collect the colors
    for activity_name, lcia_results in comparative_results.items():
        scores = [lcia_results[method] for method in methods_list]
        log_scores = np.log10(scores)
        log_scores = np.concatenate((log_scores, [log_scores[0]]))
        radar_plot = ax.plot(angles + angles[:1], log_scores, linewidth=2, label=activity_name)
        colors.append(radar_plot[0].get_color())  # Store the color used in the plot

    # Set the category labels
    ax.set_yticklabels([])  # Remove the radial labels
    ax.set_xticks(angles)
    ax.set_xticklabels(categories, fontsize=10)

    # Remove the radial grid labels for a cleaner look
    radial_ticks = [-4, -3, -2, -1, 0]  # Corresponds to 10^-4, 10^-3, 10^-2, 10^-1, 10^0
    ax.set_rgrids(radial_ticks, labels=[], angle=0)

    # Add a legend at the bottom
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=2)

    # Prepare the table data
    wrapped_header = ['Impact Category'] + [textwrap.fill(activity, header_wrap_width) for activity in comparative_results.keys()]
    table_data = []
    
    for i, method in enumerate(methods_list):
        category = method[1]
        row = [textwrap.fill(category, wrap_width)] + [f'{comparative_results[activity].get(method, 0):.2e}' for activity in comparative_results.keys()]
        table_data.append(row)

    # Create the table
    table = plt.table(cellText=table_data,
                      colLabels=wrapped_header,
                      cellLoc='center',
                      loc='right',
                      bbox=[1.3, 0, 0.8, 1])  # Move the table further right

    # Manually set the font size and adjust cell properties
    table.auto_set_font_size(False)
    table.set_fontsize(table_font_size)  # Set the font size of the table
    
    # Color the header cells according to the radar plot colors and remove text
    for i in range(1, len(wrapped_header)):
        cell = table[0, i]
        cell.set_text_props(text='')
        cell.set_facecolor(colors[i-1])
    
    # Adjust the column widths and row heights
    for (i, j), cell in table.get_celld().items():
        if j == 0:  # Widen the impact category column
            cell.set_width(0.3)
        else:
            cell.set_width(0.2)
        
        if i > 0:  # Widen the height of the rows presenting the impact results
            cell.set_height(0.05)  # Adjust this value to make rows taller

    plt.title('Comparative LCIA Results (Log Scale)', size=14, color='blue', y=1.1)
    plt.subplots_adjust(left=0.1, right=0.8, top=0.9, bottom=0.2)  # Adjust layout to give more space for the table

    plt.show()

###############
## SYNTHESIS ##
###############

def plot_activity_impact_changes(activity_name, df):
    """
    Plots VSI to Baseline % Change for all impact categories across SSPs for a given activity.
    """
    df_filtered = df[df["Activity"] == activity_name]

    # Pivot data for grouped bar chart
    df_pivot = df_filtered.pivot(index="Impact Category", columns="SSP", values="VSI to baseline change %")

    df_pivot.plot(kind="bar", figsize=(10, 6), colormap="viridis", edgecolor="black")

    plt.ylabel("VSI to Baseline % Change in 2040")
    plt.title(f"Impact Change Across SSPs and impact catgories for \n {activity_name}")
    plt.axhline(0, color='black', linewidth=1)
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="SSP Scenario")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.show()


###########################
## CONTRIBUTION ANALYSIS ##
###########################

def visualize_contribution_all_activities_with_grid(csv_path):
    # Load data
    df = pd.read_csv(csv_path)
    
    # Convert percentage column to numeric
    df['percentage'] = pd.to_numeric(df['percentage'], errors='coerce')

    # Create a new column to clearly identify biosphere exchanges
    df['sub_activity_label'] = df.apply(
        lambda x: f"{x['sub_activity']} ({x['compartment']})" if x['exchange_type'] == 'biosphere' else x['sub_activity'], 
        axis=1
    )

    # Get unique activities and their names
    unique_activities = df[['activity_id', 'activity_name']].drop_duplicates()

    print(f"Total Activities: {len(unique_activities)}")

    # Loop through each unique activity
    for _, row in unique_activities.iterrows():
        activity_id = row['activity_id']
        activity_name = row['activity_name']

        # Filter data for this activity
        subset = df[df['activity_id'] == activity_id]

        if subset.empty:
            continue

        # Filter to sub-activities contributing at least 1%
        subset = subset[subset['percentage'] >= 1]

        # Pivot data for stacked bar chart
        pivot_df = subset.pivot_table(
            values="percentage", 
            index="impact_indicator", 
            columns="sub_activity_label", 
            aggfunc="sum",
            fill_value=0
        )

        # Define colors: different shades for technosphere and biosphere
        color_map = {
            sub_activity: "tab:blue" if subset[subset["sub_activity_label"] == sub_activity]["exchange_type"].iloc[0] == "technosphere"
            else "tab:red"
            for sub_activity in pivot_df.columns
        }

        # Plot
        ax = pivot_df.plot(kind="bar", stacked=True, figsize=(12, 6), color=[color_map[sub] for sub in pivot_df.columns])

        # Add grid for better readability
        ax.grid(axis="y", linestyle="--", alpha=0.7)  # Dashed grid, slightly transparent

        plt.title(f"Impact Breakdown for {activity_name}")
        plt.xlabel("Impact Indicator")
        plt.ylabel("Percentage Contribution")
        plt.xticks(rotation=45, ha='right')
        plt.legend(title="Sub-Activity (Biosphere includes Compartment)", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()




def visualize_all_activities_with_detailed_biosphere(csv_path, filter=None):
    # Load data
    df = pd.read_csv(csv_path)
    
    # Convert percentage column to numeric
    df['percentage'] = pd.to_numeric(df['percentage'], errors='coerce')

    # Keep a reference of all impact indicators
    all_impact_indicators = df['impact_indicator'].unique()

    # Optional filtering by exchange_type
    if filter in ["biosphere", "technosphere"]:
        df = df[df['exchange_type'] == filter]

    # Create label for sub-activities
    df['sub_activity_label'] = df.apply(
        lambda x: f"{x['sub_activity']} ({x['compartment']})" if x['exchange_type'] == 'biosphere' else x['sub_activity'],
        axis=1
    )

    # Get unique activities
    unique_activities = df[['activity_id', 'activity_name']].drop_duplicates()

    print(f"Total Activities: {len(unique_activities)}")

    # Generate color palette
    unique_labels = df['sub_activity_label'].unique()
    color_palette = dict(zip(unique_labels, sns.color_palette("husl", len(unique_labels))))
    color_palette["Rest"] = "#d3d3d3"  # light gray

    # Loop through activities
    for _, row in unique_activities.iterrows():
        activity_id = row['activity_id']
        activity_name = row['activity_name']

        # Filter for this activity
        subset = df[df['activity_id'] == activity_id]

        if subset.empty:
            continue

        # Only sub-activities with >=1% contribution
        subset = subset[subset['percentage'] >= 1]

        # Pivot table (can be empty for some indicators)
        pivot_df = subset.pivot_table(
            values="percentage",
            index="impact_indicator",
            columns="sub_activity_label",
            aggfunc="sum",
            fill_value=0
        )

        # Ensure all impact indicators are represented
        pivot_df = pivot_df.reindex(all_impact_indicators, fill_value=0)

        # Add 'Rest' to make total 100%
        pivot_df["Rest"] = 100 - pivot_df.sum(axis=1)

        # Generate color list for plot
        color_list = [color_palette.get(col, "#cccccc") for col in pivot_df.columns]

        # Plot
        ax = pivot_df.plot(
            kind="bar",
            stacked=True,
            figsize=(12, 6),
            color=color_list
        )

        # Add grid and labels
        ax.grid(axis="y", linestyle="--", alpha=0.7)
        # title_filter = f" ({filter.capitalize()} only)" if filter else ""
        # If want to include filter, just add it below after {activity_name}, as in {title_filter}
        plt.title(f"Impact Breakdown for {activity_name}")
        plt.xlabel("Impact Indicator")
        plt.ylabel("Percentage Contribution")
        plt.xticks(rotation=45, ha='right')
        plt.legend(title="Sub-Activity", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()