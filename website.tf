module "website-container-gce" {
  depends_on = [
    null_resource.analyser_build_image,
    //google_storage_bucket.static,
    google_compute_address.website,
    google_sql_database.main
  ]

  # https://github.com/terraform-google-modules/terraform-google-container-vm
  source  = "terraform-google-modules/container-vm/google"
  version = "~> 2.0"

  container = {
    image = "${local.region}-docker.pkg.dev/${local.project}/${local.registry.repository_id}/${local.registry.website.image}"
    env = [
      {
        name  = "PORT"
        value = var.website_port
      },
      {
        name  = "HOST"
        value = "0.0.0.0"
      },
      {
        name  = "ALLOWED_HOST"
        value = google_compute_address.website.address
      },
      {
        name  = "DJANGO_SECRET_KEY"
        value = var.website_secret_key
      },
      {
        name  = "DJANGO_DEBUG"
        value = var.website_debug
      },
      {
        name  = "DB_HOST"
        value = google_sql_database_instance.main.public_ip_address
      },
      {
        name  = "DB_PORT"
        value = "5432"
      },
      {
        name  = "DB_USERNAME"
        value = google_sql_user.root.name
      },
      {
        name  = "DB_PASSWORD"
        value = google_sql_user.root.password
      },
      {
        name  = "DB_NAME"
        value = google_sql_database.main.name
      },
      {
        name  = "ANALYSER_HOST",
        value = "http://${google_compute_address.analyser.address}"
      },
      {
        name  = "WEBHOOK_RETURN_HOST",
        value = "http://${google_compute_address.website.address}"
      }
    ]
  }

  restart_policy = "Always"
}

resource "google_compute_address" "website" {
  name   = "website"
  region = local.region
}

resource "google_compute_network" "website" {
  name = "website-network"
}

resource "google_compute_firewall" "website" {
  name    = "website-firewall"
  network = google_compute_network.website.name

  allow {
    protocol = "tcp"
    ports    = ["80"]
  }

  // TODO(Callum): Only allow traffic from audialytix website
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["website"]
}

resource "google_compute_instance" "website" {
  project      = local.project
  name         = "website-instance"
  machine_type = var.website_machine
  zone         = local.zone
  tags         = ["website"]

  boot_disk {
    initialize_params {
      image = module.website-container-gce.source_image
    }
  }

  network_interface {
    network = google_compute_network.website.name
    access_config {
      nat_ip = google_compute_address.website.address
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
    email = google_service_account.main.email
    scopes = [
      "cloud-platform"
    ]
  }
}
