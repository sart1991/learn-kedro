# Kedro Application Helm Chart

This Helm chart can deploy the Kedro application in two modes:

1. **Job Mode (Default)**: For on-demand execution of the Kedro pipeline
2. **Deployment Mode**: For long-running service (legacy mode)

## Job Mode

In Job mode, the Kedro application is deployed as a Kubernetes Job that runs the pipeline and then completes. This is ideal for data processing tasks that need to be run on-demand rather than continuously.

### Configuration

The default configuration in `values.yaml` is set to Job mode:

```yaml
# Deployment mode: 'job' for on-demand execution or 'deployment' for long-running service
mode: job

# Job specific configuration
job:
  # Time to keep completed jobs (in seconds)
  ttlSecondsAfterFinished: 100
  # Number of retries before considering a job as failed
  backoffLimit: 3
```

### Triggering the Job On-Demand

To trigger the Kedro job on-demand, you can use the following kubectl command:

```bash
# Deploy the Helm chart if not already deployed
helmfile sync

# Delete any previous job instance to create a new one
kubectl delete job learn-kedro-service -n default

# The Helm chart will automatically create a new job
```

Alternatively, you can create a new job with a unique name each time:

```bash
# Generate a unique job name with a timestamp
JOB_NAME="learn-kedro-service-$(date +%s)"

# Create a new job by applying the Helm template with the unique name
helm template learn-kedro-service ./charts/learn-kedro-service \
  --set mode=job \
  --set "nameOverride=$JOB_NAME" \
  | kubectl apply -f -

# Check the job status
kubectl get jobs -n default
kubectl logs job/$JOB_NAME -n default
```

## Deployment Mode

To deploy the application as a long-running service, update the `mode` value in `values.yaml`:

```yaml
# Deployment mode: 'job' for on-demand execution or 'deployment' for long-running service
mode: deployment
```

Then apply the changes:

```bash
helmfile sync
```

## Monitoring Jobs

To check the status of your jobs:

```bash
# List all jobs
kubectl get jobs -n default

# Get details of a specific job
kubectl describe job learn-kedro-service -n default

# View logs from the job
kubectl logs job/learn-kedro-service -n default
```