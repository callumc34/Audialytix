output "private_ip" {
  value = google_sql_database_instance.main.private_ip_address
}
