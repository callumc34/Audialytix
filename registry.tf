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

resource "null_resource" "website_build_image" {
  depends_on = [google_artifact_registry_repository.main]

  triggers = {
    timestamp = timestamp()
  }

  provisioner "local-exec" {
    command = "gcloud builds submit --project ${local.project} --tag ${local.region}-docker.pkg.dev/${local.project}/${local.registry.repository_id}/${local.registry.website.image} ${path.module}/audialytix"
  }
}

resource "google_project_iam_member" "artifact_registry_reader" {
  project = local.project
  role    = "roles/artifactregistry.reader"
  member  = "serviceAccount:${google_service_account.main.email}"
}
