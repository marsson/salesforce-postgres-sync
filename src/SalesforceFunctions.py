import subprocess
import json
import os

def get_sf_auth_and_instance(org_name:str):
    try:
        env = os.environ.copy()
        env['NO_COLOR'] = '1'

        # Execute the sf command and capture the output
        result = subprocess.run(['sf', 'org', 'display', '-o', org_name, '--json'],
                              capture_output=True,
                              text=True,
                              check=True,
                              env=env
                                )

        # Parse the JSON output
        json_output = json.loads(result.stdout)

        # Extract the specific fields
        access_token = json_output.get('result', {}).get('accessToken')
        instance_url = json_output.get('result', {}).get('instanceUrl')

        if not access_token or not instance_url:
            print("Could not find accessToken or instanceUrl in the response")
            return None, None

        return access_token, instance_url


    except subprocess.CalledProcessError as e:
        print(f"Command execution failed: {e}")
        print(f"Error output: {e.stderr}")
        return None
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON output: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None