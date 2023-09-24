variable "project" {
  description = "Project ID"
  default     = "audialytix"
  type        = string
}

variable "region" {
  description = "Region to deploy the analyser"
  default     = "australia-southeast1"
  type        = string
}

variable "zone" {
  description = "Zone to deploy the analyser"
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
  description = "Machine type for the analyser"
  default     = "e2-micro"
  type        = string
}

variable "port" {
  description = "Port for the analyser to listen on"
  default     = "80"
  type        = string
}

variable "debug" {
  description = "Whether to run the analyser with debug mode on"
  default     = "False"
  type        = string
}

variable "service_account_email" {
  description = "Service account email for the analyser"
  type        = string
}

variable "subnetwork_id" {
  description = "Subnetwork ID for the analyser instance"
  type        = string
}
