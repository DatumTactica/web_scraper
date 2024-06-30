import duckdb, numpy as np, os

def years_to_process(full_path,years,year):
    # Check if there are any processed results
    if not os.path.exists(full_path) or not os.listdir(full_path):
        # When there are not processed results, process all years
        to_process = years
    else:
        duckdb_con = duckdb.connect()
        df = duckdb_con.read_parquet(f'{full_path}/**')
        processed = duckdb_con.execute("SELECT DISTINCT year FROM df").fetchdf()
        # Ensure to reprocess current year
        processed = processed[processed != int(year)]
        # Set the years to process as the difference between what has been pocessed and the expectation
        to_process = np.setdiff1d(years, processed)
    return to_process