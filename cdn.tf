# resource "google_storage_bucket" "static" {
#   name = "audialytix-static"
#   storage_class = "STANDARD"
#   location = local.region
# }

# resource "google_compute_backend_bucket" "static" {
#   name = "audialytix-cdn"
#   description = "CDN Backend bucket for Audialytix static content"
#   bucket_name = google_storage_bucket.static.name
#   enable_cdn = true
# }

# resource "google_compute_url_map" "static" {
#   name = "audialytix-cdn"
#   description = "CDN URL map for Audialytix static content"
#   default_service = google_compute_backend_bucket.static.self_link
# }

# resource "google_compute_managed_ssl_certificate" "static" {
#   name = "audialytix-cdn"

#   managed {
#     domains = [local.project]
#   }
# }

# resource "google_compute_target_https_proxy" "static" {
#   name = "audialytix-cdn"
#   url_map = google_compute_url_map.static.self_link
#   ssl_certificates = [google_compute_managed_ssl_certificate.static.self_link]
# }

# resource "google_compute_global_address" "static" {
#   name         = "audialytix-cdn"
#   ip_version   = "IPV4"
#   address_type = "EXTERNAL"
# }

# resource "google_compute_global_forwarding_rule" "static" {
#   name       = "audialytix-cdn"
#   target     = google_compute_target_https_proxy.static.self_link
#   ip_address = google_compute_global_address.static.address
#   port_range = "443"
# }
