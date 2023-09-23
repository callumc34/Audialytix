module "project-services" {
  source  = "terraform-google-modules/project-factory/google//modules/project_services"
  version = "~> 12.0"

  project_id  = local.project
  enable_apis = true

  activate_apis = [
    "artifactregistry.googleapis.com",
    "compute.googleapis.com",
    "servicenetworking.googleapis.com",
    "storage-component.googleapis.com",
    "sql-component.googleapis.com"
  ]
  disable_services_on_destroy = false
}
