import asyncio
import json

import httpx
import jinja2
from assets.queries import queries
from tqdm.asyncio import tqdm_asyncio
import os



port_client_id = os.environ["PORT_CLIENT_ID"]
port_client_secret = os.environ["PORT_CLIENT_SECRET"]

leanix_client_secret = os.environ["LEANIX_SECRET"]

port_host = 'https://api.getport.io/v1'
leanix_host = 'https://eu.leanix.net'


def handle_request_error(e):
    if e.is_error:
        print(e.status_code)
        print(e.text)
    e.raise_for_status()


def get_token():
    body = {
        'clientId': port_client_id,
        'clientSecret': port_client_secret,
    }
    auth_res = httpx.post(f'{port_host}/auth/access_token', json=body)

    handle_request_error(auth_res)
    return auth_res.json()['accessToken']


def generate_leanix_token():
    token_url = f"{leanix_host}/services/mtm/v1/oauth2/token"
    res = httpx.post(token_url, data={
        "client_id": "apitoken",
        "client_secret": leanix_client_secret,
        "grant_type": 'client_credentials'
    })
    handle_request_error(res)

    return res.json()['access_token']


headers = {
    "Authorization": f"Bearer {get_token()}"
}
leanix_headers = {"Authorization": f"Bearer {generate_leanix_token()}", 'Content-Type': 'application/json'}


def create_blueprints():
    f = open('assets/blueprints.json')
    print("Trying to create blueprints")

    data = json.load(f)
    for blueprint in data:
        res = httpx.post(f'{port_host}/blueprints', json=blueprint, headers=headers)
        if res.is_error:
            print(f"Failed creating blueprint {blueprint['identifier']}, skipping")
            if res.status_code != 409:
                print(res.status_code)
                print(res.text)
        else:
            print(f"Created blueprint {blueprint['identifier']}")


def get_or_create_webhook():
    f = open('assets/webhook.json')
    print("Trying to fetch the webhook url")
    data = json.load(f)
    res = httpx.get(f'{port_host}/webhooks/{data["identifier"]}', headers=headers)
    if res.status_code == 404:
        print("Webhook not found, creating")
        res = httpx.post(f'{port_host}/webhooks', json=data, headers=headers)
    handle_request_error(res)
    return res.json()['integration']['url']


async def ingest(semaphore, client, webhook_url: str, data):
    async with semaphore:
        res = await client.post(webhook_url, json=data)
        res.raise_for_status()
        # Throttling the requests
        await asyncio.sleep(0.3)


def paginate_query(webhook_url: str, query: str):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    semaphore = asyncio.Semaphore(5)

    page_size = 100
    end_cursor = ""
    more = True
    client = httpx.AsyncClient(timeout=160)
    tasks = []
    page = 1

    while more:
        template = jinja2.Template(query, enable_async=True)
        q = template.render(
            end_cursor=end_cursor,
            page_size=page_size
        )
        print(f"Querying page {page}, page size {page_size}")
        res = httpx.request("POST", f"{leanix_host}/services/pathfinder/v1/graphql", headers=leanix_headers, json={
            "query": q
        })
        handle_request_error(res)
        data = res.json()['data']['allFactSheets']

        more = data['pageInfo']['hasNextPage']
        end_cursor = data['pageInfo']['endCursor']
        for edge in data['edges']:
            tasks.append(ingest(semaphore, client, webhook_url, edge['node']))
        page += 1

    print("All pages queried, waiting for ingestion to finish")
    asyncio.get_event_loop().run_until_complete(tqdm_asyncio.gather(*tasks))


def query_and_ingest(webhook_url: str):
    for idx, q in enumerate(queries):
        print(f"Syncing query {idx + 1} out of {len(queries)}")
        paginate_query(webhook_url, q.strip().replace('\n', ""))


if __name__ == '__main__':
    create_blueprints()
    url = get_or_create_webhook()
    print(url)
    query_and_ingest(url)
    print("Completed ingestion")
