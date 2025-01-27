import time
import subprocess
import re
import logging
import os

# Configure logging
logging.basicConfig(
    filename='website_blocker.log',  # Log file where messages will be saved
    level=logging.INFO,  # Log level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
)

def monitor_traffic():
    logging.info("Started monitoring traffic.")
    while True:  # Continuously monitor traffic
        try:
            output = run_command('nettop')
            list_of_dns = extract_domains(output)
            clean_list = [item.strip() for item in list_of_dns]
            logging.info(f"Extracted {len(clean_list)} DNS entries.")
            
            for dns in clean_list:
                if is_blocked(dns):
                    block_site(dns)
                    time.sleep(180)  # Optional: Throttle after blocking
                else:
                    logging.info(f"Domain {dns} is not blocked.")
            time.sleep(60)  # Wait before the next iteration
        except Exception as e:
            logging.error(f"Error in monitor_traffic: {str(e)}")

def run_command(command):
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)  # Added shell=True
        output, error = process.communicate()

        # Decoding contents
        output = output.decode('utf-8')
        error = error.decode('utf-8')
        
        if error:
            logging.error(f"Error executing command '{command}': {error}")
        
        return output
    except Exception as e:
        logging.error(f"Error in run_command: {str(e)}")
        return ''

def extract_domains(output):
    try:
        pattern_of_domain = r'(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'  # Improved regex
        dns_list = re.findall(pattern_of_domain, output)
        logging.info(f"Found {len(dns_list)} domains in the output.")
        return dns_list
    except Exception as e:
        logging.error(f"Error in extract_domains: {str(e)}")
        return []

def is_blocked(domain):
    try:
        # Create blocklist.txt if it doesn't exist
        if not os.path.exists('blocklist.txt'):
            open('blocklist.txt', 'w').close()

        with open('blocklist.txt', 'r') as f:
            domain_list = f.readlines()
        
        domain_list = [line.strip() for line in domain_list]  # Strip whitespace
        if domain in domain_list:
            logging.info(f"Domain {domain} is blocked.")
            return True
        return False
    except Exception as e:
        logging.error(f"Error in is_blocked: {str(e)}")
        return False

def block_site(domain):
    try:
        # Check if the domain is already blocked
        with open('/etc/hosts', 'r') as host_file:
            if f'127.0.0.1 {domain}' in host_file.read():
                logging.info(f"Domain {domain} is already blocked.")
                return

        # Append the domain to /etc/hosts
        with open('/etc/hosts', 'a') as host_file:
            host_file.write(f'127.0.0.1 {domain}\n')
            logging.info(f"Blocked {domain} by redirecting to 127.0.0.1.")
    except PermissionError:
        logging.error("Permission denied. Please run the script with sudo.")
    except Exception as e:
        logging.error(f"Error blocking {domain}: {str(e)}")

if __name__ == "__main__":
    logging.info("Script started.")
    monitor_traffic()
    logging.info("Script finished.")