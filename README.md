# LeanIX Sync

The LeanIX sync script is a python script that can be used to synchronize data from LeanIX into Port.
It is based on the LeanIX GraphQL API to query factSheets and Port's Generic Webhook Integration to map the factSheets into
the catalog.

## Installation & Run

!!! Make sure that you have python 3.6 or higher installed.
!!! Make sure that you fill the required configuration in the script.

```python
port_client_id = 'PORT_CLIENT_ID'
port_client_secret = 'PORT_CLIENT_SECRET'

leanix_client_secret = 'LEANIX_SECRET'
```

```bash
pip install -r requirements.txt

python sync.py
```

## How to clear and start over

!!! Make sure to fill in Port `client_id` and `client_secret` in the `clean.py` script.

To clear the data ingested into port you can use the `clean.py` python script to remove all the ingested data from the
`sync.py` script.

The clean script will delete all the blueprints and their entities according to the defined list of blueprints in the script file.

```bash
pip install -r requirements.txt

python clean.py
```

## Q & A

- Why are old entities not deleted in the sync process?

  The sync process does not delete entities, it only updates or creates new ones.

- What blueprints are created?

  The blueprints that are created are based on the `./assets/blueprints.json` file.

- What is the generic webhook integration configuration?

  The webhook configuration is based on the `./assets/webhook.json` file.

- How can I change the data queried from LeanIX?

  The data that is queried from LeanIX is based on the `./assets/queries.py` file.
  The queries are written in GraphQL.
  Each query in the list will be executed and paginated accordingly

  !!! Make sure that you add the following fields to filter the query according to the pagination:

  ```
    after: "{{ end_cursor }}"
    first: {{ page_size }}
  ```
