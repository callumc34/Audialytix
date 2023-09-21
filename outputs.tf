output "analyser_ip" {
  description = "Static IP address of analyser instance"
  value       = google_compute_address.analyser.address
}

output "website_ip" {
  description = "Static IP address of website instance"
  value       = google_compute_address.website.address
}
