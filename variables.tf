variable "project" {
  description = "Project ID"
  default     = "audialytix"
  type        = string
}

variable "region" {
  description = "Region to deploy the instances"
  default     = "australia-southeast1"
  type        = string
}

variable "zone" {
  description = "Zone to deploy the instances in"
  default     = "australia-southeast1-a"
  type        = string
}

variable "analyser_machine_type" {
  description = "Machine type for the analyser instance"
  default     = "e2-micro"
  type        = string
}

variable "analyser_port" {
  description = "Port for the analyser instance"
  default     = 80
  type        = number
}

variable "analyser_debug" {
  description = "Whether to run the analyser with debug mode on"
  default     = "False"
  type        = string
}

variable "database_db_name" {
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

variable "database_machine_type" {
  description = "Machine type for the database instance"
  default     = "db-f1-micro"
  type        = string
}

variable "website_machine_type" {
  description = "Machine type for the website"
  default     = "e2-micro"
  type        = string
}

variable "website_port" {
  description = "Port for the website to listen on"
  default     = "80"
  type        = string
}

variable "website_secret_key" {
  description = "Secret key for the website"
  default     = "\"django-insecure-#6l*)qe#e-qq#kf@18m(e-34tg7^pikd81v0(+vupy)w%7mlln\""
  type        = string
}

variable "website_debug" {
  description = "Whether to run the website with debug mode on"
  default     = "False"
  type        = string
}
