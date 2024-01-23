import json
import pandas as pd
from datetime import datetime


def parse_csv_to_json(columns):
    json_schema = {}

    # Iterate CSV columns identifying "_" and prefix/suffix
    for column in columns:
        parts = column.split('_')
        if len(parts) == 1:
            json_schema[column] = []
            prefix = parts[0] + '_'
        else:
            prefix = parts[1] + '_'

        # Loop again over columns using previously identified CSV column name to create new property or assign child
        # property if exists
        for nest in columns:
            if nest.startswith(prefix):
                if column not in json_schema.keys():
                    json_schema[column] = []  # new level
                json_schema[column].append(nest)  # Nested level

    return json_schema


def csv_to_json(pdf_csv, json_schema, grouped_df=None):
    json_formatted = []
    levels = None
    if not levels:
        levels = [x for x in json_schema.keys() if len(x.split("_")) == 1]
        grouped_df = pdf_csv.groupby(by=levels, dropna=False)
    elif not grouped_df:
        grouped_df = pdf_csv.groupby(by=levels, dropna=False)

    for values, schema in grouped_df:
        json_data = {}

        for i, key in enumerate(levels):
            if not json_schema[key]:  # json_schema[key] is None does not work
                json_data[key] = values[i]
            elif key.endswith("List"):
                json_data[key] = []
                slc_cols, grp_cols = extract_group_columns(json_schema=json_schema, nested_levels=json_schema[key])
                sub_data = schema[slc_cols]
                # subloop = 1
                grp_sub_data = sub_data.groupby([col for col in slc_cols if col not in grp_cols])
                for sub_values, sub_schema in grp_sub_data:
                    gen_json = set_data(json_schema, key, sub_values, sub_schema)
                    json_data[key].append(gen_json)
            else:
                json_data[key] = {}
                for attr in json_schema[key]:
                    json_data[key][attr] = schema[attr].values[0]
        json_formatted.append(json_data)
    return json_formatted


def set_data(json_schema, key, sub_values, sub_schema):
    result = {}
    for sub_level in json_schema[key]:
        for i, key in enumerate(json_schema[sub_level]):
            result[key] = sub_values[i]
    return result


def extract_group_columns(json_schema, nested_levels):
    slc_columns = []
    grp_columns = []

    for level in nested_levels:
        if level in json_schema:
            sub_level = json_schema[level]
            slc, grp = extract_group_columns(json_schema, sub_level)
            grp_columns.extend(grp)
            slc_columns.extend(slc)
        else:
            if level.split("_")[0].endswith("List"):
                grp_columns.append(level)
            slc_columns.append(level)
    return slc_columns, grp_columns


if __name__ == '__main__':
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Working directories related to current project structure:
    csv_file = 'files/MarketAvrgTicketSample.csv'
    json_file_path = f'files/output_{timestamp}.json'

    # Read CSV file
    raw_df = pd.read_csv(csv_file, sep=";")
    csv_columns = list(raw_df.columns)

    # Parse CSV file into JSON dict:
    parsed_json_dict = parse_csv_to_json(csv_columns)

    # Run transformation:
    csv_to_json(pdf_csv=raw_df, json_schema=parsed_json_dict)
