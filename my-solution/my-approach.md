My approach to this exercise was to leverage existing systems wherever possible. I worked from the assumption that the CRM has a full featured API and can be counted as a source of truth for customer related data. Additional assumptions include a comprehensive monitoring solution, a GitLab instance, and a Kubernetes production environment. Additionally, I have chosen to focus on Objectives 2 (Data Deployment), 5 (Pipeline Orchestration), and 10 (Error Handling & Recovery)

The pipeline I have created has three stages:
- A "build" stage where artifacts for the rest of the pipeline are created
- A "test" stage where the data pulled from the CRM is verified for completeness and integrity
- A "deploy" stage where the customer's website is deployed to production

In the first stage, the pipeline executes a Python script to pull information from the CRM and use to populate a dict with relevant information about the customer and then generate a JSON file for subsequent scripts to pull information from and a ConfigMap to provide the HTML payload for the customer's website. Error handling includes verifying the correct customer with both a name and a UUID, and verifying connectivity with the CRM and some automated recovery options.

In the second stage, the pipeline executes another Python script to verify that none of the necessary variable fields are empty and that the created_date field has the appropriate format, so as to verify that it was created automatically by the CRM and not manually entered. All error messages are reported verbosely, for process monitors that can trigger alerts for operator intervention.

In the final stage, the pipeline executes a series of commands to create a Kubernetes namespace, deploy an NGINX instance, deploy a ConfigMap for said NGINX instance, and then restart the instance to pick up the new configuration. Upon successful completion, an alert is generated and transmitted to the customer informing them of the URL of their new web app.

All steps will automatically retry on failures due to errors with the runner system, execution timeouts, and exit code 137, which is the error code denoting OoM exceptions for Kubernetes.

Included is a values.yml file for Gitlab Runners deployed via Kubernetes that describes a simple scaling regime suitable for 10-100 customer instances.