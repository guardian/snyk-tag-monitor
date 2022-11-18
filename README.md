## Snyk Tag Monitor

Snyk has a limit of 1000 unique key-value pairs that can be used as tags. This scheduled lambda checks the number of tags we are using once every two days, and sends an email to the security team if that number is higher than 900.
