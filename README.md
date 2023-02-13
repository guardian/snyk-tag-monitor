## Snyk Tag Monitor

Snyk allowed us a custom limit of 5000 unique key-value pairs that can be used as tags. This scheduled lambda first clears out any orphaned tags, then counts up the remaining tags in use on Snyk projects. The lambda runs every day, and sends
an email to the security team if that number is higher than 4500. The number of tags is logged, and also registered as a
cloudwatch datapoint. Cloudwatch will use the `stage` dimension `DEV` or`INFRA`, depending on whether the code was run locally or on AWS, respectively.

### Running locally
Before running the code locally you will need:

1. federated access to the `security` account
2. to set the `security` account as default by running `export AWS_DEFAULT_PROFILE=security`
3. a default region set.

To run:

1. install all required dependencies in a virtual environment by running `./scripts/setup.sh` from the root of the project
2. activate the virtual environment by running `source .venv/bin/activate` from the root of the project
3. run the program using `python3 src/main.py`.
