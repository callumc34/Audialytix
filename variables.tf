variable "analyser_machine" {
  description = "Machine type for the analyser"
  default     = "n1-standard-1"
  type        = string
}

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

variable "website_machine" {
  description = "Machine type for the website"
  default     = "n1-standard-1"
  type        = string
}

variable "website_port" {
  description = "Port for the website to listen on"
  default     = "80"
  type        = string
}

variable "website_secret_key" {
  description = "Secret key for Django"
  default     = "\"django-insecure-#6l*)qe#e-qq#kf@18m(e-34tg7^pikd81v0(+vupy)w%7mlln\""
  type        = string
}

variable "website_debug" {
  description = "Whether to run the website with debug mode on"
  default     = "False"
  type        = string
}
