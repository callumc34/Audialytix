resource "google_sql_database_instance" "main" {
  name             = "audialytix-database"
  database_version = "POSTGRES_15"
  region           = var.region

  deletion_protection = false

  settings {
    tier              = var.machine_type
    activation_policy = "ALWAYS"

    // TODO(Callum): Setup private network with website
    // https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/sql_database_instance
    ip_configuration {
      ipv4_enabled    = false
      private_network = var.private_network_id
    }
  }
}

resource "google_sql_database" "main" {
  name     = var.name
  instance = google_sql_database_instance.main.name
}

resource "google_sql_user" "root" {
  depends_on = [google_sql_database_instance.main]

  name     = var.user
  password = var.password
  instance = google_sql_database_instance.main.name
}
