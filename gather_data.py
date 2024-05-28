import pandas as pd

def process_csv(file_path):
    # Load the CSV data into a DataFrame
    df = pd.read_csv(file_path)
    
    # Group by 'Entity Schema Name' and 'Dependent Component Type' and count occurrences
    grouped = df.groupby(['Entity Schema Name', 'Dependent Component Type']).size().unstack(fill_value=0)
    
    # Calculate risks based on the specified criteria
    process_cols = [col for col in grouped.columns if 'Entity Relationship' in col]
    if process_cols:
        grouped['** Entity Relationship Risk'] = grouped[process_cols].sum(axis=1).apply(lambda x: 'High' if x > 17 else 'Low')
    else:
        grouped['** Entity Relationship Risk'] = 'Low'  # Default to 'Low' if no process columns


    # Process Reference Risk: sum any columns that contain 'Process'
    process_cols = [col for col in grouped.columns if 'Process' in col]
    if process_cols:
        grouped['** Process Reference Risk'] = grouped[process_cols].sum(axis=1).apply(lambda x: 'High' if x > 1 else 'Low')
    else:
        grouped['** Process Reference Risk'] = 'Low'  # Default to 'Low' if no process columns

    # App Reference Risk: Check for 'Model-driven App' and 'Canvas App'
    app_cols = [col for col in grouped.columns if col in ['Model-driven App', 'Canvas App']]
    if app_cols:
        grouped['** App Reference Risk'] = grouped[app_cols].sum(axis=1).apply(lambda x: 'High' if x > 0 else 'Low')
    else:
        grouped['** App Reference Risk'] = 'Low'  # Default to 'Low' if no app columns

    # Other's Reference Risk: sum 'Forms', 'Sitemap', 'Views'
    others_cols = [col for col in grouped.columns if col in ['Forms', 'Sitemap', 'Views']]
    if others_cols:
        grouped['** Other\'s Reference Risk'] = grouped[others_cols].sum(axis=1).apply(lambda x: 'High' if x > 1 else 'Low')
    else:
        grouped['** Other\'s Reference Risk'] = 'Low'  # Default to 'Low' if no other specified types

    # Reset the index to turn multi-level index into columns
    results = grouped.reset_index()
    
    # Optionally, save the results to a new CSV file
    results.to_csv('output_risk_summary.csv', index=False)
    
    return results

# Example usage
file_path = 'source_dependency.csv'  # Replace this with the path to your actual CSV file
summary = process_csv(file_path)
print(summary)
