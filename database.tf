resource "google_sql_database_instance" "main" {
  depends_on       = [google_service_networking_connection.main]
  name             = "audialytix-database"
  database_version = "POSTGRES_15"
  region           = local.region

  deletion_protection = false

  settings {
    tier              = var.database_machine
    activation_policy = "ALWAYS"

    // TODO(Callum): Setup private network with website
    // https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/sql_database_instance
    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.main.id
    }
  }
}

resource "google_sql_database" "main" {
  name     = var.database_name
  instance = google_sql_database_instance.main.name
}

resource "google_sql_user" "root" {
  depends_on = [google_sql_database_instance.main]

  name     = var.database_user
  password = var.database_password
  instance = google_sql_database_instance.main.name
}
