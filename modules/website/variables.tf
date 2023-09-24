variable "project" {
  description = "Project ID"
  default     = "audialytix"
  type        = string
}

variable "region" {
  description = "Region to deploy the website"
  default     = "australia-southeast1"
  type        = string
}

variable "zone" {
  description = "Zone to deploy the website"
  default     = "australia-southeast1-a"
  type        = string
}

variable "registry" {
  description = "Artifact registry information"
  type = object({
    repository_id = string
    analyser = object({
      image = string
    })
    website = object({
      image = string
    })
  })
  default = {
    repository_id = "audialytix-container-repository"
    analyser = {
      image = "analyser:latest"
    }
    website = {
      image = "website:latest"
    }
  }
}

variable "machine_type" {
  description = "Machine type for the website"
  default     = "e2-micro"
  type        = string
}

variable "secret_key" {
  description = "Secret key for Django"
  default     = "\"django-insecure-#6l*)qe#e-qq#kf@18m(e-34tg7^pikd81v0(+vupy)w%7mlln\""
  type        = string
}

variable "port" {
  description = "Port for the website to listen on"
  default     = "80"
  type        = string
}

variable "debug" {
  description = "Whether to run the website with debug mode on"
  default     = "False"
  type        = string
}

variable "service_account_email" {
  description = "Service account email for the website"
  type        = string
}

variable "subnetwork_id" {
  description = "Subnetwork ID for the website instance"
  type        = string
}

variable "private_ip" {
  description = "Private IP address for the website to run on"
  default     = "10.0.1.3"
  type        = string
}

variable "public_ip" {
  description = "External public IP address for the website to run on"
  type        = string
}

variable "database_private_ip" {
  description = "Private IP for the database"
  type        = string
}

variable "database_port" {
  description = "Database port for the website"
  default     = "5432"
  type        = string
}

variable "database_username" {
  description = "Database username for the website"
  type        = string
}

variable "database_password" {
  description = "Database password for the website"
  type        = string
}

variable "database_db_name" {
  description = "Main database name for the website"
  type        = string
}

variable "analyser_private_ip" {
  description = "Private IP for the analyser"
  type        = string
}

variable "analyser_port" {
  description = "Port that the analyser is listening on"
  type        = string
}

variable "bucket_name" {
  description = "Name of the bucket for static hosting"
  default     = "audialytix-static"
  type        = string
}
