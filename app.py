import psutil
import time
import random
import mysql.connector

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': 'root',  # Replace with your MySQL password
    'database': 'cinema_booking_system'
}

def memory_stress_test():
    """Perform memory stress test and return result."""
    memory_stress_size = 100 * (1024 ** 2) // 8  # Allocate 100 MB (using float, each takes 8 bytes)
    stress_data = [random.random() for _ in range(memory_stress_size)]  # Allocate memory
    time.sleep(2)  # Allow time for allocation
    memory_usage = psutil.virtual_memory().percent
    return {
        "resource": "Memory",
        "usage": memory_usage
    }

def disk_stress_test():
    """Perform disk stress test and return result."""
    file_size = 100 * (1024 ** 2)  # 100 MB
    with open('stress_test_file.bin', 'wb') as f:
        f.write(random.randbytes(file_size))  # Write random bytes to file
    time.sleep(2)  # Allow time for writing
    disk_usage = psutil.disk_usage('/').percent
    return {
        "resource": "Disk",
        "usage": disk_usage
    }

def network_stress_test():
    """Perform network stress test and return usage."""
    for _ in range(10):  # Adjust number of requests
        random_data = random.randbytes(5 * 1024 * 1024)  # 5 MB of data
        time.sleep(0.5)  # Simulate delay
    net_io = psutil.net_io_counters()
    total_usage = net_io.bytes_sent + net_io.bytes_recv
    max_bandwidth = 100 * (1024 ** 2)  # Assuming 100 MB max for calculation
    usage_percentage = (total_usage / max_bandwidth) * 100 if total_usage < max_bandwidth else 100
    return {
        "resource": "Network",
        "usage": usage_percentage
    }

def cpu_stress_test():
    """Perform CPU stress test and return result."""
    start_time = time.time()
    while time.time() - start_time < 10:  # Run for 10 seconds
        _ = [x * x for x in range(10000)]
    cpu_usage = psutil.cpu_percent(interval=1)
    return {
        "resource": "CPU",
        "usage": cpu_usage
    }

def mysql_stress_test():
    """Perform SQL stress test and return results along with MySQL resource usage."""
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
            return {"error": "MySQL process not found."}

        # Run the specified query in a loop to simulate stress
        query = """
            SELECT b.customer_id, COUNT(r.id)
            FROM bookings b
            JOIN reserved_seat r ON b.id = r.booking_id
            JOIN screenings s ON b.screening_id = s.id
            WHERE s.start_time BETWEEN '2017-10-01 00:00:00' AND '2017-11-01 00:00:00'
            GROUP BY b.customer_id
            ORDER BY b.customer_id;
        """
        
        # Run query multiple times to simulate load
        for _ in range(50):  # Adjust for desired load
            cursor.execute(query)
            cursor.fetchall()  # Fetch results to complete query execution

        # Capture MySQL resource usage after queries
        mysql_cpu = mysql_process.cpu_percent(interval=1)  # Sample over 1 second
        mysql_memory = mysql_process.memory_percent()

        cursor.close()
        connection.close()

        return {
            "resource": "MySQL",
            "cpu_usage": mysql_cpu,
            "memory_usage": mysql_memory
        }
    except mysql.connector.Error as e:
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
            print("Invalid choice.")
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
