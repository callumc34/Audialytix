resource "google_compute_address" "website" {
  name   = "website-static-ip"
  region = local.region
}

resource "google_compute_network" "main" {
  name                    = "audialytix-network"
  auto_create_subnetworks = false
}

resource "google_compute_global_address" "service_range" {
  name          = google_compute_address.website.name
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 24
  network       = google_compute_network.main.id
}

resource "google_service_networking_connection" "main" {
  network                 = google_compute_network.main.self_link
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.service_range.name]
}

resource "google_compute_subnetwork" "main" {
  name                     = "audialytix-subnetwork"
  ip_cidr_range            = "10.0.1.0/28"
  network                  = google_compute_network.main.id
  private_ip_google_access = true
}

resource "google_compute_firewall" "website" {
  name    = "website-access"
  network = google_compute_network.main.name

  allow {
    protocol = "tcp"
    ports    = ["80", "443"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["website"]
}

resource "google_compute_firewall" "analyser" {
  name    = "website-to-analyser-access"
  network = google_compute_network.main.name

  allow {
    protocol = "tcp"
    ports    = ["80"]
  }

  source_ranges = ["${google_compute_instance.website.network_interface.0.network_ip}/32"]
  target_tags   = ["analyser"]
}
