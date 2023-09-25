# Website Compute Instance

Deploys a GCE instance using the website image.

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
| `private_ip` | The private IP address to use | 10.0.1.3 |
| `public_ip` | The public IP address assigned for the website |  |
| `database_private_ip` | The private IP address of the database |  |
| `database_port` | The port of the database | 5432 |
| `database_username` | The username of the database |  |
| `database_password` | The password of the database |  |
| `database_db_name` | The name of the database |  |
| `analyser_private_ip` | The private IP address of the analyser |  |
| `analyser_port` | The port of the analyser |  |
| `bucket_name` | The name of the bucket to use |  |
