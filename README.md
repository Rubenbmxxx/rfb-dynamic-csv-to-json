# Dynamic CSV transformation into JSON
Parse CSV into a JSON file based on CSV column names, making easy to add new JSON properties from a CSV file data source. 


# Starting point

## CSV file
`files/MarketAvrgTicketSample.csv`


## Desired JSON file
`files/MarketAvrgTicketSample.json`


# Process

The aim of this script is to build dynamically a JSON file starting from a CSV file, following the rules below.

Notice there are different column types:

1. Column name where no underscore in it; indicates nesting is opened, so this there is no data for this column at the CSV.
   (i.e. MarketsList)
2. Column name where no underscore in it and there is data int this column at the CSV file; indicates it is a first level 
 property. (i.e. schemaVersion)
3. Column name contains underscore; that identifies from left side the origin and from right side the destiny. In addition,
when a column appears with no data at the CSV file, indicates new nest opening, otherwise finding data in this column indicates
it is a JSON propertie itself. (i.e. MarketsList_Market and Market_isoCod)

