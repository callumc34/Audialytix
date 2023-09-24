variable "region" {
  description = "Region to deploy the static files bucket"
  default     = "australia-southeast1"
  type        = string
}

variable "name" {
  description = "Name of the bucket"
  default     = "audialytix-static"
  type        = string
}
