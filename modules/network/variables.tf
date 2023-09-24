variable "project" {
  description = "Project ID"
  default     = "audialytix"
  type        = string
}

variable "region" {
  description = "Region to deploy the VPC network"
  default     = "australia-southeast1"
  type        = string
}

variable "analyser_port" {
  description = "Port that the analyser is listening on"
  default     = "80"
  type        = string
}

variable "website_private_ip" {
  description = "Private IP assigned to the website"
  default     = "10.0.1.3"
}

variable "website_port" {
  description = "Port that the website is listening on"
  default     = "80"
  type        = string
}
