import os
import threading

import httpx

API_URL = "https://api.getport.io/v1"
MAX_THREADS = 5
sema = threading.Semaphore(value=MAX_THREADS)

CLIENT_ID = os.environ["PORT_CLIENT_ID"]
CLIENT_SECRET = os.environ["PORT_CLIENT_SECRET"]

DELETE_ENTITIES_FLAG = bool(os.getenv("DELETE_ENTITIES", 1))
DELETE_BLUEPRINTS_FLAG = bool(os.getenv("DELETE_BLUEPRINTS", 1))
DELETE_WEBHOOK_FLAG = bool(os.getenv("DELETE_WEBHOOK", 0))

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
        timeout=60
    )
    sema.release()
    if res.status_code == 200:
        print(f"Entity {entity} deleted")
    else:
        print(f"Encountered error deleting {entity}: {res.json()}")


def delete_blueprint(blueprint):
    res = httpx.delete(
        f"{API_URL}/blueprints/{blueprint}",
        headers=headers,
        timeout=60
    )
    return res.is_success or res.status_code == 404

def delete_leanix_webhook(identifier):
    res = httpx.delete(
        f"{API_URL}/webhooks/{identifier}",
        headers=headers,
        timeout=60
    )
    if res.is_error and res.status_code != 404:
        print(f"Failed to delete webhook {identifier}: {res.json()}")
        res.raise_for_status()

def delete_all(blueprints):
    blueprints_to_delete = set(blueprints)
    deleted_blueprints = set()
    while blueprints_to_delete - deleted_blueprints:
        report_threads = []
        left_blueprints = blueprints_to_delete - deleted_blueprints
        for blue in left_blueprints:
            print(f"Searching for entities in {blue}")
            entities = httpx.get(f"{API_URL}/blueprints/{blue}/entities", headers=headers, timeout=60)
            if entities.status_code != 404:
                print(f"Starting to delete all {blue} entities")
                res = entities.json()
                for ent in res["entities"]:
                    report_thread = threading.Thread(target=delete_port_entity, args=(blue, ent["identifier"]))
                    report_thread.start()
                    report_threads.append(report_thread)

                for thread in report_threads:
                    thread.join()

                if DELETE_BLUEPRINTS_FLAG:
                    if delete_blueprint(blue):
                        deleted_blueprints.add(blue)
                        print(f"Deleted blueprint {blue}")
                    else:
                        print(f"Failed to delete blueprint {blue}. Retrying...")
                elif not res["entities"]:
                    deleted_blueprints.add(blue)
            else:
                deleted_blueprints.add(blue)
                print(f"Blueprint {blue} not found. Skipping...")


blueprints = ["component",
              "provider",
              "domain",
              "product",
              "data_objects",
              "resource",
              "business_service",
              "interface",
              "system"]

if DELETE_ENTITIES_FLAG:
    delete_all(blueprints)
if DELETE_ENTITIES_FLAG:
    delete_leanix_webhook("leanix-eam")

print("Done deleting")
