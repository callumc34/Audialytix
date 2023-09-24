resource "google_artifact_registry_repository" "main" {
  location      = var.region
  repository_id = var.registry.repository_id
  description   = "Container repository for storing audialytix containers"
  format        = "DOCKER"
}

resource "null_resource" "analyser_build_image" {
  depends_on = [google_artifact_registry_repository.main]

  triggers = {
    timestamp = timestamp()
  }

  provisioner "local-exec" {
    command = "gcloud builds submit --project ${var.project} --tag ${var.region}-docker.pkg.dev/${var.project}/${var.registry.repository_id}/${var.registry.analyser.image} ${path.root}/files/analyser"
  }
}

resource "null_resource" "website_build_image" {
  depends_on = [google_artifact_registry_repository.main]

  triggers = {
    timestamp = timestamp()
  }

  provisioner "local-exec" {
    command = "gcloud builds submit --project ${var.project} --tag ${var.region}-docker.pkg.dev/${var.project}/${var.registry.repository_id}/${var.registry.website.image} ${path.root}/files/website"
  }
}
