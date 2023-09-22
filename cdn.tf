resource "google_storage_bucket" "static" {
  name          = "audialytix-static"
  storage_class = "STANDARD"
  location      = local.region
  force_destroy = true
}

resource "google_storage_default_object_access_control" "public_rule" {
  bucket = google_storage_bucket.static.name
  role   = "READER"
  entity = "allUsers"
}
