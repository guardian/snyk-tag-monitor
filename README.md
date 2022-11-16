## Snyk Tag Monitor

Snyk has a hard limit of 1000 unique key-value pairs that can be used as tags. This scheduled lambda checks the number of tags we are using, and sends an alert if that number is too high.

## Running locally
1. Run [scripts/setup.sh](./scripts/setup.sh) to install depencencies
2. Set up the required environment variables, you'll need a SNYK_API_KEY with view permissions, and the SNYK_GROUP_ID for the whole guardian. 
3. Run `source .venv/bin/activate` from the root of the repository to activate the virtual environment.

