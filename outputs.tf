output "analyser_ip" {
  description = "Static IP address of analyser instance"
  value       = google_compute_address.analyser.address
}
