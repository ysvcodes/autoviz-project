\
# app/tests/test_data_handler.py
# Author: Atirola Adesanya
# Purpose: Unit tests for the data_handler module.

import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from app.data_handler import load_and_process_data, get_summary_statistics
import os

# Helper to create a dummy CSV for testing - ensuring it's created within the test's temp directory
def create_dummy_csv(filepath, data_rows, columns="ID,Date,Category,Value"):
    # filepath is now a Path object from tmp_path
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(columns + '\\n') # Write header
        for row in data_rows:
            f.write(row + '\\n')

@pytest.fixture
def valid_csv_file(tmp_path):
    """ Fixture to create a temporary valid CSV file for tests """
    file_path = tmp_path / "valid_data.csv"
    data = [
        "1,2023-01-01,A,100",
        "2,2023-01-02,B,150.5", # Added float value
        "3,2023-01-03,A,120",
        "4,2023-01-04,C,200"  # Added more data
    ]
    create_dummy_csv(file_path, data)
    return str(file_path)

@pytest.fixture
def csv_with_numeric_conversion_needed(tmp_path):
    """ Fixture for CSV where 'Value' might be string and needs conversion """
    file_path = tmp_path / "numeric_conversion.csv"
    data = [
        "1,2023-01-01,A,100",
        "2,2023-01-02,B,'150'", # Value as string
        "3,2023-01-03,A,120.0"
    ]
    create_dummy_csv(file_path, data)
    return str(file_path)

@pytest.fixture
def empty_data_csv_file(tmp_path):
    """ Fixture to create a CSV file with only headers (no data rows) """
    file_path = tmp_path / "empty_data.csv"
    create_dummy_csv(file_path, []) # Pass empty list for data_rows
    return str(file_path)

@pytest.fixture
def malformed_row_csv_file(tmp_path):
    """ Fixture to create a CSV file with a row having incorrect number of columns """
    file_path = tmp_path / "malformed_row_data.csv"
    data = [
        "1,2023-01-01,A,100",
        "2,2023-01-02,B", # Missing a value, pandas might fill with NaN or error depending on read_csv params
        "3,2023-01-03,A,120,ExtraValue" # Extra value
    ]
    create_dummy_csv(file_path, data)
    return str(file_path)

@pytest.fixture
def csv_with_missing_value_column(tmp_path):
    """ Fixture for CSV missing the 'Value' column needed for stats """
    file_path = tmp_path / "missing_value_col.csv"
    data = [
        "1,2023-01-01,A",
        "2,2023-01-02,B"
    ]
    create_dummy_csv(file_path, data, columns="ID,Date,Category") # Custom columns
    return str(file_path)

# --- Tests for load_and_process_data ---

def test_load_and_process_data_success(valid_csv_file):
    """ Test loading a valid CSV file successfully """
    df = load_and_process_data(valid_csv_file)
    assert df is not None, "DataFrame should not be None for a valid CSV"
    assert not df.empty, "DataFrame should not be empty for a valid CSV"
    assert len(df) == 4, "DataFrame should contain 4 rows of data"
    expected_columns = ["ID", "Date", "Category", "Value"]
    assert list(df.columns) == expected_columns, f"DataFrame columns should be {expected_columns}"
    # Assuming your load_and_process_data converts 'Value' to numeric if it isn't already
    # and 'Date' to datetime. If not, these tests might need adjustment or the function updated.
    # For this example, let's assume 'Value' is numeric.
    # If 'Value' can be string and converted by get_summary_statistics, test that there.
    # Check dtypes if specific conversions are expected in load_and_process_data
    # Example: assert pd.api.types.is_numeric_dtype(df['Value'])
    # Example: assert pd.api.types.is_datetime64_any_dtype(df['Date'])


def test_load_and_process_data_file_not_found():
    """ Test loading a non-existent CSV file """
    df = load_and_process_data("this_file_does_not_exist.csv")
    assert df is None, "DataFrame should be None for a non-existent file"

def test_load_and_process_data_empty_data_file(empty_data_csv_file):
    """ Test loading a CSV file that contains only headers and no data rows """
    df = load_and_process_data(empty_data_csv_file)
    # Behavior for empty data: load_and_process_data returns None if df.empty
    assert df is None, "DataFrame should be None for an empty data file as per current logic"
    # If you change load_and_process_data to return an empty df, this assertion would change:
    # assert df is not None
    # assert df.empty

# Parametrizing for different "bad" file scenarios could be useful if handling is distinct
# For now, the generic exception in load_and_process_data covers many pd.errors

# --- Tests for get_summary_statistics ---

@pytest.fixture
def sample_df_for_stats():
    """ Creates a sample DataFrame for testing get_summary_statistics """
    data = {
        'ID': [1, 2, 3, 4, 5],
        'Date': pd.to_datetime(['2023-01-01', '2023-01-01', '2023-01-02', '2023-01-03', '2023-01-03']),
        'Category': ['A', 'B', 'A', 'C', 'B'],
        'Value': [10.0, 20.0, 15.0, 25.0, 20.0] # Ensure 'Value' is numeric for stats
    }
    return pd.DataFrame(data)

def test_get_summary_statistics_valid_df(sample_df_for_stats):
    """ Test summary statistics with a valid, typical DataFrame """
    stats = get_summary_statistics(sample_df_for_stats)
    assert stats is not None, "Statistics dictionary should not be None"
    assert "error" not in stats, "Should not contain an error message for valid df"
    assert stats["total_records"] == 5
    assert stats["average_value"] == pytest.approx(18.0) # (10+20+15+25+20)/5 = 90/5 = 18
    assert stats["categories"] == 3 # A, B, C

def test_get_summary_statistics_df_with_nan_values(tmp_path):
    """ Test stats with a DataFrame containing NaN in the 'Value' column """
    # NaN values in 'Value' should typically be excluded from mean calculation by pandas
    file_path = tmp_path / "nan_value_data.csv"
    data_rows = [
        "1,2023-01-01,A,100",
        "2,2023-01-02,B,",       # Value will be NaN
        "3,2023-01-03,A,120"
    ]
    create_dummy_csv(file_path, data_rows)
    df = load_and_process_data(file_path) # Assuming this loads and Value becomes numeric (or NaN)
    # Manually convert 'Value' to numeric if load_and_process_data doesn't already
    if df is not None and 'Value' in df.columns:
        df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
    
    stats = get_summary_statistics(df)
    assert "error" not in stats
    assert stats["total_records"] == 3 # All rows are counted
    assert stats["average_value"] == pytest.approx(110.0) # (100+120)/2

def test_get_summary_statistics_empty_df():
    """ Test summary statistics with a completely empty DataFrame """
    df_empty = pd.DataFrame()
    stats = get_summary_statistics(df_empty)
    assert stats == {}, "Statistics should be an empty dict for an empty DataFrame"

def test_get_summary_statistics_none_df():
    """ Test summary statistics when None is passed as DataFrame """
    stats = get_summary_statistics(None)
    assert stats == {}, "Statistics should be an empty dict for a None DataFrame"

def test_get_summary_statistics_missing_required_columns(sample_df_for_stats):
    """ Test stats when 'Value' or 'Category' column is missing """
    df_missing_value = sample_df_for_stats.drop(columns=['Value'])
    stats_no_value = get_summary_statistics(df_missing_value)
    assert "error" in stats_no_value, "Should return an error if 'Value' column is missing"
    assert stats_no_value["error"] == "Required columns not found"

    df_missing_category = sample_df_for_stats.drop(columns=['Category'])
    stats_no_category = get_summary_statistics(df_missing_category)
    assert "error" in stats_no_category, "Should return an error if 'Category' column is missing"
    assert stats_no_category["error"] == "Required columns not found"

@pytest.mark.parametrize(
    "data, expected_avg, expected_cats, description",
    [
        ( # All same category
            {'Category': ['A', 'A', 'A'], 'Value': [10, 20, 30]},
            20.0, 1, "All same category"
        ),
        ( # Single record
            {'Category': ['X'], 'Value': [50]},
            50.0, 1, "Single record"
        ),
        ( # Values are zero
            {'Category': ['A', 'B'], 'Value': [0, 0]},
            0.0, 2, "Values are zero"
        )
    ]
)
def test_get_summary_statistics_various_scenarios(data, expected_avg, expected_cats, description):
    """ Test get_summary_statistics with various data scenarios using parametrization """
    # Add other necessary columns if your function depends on them (ID, Date)
    # For simplicity, assuming get_summary_statistics only needs Category and Value for these checks
    df = pd.DataFrame(data)
    # Ensure 'Value' is numeric
    df['Value'] = pd.to_numeric(df['Value'])

    stats = get_summary_statistics(df)
    
    assert "error" not in stats, f"Test failed for: {description}"
    assert stats["total_records"] == len(df), f"Total records mismatch for: {description}"
    assert stats["average_value"] == pytest.approx(expected_avg), f"Average value mismatch for: {description}"
    assert stats["categories"] == expected_cats, f"Category count mismatch for: {description}"
