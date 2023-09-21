variable "analyser_port" {
  description = "Port for the analyser to listen on"
  default     = "80"
  type        = string
}

variable "analyser_debug" {
  description = "Whether to run the analyser with debug mode on"
  default     = "False"
  type        = string
}

variable "analyser_machine" {
  description = "Machine type for the analyser"
  default     = "n1-standard-1"
  type        = string
}

variable "database_machine" {
  description = "Machine type for the database"
  default     = "db-f1-micro"
  type        = string
}

variable "database_name" {
  description = "Name for the database"
  default     = "audialytix"
  type        = string
}

variable "database_user" {
  description = "Username for the database"
  default     = "audialytix-root"
  type        = string
}

variable "database_password" {
  description = "Password for the database"
  default     = "insecure-login"
  type        = string
}
