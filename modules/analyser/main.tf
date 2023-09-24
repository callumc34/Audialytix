module "analyser-container-gce" {
  # https://github.com/terraform-google-modules/terraform-google-container-vm
  source  = "terraform-google-modules/container-vm/google"
  version = "~> 2.0"

  container = {
    image = "${var.region}-docker.pkg.dev/${var.project}/${var.registry.repository_id}/${var.registry.analyser.image}"
    env = [
      {
        name  = "PORT"
        value = var.port
      },
      {
        name  = "HOST",
        value = "0.0.0.0"
      },
      {
        name  = "DEBUG",
        value = var.debug
      }
    ]
  }

  restart_policy = "Always"
}

resource "google_compute_instance" "main" {
  project      = var.project
  name         = "analyser-instance"
  machine_type = var.machine_type
  zone         = var.zone
  tags         = ["analyser"]

  boot_disk {
    initialize_params {
      image = module.analyser-container-gce.source_image
    }
  }

  network_interface {
    subnetwork = var.subnetwork_id
  }

  metadata = {
    gce-container-declaration = module.analyser-container-gce.metadata_value
    google-logging-enabled    = "true"
    google-monitoring-enabled = "true"
  }

  labels = {
    container-vm = module.analyser-container-gce.vm_container_label
  }

  service_account {
    email = var.service_account_email
    scopes = [
      "cloud-platform"
    ]
  }
}
