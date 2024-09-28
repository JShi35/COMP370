import pandas as pd
import argparse

# Define the column names based on the data structure
column_names = [
    'UniqueKey', 'CreatedDate', 'ClosedDate', 'Agency', 'AgencyName', 'ComplaintType', 
    'Descriptor', 'LocationType', 'IncidentZip', 'IncidentAddress', 'StreetName', 
    'CrossStreet1', 'CrossStreet2', 'IntersectionStreet1', 'IntersectionStreet2', 
    'AddressType', 'City', 'Landmark', 'FacilityType', 'Status', 'DueDate', 
    'ResolutionDescription', 'ResolutionActionUpdatedDate', 'CommunityBoard', 
    'Borough', 'XCoordinateStatePlane', 'YCoordinateStatePlane', 'ParkFacilityName', 
    'ParkBorough', 'SchoolName', 'SchoolNumber', 'SchoolRegion', 'SchoolCode', 
    'SchoolPhoneNumber', 'SchoolAddress', 'SchoolCity', 'SchoolState', 'SchoolZip', 
    'SchoolNotFound', 'Latitude', 'Longitude', 'Location'
]

# Function to filter and count complaints by borough and complaint type
def filter_complaints(input_file, start_date, end_date):
    # Load CSV, specifying column names since the CSV doesn't have headers
    df = pd.read_csv(input_file, names=column_names, low_memory=False)

    # Convert the 'CreatedDate' column to datetime
    df['CreatedDate'] = pd.to_datetime(df['CreatedDate'], errors='coerce')

    # Filter based on the date range
    mask = (df['CreatedDate'] >= start_date) & (df['CreatedDate'] <= end_date)
    filtered_df = df[mask]

    # Group by complaint type and borough, then count
    result = filtered_df.groupby(['ComplaintType', 'Borough']).size().reset_index(name='count')
    return result

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Process complaints by borough and date.')
    parser.add_argument('-i', '--input', required=True, help='Input CSV file')
    parser.add_argument('-s', '--start_date', required=True, help='Start date in YYYY-MM-DD format')
    parser.add_argument('-e', '--end_date', required=True, help='End date in YYYY-MM-DD format')
    parser.add_argument('-o', '--output', help='Output file (optional)')

    # Parse arguments
    args = parser.parse_args()

    # Convert start and end date to datetime
    start_date = pd.to_datetime(args.start_date)
    end_date = pd.to_datetime(args.end_date)

    # Filter and get the result
    result = filter_complaints(args.input, start_date, end_date)

    # Output result
    if args.output:
        result.to_csv(args.output, index=False)
        print(f"Results saved to {args.output}")
    else:
        print(result.to_csv(index=False))

if __name__ == '__main__':
    main()
