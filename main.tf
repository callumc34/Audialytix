terraform {
  backend "gcs" {
    prefix = "audialytix/state"
    bucket = "terraform-audialytix" // Must be pre-setup
  }
}

locals {
  project = "audialytix"
  region  = "australia-southeast1"
  zone    = "australia-southeast1-a"

  registry = {
    repository_id = "audialytix-container-repository"
    analyser = {
      //image = "${local.region}-docker.pkg.dev/${local.project}/${local.registry.repository_id}/${local.registry.analyser.image}"
      image = "analyser:latest"
    }
    website = {
      //tag = "${local.region}-docker.pkg.dev/${local.project}/${local.registry.repository_id}/${local.registry.website.image}"
      image = "website:latest"
    }
  }
}

provider "google" {
  project = local.project
  region  = local.region
}
