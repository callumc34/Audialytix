output "website_ip" {
  description = "Static IP address of website instance"
  value       = google_compute_address.website.address
}
