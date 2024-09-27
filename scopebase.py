import mysql.connector
from tabulate import tabulate
import getpass

__version__ = "0.3.1"

def execute_query(cursor, query):
    cursor.execute(query)
    result = cursor.fetchall()
    columns = [i[0] for i in cursor.description]
    return result, columns

def display_table(result, columns, query_name):
    print(f"\nResults for {query_name}:")
    print(tabulate(result, headers=columns, tablefmt="fancy_grid"))

def query_samples(cursor):
    query = """
    SELECT `sample`.`id` AS `Sample-ID`, `sample`.`date` AS `Date`, `location`.`name` AS `Location`, 
           `sample-type`.`name` AS `Type`, `fixation`.`name` AS `Fixation`, `preservative`.`name` AS `Preservative`, 
           `sample`.`latitude` AS `Latitude`, `sample`.`longitude` AS `Longitude`, `sample`.`T` AS `T`, 
           `sample`.`pH` AS `pH`, `sample`.`EC` AS `EC`, `sample`.`nitrate` AS `NO3`, `sample`.`note` AS `Note`
    FROM `scopebase`.`sample` `sample`
    LEFT OUTER JOIN `scopebase`.`sample-type` `sample-type` ON `sample`.`sample-type_id` = `sample-type`.`id`
    LEFT OUTER JOIN `scopebase`.`fixation` `fixation` ON `sample`.`fixation_id` = `fixation`.`id`
    LEFT OUTER JOIN `scopebase`.`location` `location` ON `sample`.`location_id` = `location`.`id`
    LEFT OUTER JOIN `scopebase`.`preservative` `preservative` ON `sample`.`preservative_id` = `preservative`.`id`
    ORDER BY `Sample-ID` DESC;
    """
    return execute_query(cursor, query)

def query_slides(cursor):
    query = """
    SELECT `slide`.`id` AS `Slide-ID`, `sample`.`id` AS `Sample-ID`, 
           `sample-type`.`name` AS `Sample-Type`, `fixation`.`name` AS `Fixation`, 
           `preservative`.`name` AS `Preservative`, `protocol`.`name` AS `Protocol`, 
           `mounting-medium`.`name` AS `Mounting-Medium`, `slide`.`date` AS `Slide-Date`, 
           `sample`.`date` AS `Sample-Date`, `location`.`name` AS `Location`, 
           `sample`.`latitude` AS `Sample-Latitude`, `sample`.`longitude` AS `Sample-Longitude`
    FROM `scopebase`.`sample` `sample`
    LEFT OUTER JOIN `scopebase`.`sample-type` `sample-type` ON `sample`.`sample-type_id` = `sample-type`.`id`
    RIGHT OUTER JOIN `scopebase`.`slide` `slide` ON `sample`.`id` = `slide`.`sample_id`
    RIGHT OUTER JOIN `scopebase`.`protocol` `protocol` ON `slide`.`protocol_id` = `protocol`.`id`
    RIGHT OUTER JOIN `scopebase`.`mounting-medium` `mounting-medium` ON `slide`.`mounting-medium_id` = `mounting-medium`.`id`
    LEFT OUTER JOIN `scopebase`.`preservative` `preservative` ON `sample`.`preservative_id` = `preservative`.`id`
    LEFT OUTER JOIN `scopebase`.`fixation` `fixation` ON `sample`.`fixation_id` = `fixation`.`id`
    LEFT OUTER JOIN `scopebase`.`location` `location` ON `sample`.`location_id` = `location`.`id`
    ORDER BY `Slide-ID` DESC;
    """
    return execute_query(cursor, query)

def main():
    # Connect to the database
    password = getpass.getpass("Enter the password for the database: ")
    connection = mysql.connector.connect(
        host="scopebase.fritz.box",
        user="sr",
        password=password,
        database="scopebase"
    )

    cursor = connection.cursor()

    # Query and display sample data
    sample_result, sample_columns = query_samples(cursor)
    display_table(sample_result, sample_columns, "Sample Data")

    # Query and display slide data
    slide_result, slide_columns = query_slides(cursor)
    display_table(slide_result, slide_columns, "Slide Data")

    cursor.close()
    connection.close()
    
    # Wait for user input to keep the terminal open
    input("\nPress Enter to exit...")
if __name__ == "__main__":
    main()
