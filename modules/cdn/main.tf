resource "google_storage_bucket" "static" {
  name          = var.name
  storage_class = "STANDARD"
  location      = var.region
  force_destroy = true
}

resource "google_storage_default_object_access_control" "public_rule" {
  bucket = google_storage_bucket.static.name
  role   = "READER"
  entity = "allUsers"
}
