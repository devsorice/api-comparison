import http.client
import json
import random
import uuid
from datetime import datetime
import logging
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_settings():
    logging.info("Loading settings from settings.json")
    with open('settings.json') as f:
        settings = json.load(f)
    return settings

def generate_random_user():
    logging.info("Generating a random user")
    uid = uuid.uuid4()
    return {
        "name": f"User {uid}",
        "email": f"user{random.randint(1, 9999999999)}@example.com"
    }

def send_request(method, url, body=None):
    logging.info(f"Sending {method} request to {url}")
    parsed_url = urlparse(url)
    conn = http.client.HTTPConnection(parsed_url.netloc)
    headers = {"Content-Type": "application/json"}
    if body:
        body = json.dumps(body)
    conn.request(method, parsed_url.path, body, headers)
    response = conn.getresponse()
    response_data = response.read().decode()
    response_body = json.loads(response_data) if response.getheader("Content-Type") == "application/json" else response_data
    return response, response_body

def create_initial_users(base_url, num_initial_users):
    logging.info(f"Creating {num_initial_users} initial users")
    created_user_ids = []
    for _ in range(num_initial_users):
        user_data = generate_random_user()
        logging.info(f"Creating user: {user_data}")
        response, response_body = send_request("POST", f"{base_url}/user/create-one", user_data)
        if response.status == 201:
            created_user_ids.append(response_body)
        else:
            logging.error("------")
            logging.error("Failed to create initial user.")
            logging.error(f"Status: {response.status}   |  Response Body: {json.dumps(response_body)}")
            logging.error("------")
            exit()

    if not created_user_ids:
        logging.error("No users created, exiting tests.")
        exit()
    return created_user_ids

class CallLog:
    def __init__(self, start, end, time_elapsed, request_headers, request_url, request_body, response_headers, response_body):
        self.start = start
        self.end = end
        self.time_elapsed = time_elapsed
        self.request_headers = request_headers
        self.request_url = request_url
        self.request_body = request_body
        self.response_headers = response_headers
        self.response_body = response_body

def perform_request(route_name, route_info, created_user_ids):
    logging.info(f"Performing request for route: {route_name}")
    start = datetime.now()
    url = route_info["url"]
    method = route_info["method"]
    headers = {"Content-Type": "application/json"}
    body = None
    if "body_generator" in route_info:
        logging.info("Generating request body")
        body = route_info["body_generator"]()
    if "{id}" in url:
        logging.info("Replacing {id} in URL with a random user ID")
        user_id = random.choice(created_user_ids)
        url = url.replace("{id}", str(user_id))

    response, response_body = send_request(method, url, body)
    end = datetime.now()
    time_elapsed = (end - start).total_seconds() * 1000
    call_log = CallLog(
        start=start.isoformat(),
        end=end.isoformat(),
        time_elapsed=time_elapsed,
        request_headers=headers,
        request_url=url,
        request_body=body,
        response_headers=dict(response.getheaders()),
        response_body=response_body,
    )
    return call_log

def define_routes(base_url):
    logging.info("Defining routes")
    return {
        "get_user": {"method": "GET", "url": f"{base_url}/user/get/{{id}}"},
        "create_user": {"method": "POST", "url": f"{base_url}/user/create-one", "body_generator": generate_random_user},
        "create_users": {"method": "POST", "url": f"{base_url}/user/create-many", "body_generator": lambda: [generate_random_user() for _ in range(random.randint(1, 5))]},
        "list_users": {"method": "GET", "url": f"{base_url}/user/list"},
        "delete_user": {"method": "POST", "url": f"{base_url}/user/delete/{{id}}"},
        "update_user": {"method": "POST", "url": f"{base_url}/user/update-one/{{id}}", "body_generator": generate_random_user},
        "update_users": {"method": "POST", "url": f"{base_url}/user/update-many", "body_generator": lambda: [(random.choice(created_user_ids), generate_random_user()) for _ in range(random.randint(1, 5))]},
        "duplicate_user": {"method": "POST", "url": f"{base_url}/user/duplicate/{{id}}"}
    }

def main():
    settings = load_settings()
    num_initial_users = settings.get("num_initial_users", 0)
    routes_settings = settings.get("routes", {})
    base_url = "http://127.0.0.1:5555"

    created_user_ids = create_initial_users(base_url, num_initial_users)

    logging.info("Checking if there are users available for testing")
    response, response_body = send_request("GET", f"{base_url}/user/list")
    if response.status != 200 or not response_body:
        logging.error("No users available, exiting tests.")
        exit()

    routes = define_routes(base_url)

    logging.info("Opening log file for writing")
    with open('log.jsonl', mode='w') as writer:
        for route_name, num_calls in routes_settings.items():
            route_info = routes.get(route_name)
            if not route_info:
                continue
            for _ in range(num_calls):
                log = perform_request(route_name, route_info, created_user_ids)
                if log:
                    writer.write(json.dumps(log.__dict__) + "\n")

if __name__ == "__main__":
    main()
