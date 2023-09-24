module "website-container-gce" {
  # https://github.com/terraform-google-modules/terraform-google-container-vm
  source  = "terraform-google-modules/container-vm/google"
  version = "~> 2.0"

  container = {
    image = "${var.region}-docker.pkg.dev/${var.project}/${var.registry.repository_id}/${var.registry.website.image}"
    env = [
      {
        name  = "PORT"
        value = var.port
      },
      {
        name  = "HOST"
        value = "0.0.0.0"
      },
      {
        name  = "ALLOWED_HOSTS"
        value = "${var.public_ip},${var.private_ip}"
      },
      {
        name  = "DJANGO_SECRET_KEY"
        value = var.secret_key
      },
      {
        name  = "DJANGO_DEBUG"
        value = var.debug
      },
      {
        name  = "DB_HOST"
        value = var.database_private_ip
      },
      {
        name  = "DB_PORT"
        value = var.database_port
      },
      {
        name  = "DB_USERNAME"
        value = var.database_username
      },
      {
        name  = "DB_PASSWORD"
        value = var.database_password
      },
      {
        name  = "DB_NAME"
        value = var.database_db_name
      },
      {
        name  = "ANALYSER_HOST"
        value = "http://${var.analyser_private_ip}:${var.analyser_port}"
      },
      {
        name  = "WEBHOOK_RETURN_HOST"
        value = "http://${var.private_ip}:${var.port}"
      },
      {
        name  = "STATIC_URL"
        value = "https://storage.googleapis.com/${var.bucket_name}/"
      },
      {
        name  = "GS_BUCKET_NAME"
        value = var.bucket_name
      }
    ]
  }

  restart_policy = "Always"
}

resource "google_compute_instance" "main" {
  project      = var.project
  name         = "website-instance"
  machine_type = var.machine_type
  zone         = var.zone
  tags         = ["website"]

  boot_disk {
    initialize_params {
      image = module.website-container-gce.source_image
    }
  }

  network_interface {
    subnetwork = var.subnetwork_id
    network_ip = "10.0.1.3"
    access_config {
      nat_ip = var.public_ip
    }
  }

  metadata = {
    gce-container-declaration = module.website-container-gce.metadata_value
    google-logging-enabled    = "true"
    google-monitoring-enabled = "true"
  }

  labels = {
    container-vm = module.website-container-gce.vm_container_label
  }

  service_account {
    email = var.service_account_email
    scopes = [
      "cloud-platform"
    ]
  }
}
