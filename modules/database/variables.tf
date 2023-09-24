variable "region" {
  description = "Region to deploy the database"
  default     = "australia-southeast1"
  type        = string
}

variable "name" {
  description = "Name for the database"
  default     = "audialytix"
  type        = string
}

variable "user" {
  description = "Username for the database"
  default     = "audialytix-root"
  type        = string
}

variable "password" {
  description = "Password for the database"
  default     = "insecure-login"
  type        = string
}

variable "machine_type" {
  description = "Machine type for the database"
  default     = "db-f1-micro"
  type        = string
}

variable "private_network_id" {
  description = "Private network for the database"
}
