## Snyk Tag Monitor

Snyk has a hard limit of 1000 unique key-value pairs that can be used as tags. This scheduled lambda checks the number of tags we are using, and sends an alert if that number is too high.

## Running locally
1. Run [scripts/setup.sh](./scripts/setup.sh) to install depencencies
