import sqlite3
import csv

# Connect to the SQLite database
conn = sqlite3.connect('database.sqlite')
cursor = conn.cursor()

csv_files_list = ['combined_active_program_codes', 'combined_award_program_codes', 'maternal_ehb_grantees', 'maternal_ehb_2023', 'maternal_ehb_active', 'maternal_ehb_awarded', 'wic_states', 'wic_totals']

for csv_file in csv_files_list:
  csv_file_path = f'data/output/{csv_file}.csv'
  table_name = csv_file

  # Open and read the CSV file
  with open(csv_file_path, 'r', encoding= "utf-8") as csv_file:
      csv_reader = csv.reader(csv_file)
      # Skip the header row if it exists
      next(csv_reader, None)
      
      # Read the data from the CSV file
      data = [row for row in csv_reader]

  # Get the column names from the existing table
  cursor.execute(f"PRAGMA table_info({table_name})")
  columns = [column[1] for column in cursor.fetchall()]

  # Prepare the INSERT statement
  placeholders = ','.join(['?' for _ in columns])
  column_names = ','.join(columns)
  insert_query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"

  # Insert the data into the existing table
  cursor.executemany(insert_query, data)
  conn.commit()
  print(f"Data imported successfully into {table_name}!")

# Close the connection
conn.close()