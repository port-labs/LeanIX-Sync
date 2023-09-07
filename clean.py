import threading

import httpx

API_URL = "https://api.getport.io/v1"
MAX_THREADS = 5
sema = threading.Semaphore(value=MAX_THREADS)

CLIENT_ID = "CLIENT_ID"
CLIENT_SECRET = "CLIENT_SECRET"

API_URL = "https://api.getport.io/v1"

credentials = {"clientId": CLIENT_ID, "clientSecret": CLIENT_SECRET}

token_response = httpx.post(f"{API_URL}/auth/access_token", json=credentials)

access_token = token_response.json()["accessToken"]

print(access_token)

headers = {"Authorization": f"Bearer {access_token}"}


def delete_port_entity(blueprint, entity):
    sema.acquire()
    res = httpx.delete(
        f"{API_URL}/blueprints/{blueprint}/entities/{entity}?delete_dependents=true",
        headers=headers,
    )
    sema.release()
    if res.status_code == 200:
        print(f"Entity {entity} deleted")
    else:
        print(f"Encountered error deleting {entity}: {res.json()}")


def delete_all(blueprints):
    report_threads = []
    for blue in blueprints:
        search = {
            "combinator": "and",
            "rules": [{"property": "$blueprint", "value": blue, "operator": "="}],
        }
        entities = httpx.post(f"{API_URL}/entities/search", headers=headers, json=search)
        print(f"Starting to delete all {blue} entities")
        res = entities.json()
        for ent in res["entities"]:
            report_thread = threading.Thread(target=delete_port_entity, args=(blue, ent["identifier"]))
            report_thread.start()
            report_threads.append(report_thread)

        for thread in report_threads:
            thread.join()


all_blueprints = httpx.get(f"{API_URL}/blueprints", headers=headers)

if all_blueprints.status_code != 200:
    print("Failed to get blueprints, exiting")
    exit(1)

blueprints = []

for blueprint in all_blueprints.json()["blueprints"]:
    blueprints.append(blueprint["identifier"])

# Enter here the identifiers of the blueprints you want to delete all entities from
blueprints = ["component",
              "provider",
              "domain",
              "product",
              "business_service",
              "system"]

delete_all(blueprints)

print("Done deleting")
