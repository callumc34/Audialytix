variable "project" {
  description = "Project ID"
  default     = "audialytix"
  type        = string
}

variable "region" {
  description = "Region to deploy the artifact registry"
  default     = "australia-southeast1"
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
