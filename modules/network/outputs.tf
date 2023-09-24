output "network_id" {
  value = google_compute_network.main.id
}

output "subnetwork_id" {
  value = google_compute_subnetwork.main.id
}

output "website_static_ip" {
  value = google_compute_address.website.address
}
