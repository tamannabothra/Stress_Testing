import psutil
import time
import random
import mysql.connector
import logging

# Configure logging
logging.basicConfig(
    filename='stress_test.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': 'root',  # Replace with your MySQL password
    'database': 'cinema_booking_system'
}

def memory_stress_test():
    """Perform memory stress test and return result."""
    logging.info("Starting memory stress test.")
    memory_stress_size = 100 * (1024 ** 2) // 8  # Allocate 100 MB (using float, each takes 8 bytes)
    stress_data = [random.random() for _ in range(memory_stress_size)]  # Allocate memory
    time.sleep(0.5)  # Allow time for allocation
    memory_usage = psutil.virtual_memory().percent
    logging.info("Memory stress test completed. Usage: %s%%", memory_usage)
    return {
        "resource": "Memory",
        "usage": memory_usage
    }

def disk_stress_test():
    """Perform disk stress test and return result."""
    logging.info("Starting disk stress test.")
    file_size = 1000 * (1024 ** 2)  # 100 MB
    chunk_size = 1024 * 1024  # 1 MB
    with open('stress_test_file.bin', 'wb') as f:
        for _ in range(file_size // chunk_size):
            f.write(random.randbytes(chunk_size))  # Write 1 MB chunks
    time.sleep(0.5)  # Allow time for writing
    disk_usage = psutil.disk_usage('/').percent
    logging.info("Disk stress test completed. Usage: %s%%", disk_usage)
    return {
        "resource": "Disk",
        "usage": disk_usage
    }

def network_stress_test():
    """Perform network stress test and return usage."""
    logging.info("Starting network stress test.")
    for _ in range(10):  # Adjust number of requests
        random_data = random.randbytes(5 * 1024 * 1024)  # 5 MB of data
        time.sleep(5)  # Simulate delay
    net_io = psutil.net_io_counters()
    total_usage = net_io.bytes_sent + net_io.bytes_recv
    max_bandwidth = 100 * (1024 ** 2)  # Assuming 100 MB max for calculation
    usage_percentage = (total_usage / max_bandwidth) * 100 if total_usage < max_bandwidth else 100
    logging.info("Network stress test completed. Usage: %s%%", usage_percentage)
    return {
        "resource": "Network",
        "usage": usage_percentage
    }

def cpu_stress_test():
    """Perform CPU stress test and return result."""
    logging.info("Starting CPU stress test.")
    start_time = time.time()
    while time.time() - start_time < 30:  # Run for 30 seconds
        _ = [x * x for x in range(1000000)]
    cpu_usage = psutil.cpu_percent(interval=1)
    logging.info("CPU stress test completed. Usage: %s%%", cpu_usage)
    return {
        "resource": "CPU",
        "usage": cpu_usage
    }

def mysql_stress_test():
    """Perform SQL stress test and return results along with MySQL resource usage."""
    logging.info("Starting MySQL stress test.")
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Find MySQL process for usage monitoring
        mysql_process = None
        for process in psutil.process_iter(['name']):
            if process.info['name'] == 'mysqld':
                mysql_process = process
                break

        if not mysql_process:
            logging.error("MySQL process not found.")
            return {"error": "MySQL process not found."}

        # Run the specified query in a loop to simulate stress
        query = """
            SELECT *
            FROM
            bookings b
            JOIN
            reserved_seat r ON b.id = r.booking_id
            ORDER BY b.id
            LIMIT 500;
        """

        # Run query multiple times to simulate load
        for _ in range(5000):  # Adjust for desired load
            cursor.execute(query)
            cursor.fetchall()  # Fetch results to complete query execution

        # Capture MySQL resource usage after queries
        mysql_cpu = mysql_process.cpu_percent(interval=1)  # Sample over 1 second
        mysql_memory = mysql_process.memory_percent()

        cursor.close()
        connection.close()

        logging.info("MySQL stress test completed. CPU Usage: %s%%, Memory Usage: %s%%", mysql_cpu, mysql_memory)
        return {
            "resource": "MySQL",
            "cpu_usage": mysql_cpu,
            "memory_usage": mysql_memory
        }
    except mysql.connector.Error as e:
        logging.error("MySQL error: %s", str(e))
        return {"error": str(e)}

def main():
    while True:
        print("\nSelect a stress test to run:")
        print("1. Memory Stress Test")
        print("2. Disk Stress Test")
        print("3. Network Stress Test")
        print("4. CPU Stress Test")
        print("5. MySQL Stress Test")
        print("6. Exit")

        choice = input("Enter the number of your choice: ")

        if choice == '1':
            result = memory_stress_test()
        elif choice == '2':
            result = disk_stress_test()
        elif choice == '3':
            result = network_stress_test()
        elif choice == '4':
            result = cpu_stress_test()
        elif choice == '5':
            result = mysql_stress_test()
        elif choice == '6':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice, Please Try again!!!!!!!!!!")
            continue

        # Display the result
        if "error" in result:
            print(f"Error: {result['error']}")
        elif result["resource"] == "MySQL":
            print(f"MySQL CPU Usage: {result['cpu_usage']}%")
            print(f"MySQL Memory Usage: {result['memory_usage']}%")
        else:
            print(f"{result['resource']} Usage: {result['usage']}%")

if __name__ == "__main__":
    main()
