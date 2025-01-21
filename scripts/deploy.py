#!/usr/bin/env python3

import socket
import subprocess
import os
import secrets

repo_paths = {}

def get_ip_address():
    try:
        # Create a temporary socket to connect to an external server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # We don't actually need to send data
        s.connect(("8.8.8.8", 80))
        # Get the local IP address used for this connection
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        return f"Could not get IP address: {str(e)}"

def clone_services():
    services_dir = "services"
    
    # Create services directory if it doesn't exist
    if not os.path.exists(services_dir):
        os.makedirs(services_dir)
        print(f"Created {services_dir} directory")
    
    repos = [
        "https://github.com/Masters-Degree-Project/comment-service",
        # "https://github.com/Masters-Degree-Project/task-service",
        "https://github.com/Masters-Degree-Project/project-service",
        "https://github.com/Masters-Degree-Project/user-service"
    ]
    
    for repo in repos:
        repo_name = repo.split('/')[-1]
        repo_path = os.path.join(services_dir, repo_name)
        print(f"\nCloning {repo_name}...")

        repo_paths[repo_name] = repo_path
        
        if os.path.exists(repo_path):
            print(f"{repo_name} directory already exists, pulling latest changes...")
            try:
                subprocess.run(['git', '-C', repo_path, 'pull'], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error pulling {repo_name}: {str(e)}")
        else:
            try:
                subprocess.run(['git', 'clone', repo, repo_path], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error cloning {repo_name}: {str(e)}")

def generate_jwt_secret():
    return secrets.token_hex(32)

def service_env_setup(ip_address, repo_name, repo_path, service_index):
    print(f"\nSetting up environment for {repo_name}...")
    
    env_example_path = os.path.join(repo_path, '.env.example')
    env_dist_path = os.path.join(repo_path, '.env.dist')
    env_path = os.path.join(repo_path, '.env')
    
    # Check for .env.example or .env.dist
    if os.path.exists(env_example_path):
        template_path = env_example_path
    elif os.path.exists(env_dist_path):
        template_path = env_dist_path
    else:
        print(f"No .env.example or .env.dist file found in {repo_name}")
        return
        
    try:
        with open(template_path, 'r') as template_file:
            env_content = template_file.read()
            
        # Common JWT secret for all services
        jwt_secret = generate_jwt_secret()
        
        # Calculate service port (8081 + index)
        service_port = 8081 + service_index
            
        # Parse and fill environment variables
        filled_content = []
        for line in env_content.splitlines():
            if line.strip() and not line.startswith('#'):
                key, *value_parts = line.split('=')
                value = '='.join(value_parts) if value_parts else ''
                
                # Map specific environment variables
                if key == 'API_GATEWAY_HOST':
                    filled_content.append(f"{key}={ip_address}")
                elif key == 'API_GATEWAY_PORT':
                    filled_content.append(f"{key}=8080")
                elif key == 'CONSUL_HOST':
                    filled_content.append(f"{key}={ip_address}")
                elif key == 'CONSUL_PORT':
                    filled_content.append(f"{key}=8500")
                elif key == 'SERVICE_NAME':
                    filled_content.append(f"{key}={repo_name}")
                elif key == 'SERVICE_ID':
                    filled_content.append(f"{key}={repo_name}{service_index}")
                elif key == 'SERVICE_IP':
                    filled_content.append(f"{key}={ip_address}")
                elif key == 'SERVICE_PORT':
                    filled_content.append(f"{key}={service_port}")
                elif key == 'JWT_SECRET':
                    filled_content.append(f"{key}={jwt_secret}")
                else:
                    if value.strip():
                        filled_content.append(f"{key}={value}")
                    else:
                        filled_content.append(f"{key}=placeholder_value")
            else:
                filled_content.append(line)
                
        # Write to .env file
        with open(env_path, 'w') as env_file:
            env_file.write('\n'.join(filled_content))
            
        print(f"Created .env file for {repo_name}")
        
    except Exception as e:
        print(f"Error setting up environment for {repo_name}: {str(e)}")

def main():
    # Get and display IP address
    ip_address = get_ip_address()
    print(f"Server IP Address: {ip_address}\n")

    print("Cloning services...")
    clone_services()

    print("\nCloned repositories:")
    for index, (repo_name, repo_path) in enumerate(repo_paths.items()):
        service_env_setup(ip_address, repo_name, repo_path, index)

    
if __name__ == "__main__":
    main() 