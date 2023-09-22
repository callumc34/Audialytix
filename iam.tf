resource "google_service_account" "main" {
  account_id   = local.project
  display_name = local.project
}

resource "google_project_iam_member" "artifact_registry_reader" {
  project = local.project
  role    = "roles/artifactregistry.reader"
  member  = "serviceAccount:${google_service_account.main.email}"
}

resource "google_project_iam_member" "bucket_access" {
  project = local.project
  role    = "roles/storage.objectAdmin"
  member  = "serviceAccount:${google_service_account.main.email}"
}
