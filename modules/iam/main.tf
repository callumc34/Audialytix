resource "google_service_account" "main" {
  account_id   = var.project
  display_name = var.project
}

resource "google_project_iam_member" "artifact_registry_reader" {
  project = var.project
  role    = "roles/artifactregistry.reader"
  member  = "serviceAccount:${google_service_account.main.email}"
}

resource "google_project_iam_member" "bucket_access" {
  project = var.project
  role    = "roles/storage.objectAdmin"
  member  = "serviceAccount:${google_service_account.main.email}"
}
