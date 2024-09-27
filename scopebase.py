import mysql.connector
from tabulate import tabulate
import getpass  # For securely prompting the password

# Version of the application
__version__ = "0.1.1"

# Function to connect to the database
def connect_to_db():
    try:
        # Prompting the user to input the password securely
        password = getpass.getpass("Enter the database password: ")
        
        conn = mysql.connector.connect(
            host="scopebase.fritz.box",  # Your database server host
            user="sr",                  # Your username
            password=password,           # User-entered password
            database="scopebase"         # Your database name
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Function to execute the slide query and return the result
def execute_query(conn):
    query = """
    SELECT 
        `slide`.`id` AS `Slide-ID`, 
        `sample`.`id` AS `Sample-ID`, 
        `sample-type`.`name` AS `Sample-Type`, 
        `fixation`.`name` AS `Fixation`, 
        `preservative`.`name` AS `Preservative`, 
        `protocol`.`name` AS `Protocol`, 
        `mounting-medium`.`name` AS `Mounting-Medium`, 
        `slide`.`date` AS `Slide-Date`, 
        `sample`.`date` AS `Sample-Date`, 
        `location`.`name` AS `Location`, 
        `sample`.`latitude` AS `Sample-Latitude`, 
        `sample`.`longitude` AS `Sample-Longitude`
    FROM 
        `scopebase`.`sample` AS `sample`
    INNER JOIN 
        `scopebase`.`sample-type` AS `sample-type` 
        ON `sample`.`sample-type_id` = `sample-type`.`id`
    INNER JOIN  
        `scopebase`.`slide` AS `slide` 
        ON `sample`.`id` = `slide`.`sample_id`
    INNER JOIN  
        `scopebase`.`protocol` AS `protocol` 
        ON `slide`.`protocol_id` = `protocol`.`id`
    INNER JOIN  
        `scopebase`.`mounting-medium` AS `mounting-medium` 
        ON `slide`.`mounting-medium_id` = `mounting-medium`.`id`
    INNER JOIN  
        `scopebase`.`preservative` AS `preservative` 
        ON `sample`.`preservative_id` = `preservative`.`id`
    INNER JOIN  
        `scopebase`.`fixation` AS `fixation` 
        ON `sample`.`fixation_id` = `fixation`.`id`
    INNER JOIN 
        `scopebase`.`location` AS `location` 
        ON `sample`.`location_id` = `location`.`id`
    ORDER BY 
        `Slide-ID` DESC;
    """
    
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    columns = [i[0] for i in cursor.description]
    cursor.close()
    return result, columns

# Main function
def main():
    # Display version info
    print(f"ScopeBase Frontend, version {__version__}")
    
    # Connect to the database
    conn = connect_to_db()
    if not conn:
        return

    # Execute query and display the result
    slides_result, slides_columns = execute_query(conn)

    # Display results in a table format
    print("\nSlides Information:")
    print(tabulate(slides_result, headers=slides_columns, tablefmt="grid"))

    # Pause the application to allow the user to view the data
    input("\nPress Enter to exit...")

    # Close the connection
    conn.close()

if __name__ == "__main__":
    main()
