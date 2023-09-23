module "analyser-container-gce" {
  depends_on = [null_resource.analyser_build_image]

  # https://github.com/terraform-google-modules/terraform-google-container-vm
  source  = "terraform-google-modules/container-vm/google"
  version = "~> 2.0"

  container = {
    image = "${local.region}-docker.pkg.dev/${local.project}/${local.registry.repository_id}/${local.registry.analyser.image}"
    env = [
      {
        name  = "PORT"
        value = var.analyser_port
      },
      {
        name  = "HOST",
        value = "0.0.0.0"
      },
      {
        name  = "DEBUG",
        value = var.analyser_debug
      }
    ]
  }

  restart_policy = "Always"
}

resource "google_compute_instance" "analyser" {
  project      = local.project
  name         = "analyser-instance"
  machine_type = var.analyser_machine
  zone         = local.zone
  tags         = ["analyser"]

  boot_disk {
    initialize_params {
      image = module.analyser-container-gce.source_image
    }
  }

  network_interface {
    subnetwork = google_compute_subnetwork.main.id
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
    email = google_service_account.main.email
    scopes = [
      "cloud-platform"
    ]
  }
}
