import requests
from requests.auth import HTTPDigestAuth
import json
from datetime import datetime

# Credentials
login = "service@networkoptix.com"
password = "mysupersecretpassword"





# Function to fetch license data for a given ID
def fetch_license_data(id):
    license_url = f"https://{id}.relay.vmsproxy.com/ec2/getLicenses"
    response = requests.get(license_url, auth=HTTPDigestAuth(login, password))

    if response.status_code == 200:
        try:
            license_data = response.json()
            return license_data
        except json.JSONDecodeError:
            print(f"Error decoding JSON response for ID: {id}")
    else:
        print(f"Error fetching license data for ID: {id}. HTTP status code {response.status_code}")

# URL to fetch the JSON data
url = "https://nxvms.com/cdb/system/get"

# Make the HTTP request with authentication
response = requests.get(url, auth=(login, password))

# Check if the request was successful (HTTP status code 200)
if response.status_code == 200:
    try:
        # Parse the JSON response
        data = response.json()

        # Extract "name" and "id" from each system
        extracted_data = [{"name": system["name"], "id": system["id"], "licenses": fetch_license_data(system["id"])} for system in data["systems"]]

        # Generate HTML content
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>NX Licenses</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 20px;
      background-color: #f1f1f1;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 20px;
      background-color: #fff;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    th, td {
      padding: 15px;
      text-align: left;
      border-bottom: 1px solid #ddd;
    }
    th {
      background-color: #f2f2f2;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <h1>NX Licenses</h1>
  <table>
    <thead>
      <tr>
        <th>Name</th>
        <th>Licenses</th>
      </tr>
    </thead>
    <tbody>
"""
        # Add data rows to HTML table
        for system_data in extracted_data:
            html_content += f"<tr><td>{system_data['name']}<br>ID: {system_data['id']}</td><td>"
            if "licenses" in system_data and system_data["licenses"]:
                for license in system_data["licenses"]:
                    html_content += f"<b>Key:</b> {license['key']}<br><pre>{license['licenseBlock']}</pre><br>"
            else:
                html_content += "No licenses available"
            html_content += "</td></tr>"

        html_content += """
    </tbody>
  </table>
</body>
</html>
"""

        # Add date and time to the HTML file name
        date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"nx_license_{date_time}.html"

        # Save the HTML content to a file (nxlicenses_<date_time>.html)
        with open(file_name, "w") as f:
            f.write(html_content)

        print(f"HTML page generated successfully. Saved as {file_name}")
    except json.JSONDecodeError:
        print("Error decoding JSON response.")
else:
    print(f"Error: HTTP status code {response.status_code}")
