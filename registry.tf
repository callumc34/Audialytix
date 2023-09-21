locals {
  repository_id  = "audialytix-container-repository"
  analyser_image = "analyser:latest"
  website_image  = "website:latest"
}

resource "google_artifact_registry_repository" "main" {
  location      = local.region
  repository_id = "audialytix-container-repository"
  description   = "Container repository for storing audialytix containers"
  format        = "DOCKER"
}

resource "null_resource" "analyser_build_image" {
  depends_on = [google_artifact_registry_repository.main]

  triggers = {
    timestamp = timestamp()
  }

  provisioner "local-exec" {
    command = "gcloud builds submit --project ${local.project} --tag ${local.region}-docker.pkg.dev/${local.project}/${local.registry.repository_id}/${local.registry.analyser.image} ${path.module}/analyser"
  }
}
