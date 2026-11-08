# SAS Interview Challenge

## Problem Statement

You are working for a SaaS company where customers can purchase your product.
When a customer completes their purchase, an automated pipeline should be triggered
that onboards them to the platform.

**The Goal:**
When the pipeline completes, the customer should be able to view a personalized
welcome screen that displays:

- Their company name
- Their company motto
- A "Welcome to SAS" message

**Scale Requirements:**

- Handle onboarding for 10-100 customers efficiently  
- Pipeline should be automated and reliable
- Solution should accommodate customer-specific data
- Consider how this scales as your customer base grows

## What We're Looking For

We want to see your DevOps thinking and problem-solving approach. You should:

- **Select 2-3 objectives** from the list below that interest you most
- **Create a script/solution** in any language you prefer (bash, python, groovy,
  yaml, etc.)
- **Demonstrate your understanding** of the chosen concepts
- **Document your approach** and reasoning

*Note: This does NOT need to be runnable code - pseudo code and well-commented
scripts are perfectly acceptable.*

## 10 Key Objectives to Consider

Choose a few objectives that align with your interests and expertise:

### 2. **Data Deployment to Web Servers**

Design a mechanism for deploying customer-specific data (company name, motto) to
backend web servers running in Kubernetes. Consider how to package data into ConfigMaps
or Secrets, update pod configurations, and manage rolling deployments across multiple
web server pods without downtime.

### 5. **Pipeline Orchestration**

Design the workflow that coordinates all onboarding steps from purchase completion
to live customer page. Consider using tools like Github Workflows or Github Actions.
Along with task queues, error handling, and process monitoring.

### 8. **Configuration Management**

Design a system for managing customer-specific configurations in Kubernetes using
ConfigMaps, Secrets, and custom resources. Consider Helm charts for templating,
Kustomize overlays, and feature flags that might vary per customer tier or package.

## Your Deliverable

Create a folder/file structure that demonstrates your chosen objectives. For example:

- `my-solution/` directory
- Implementation script(s) in your preferred language
- Documentation explaining your approach
- Any configuration files or templates needed

## Notes Section

*Use this space as your scratch pad for ideas, architecture diagrams (ASCII art
welcome!), or planning notes.*

---

### Planning Notes

```text
Primary Objectives:
02: Data Deployment to Web Servers
  - Populate pipeline variables with data pulled via API from CRM at runtime
  - Default to templated ConfigMaps, configuration customizable based on CRM data
  - Restart resources with rollout, post verification of correct configuration for new entries
  - Separate company identifier from customer display name (i.e. generate a cryptographic UUID to ID customer to prevent namespace collisions as well as to anonymize customer name in URL generation)

05: Pipeline Orchestration
  - Trigger build from invoice completion in CRM via webhook
  - Provision necessary git repo(s), database, application pods, and ingress configuration(s) at runtime
  - Apply a customizable application configuration from Helm chart based on pipeline variables
  - Scale number of available process runners in line with demand to keep wait time for new builds to a minimum while also keeping total concurrent compute resources to a minimum

10: Error Handling & Recovery
  - Verbose logging of error messages
  - Errors for incomplete data pulls from CRM alert both Ops and relevant Sales Engineer(s); limit inputs in CRM to pulldown menus where possible and require fields when necessary
  - Retry logic that works based on errors (e.g. backoff/retry for errors that indicate temporary failures (401, 503, 504, etc.), ask for operator verification on non-temporary failures (403, 500, 502, etc.))
  - Use pipeline orchestration to track each stage of deployment and automatically retry failures, while ignoring successful completions
  - Trigger alerts for repeated failures requiring manual intervention
  - Successful completion triggers customer alert prompting their verification of correct configuration

```

### Architecture Sketches

```text

Purchase -> Pipeline -> Personalized Page

Customer Journey:
1. Customer completes purchase
2. System captures necessary information
3. Pipeline generates personalized page
4. Customer sees "Welcome [Company], [Motto]" page

```

### Implementation Ideas

```text
Pipeline:
- Trigger build from invoice completion in CRM via webhook

- Separate company identifier from customer display name (i.e. generate a cryptographic UUID to ID customer to prevent namespace collisions as well as to anonymize customer name in URL generation)
    - CRM generates and stores Customer UUID at invoice completion

- Populate pipeline variables with data pushed via API webhook from CRM at runtime
    - This is done via URL construction for POST request to the pipeline API
    - Initially populates a friendly name and a UUID for the Customer

- Provision necessary git repo(s), database, application pods, and ingress configuration(s) at runtime

- Default to templated ConfigMaps and such; configuration customizable based on CRM data and editable from the Customer's side
    - Apply a customizable application configuration based on pipeline variables
    - Errors for incomplete data pulls from CRM alert both Ops and relevant Sales Engineer(s); limit inputs in CRM to pulldown menus where possible and require fields when necessary
    - Retry logic that works based on errors (e.g. backoff/retry for errors that indicate temporary failures (401, 503, 504, etc.), ask for operator verification on non-temporary failures (403, 500, 502, etc.))
    - Use pipeline orchestration to track each stage of deployment and automatically retry failures, while ignoring successful completions
    
- Restart resources, as necessary, with rollout, post verification of correct configuration for new entries
    - Successful completion triggers customer alert prompting their verification of correct configuration
    - Leverage CRM API for customer communications

```

---

*Good luck! We're excited to see your approach to solving this customer onboarding
pipeline challenge.*