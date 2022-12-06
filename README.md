## Snyk Tag Monitor

Snyk allowed us a custom limit of 5000 unique key-value pairs that can be used as tags. This scheduled lambda first clears out
any orphaned tags, then counts up the remaining tags in use on snyk projects. The lambda runs every day, and sends
an email to the security team if that number is higher than 4500. The number of tags is logged, and also registered as a
cloudwatch datapoint. Cloudwatch will use the `stage` dimension `DEV` or`INFRA`, depending on whether the code was run locally
or on AWS, respectively.

### Running locally
Before running the code locally you will need
- Federated access to the security account, and that profile set to the default. (setting the `AWS_DEFAULT_PROFILE` environment
variable is a quick way to do this)
- A default region set.

To run, execute the setup script (in `scripts/setup.sh`) to install all required dependencies in a virtual
environment. Activate the environment by running `source .venv/bin/activate` from the root of the project, and finally, run the
program using `python3 src/main.py`.
