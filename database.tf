resource "google_sql_database_instance" "main" {
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
      ipv4_enabled = true
      authorized_networks {
        name  = "allow-all"
        value = "0.0.0.0/0"
      }
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
