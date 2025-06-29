import mysql.connector

try:
    # Connect to MySQL server
    connection = mysql.connector.connect(
        host='localhost:3306',        # Change to your MySQL server's host
        user='root',    # Replace with your MySQL username
        database='iot-devices' # Replace with the target database name
    )

    # Check if the connection is successful
    if connection.is_connected():
        print("Connected to the database.")

    # Create a cursor object
    cursor = connection.cursor()

    # Define the CREATE TABLE statement
    create_table_query = """
    CREATE TABLE IF NOT EXISTS employees (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        age INT NOT NULL,
        department VARCHAR(100),
        hire_date DATE
    );
    """

    # Execute the CREATE TABLE query
    cursor.execute(create_table_query)
    print("Table `employees` created successfully.")

except mysql.connector.Error as e:
    print(f"Error: {e}")
finally:
    # Close the connection
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("Connection closed.")
