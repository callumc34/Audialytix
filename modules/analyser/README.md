# Analyser Compute Instance

Deploys a GCE instance using the analyser image.

## Variables

| Name | Description | Default |
|------|-------------|---------|
| `project` | The name of the google project | audialytix |
| `region` | The region to deploy to | australia-southeast1 |
| `zone` | The zone to deploy to | australia-southeast1-a |
| `registry` | Artifact registry information |  |
| `machine_type` | The instance type to use | e2-micro |
| `port` | The port to listen on | 80 |
| `debug` | Whether to run with debug mode | False |
| `service_account_email` | The service account email to use |  |
| `subnetwork_id` | The VPC subnetwork to use |  |
