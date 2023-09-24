terraform {
  backend "gcs" {
    prefix = "audialytix/state"
    bucket = "terraform-audialytix" // Must be pre-setup
  }
}

provider "google" {
  project = local.project
  region  = local.region
}

locals {
  project = var.project
  region  = var.region
  zone    = var.zone

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

  website = {
    private_ip = "10.0.1.3"
  }
}

module "analyser" {
  depends_on = [module.iam, module.network]

  source = "./modules/analyser"

  project  = local.project
  region   = local.region
  zone     = local.zone
  registry = local.registry

  machine_type = var.analyser_machine_type
  port         = var.analyser_port
  debug        = var.analyser_debug

  service_account_email = module.iam.email
  subnetwork_id         = module.network.subnetwork_id
}

module "artifact" {
  source = "./modules/artifact"

  project  = local.project
  region   = local.region
  registry = local.registry
}

module "cdn" {
  source = "./modules/cdn"

  region = local.region
}

module "database" {
  depends_on = [module.network]

  source = "./modules/database"

  region = local.region

  name         = var.database_db_name
  user         = var.database_user
  password     = var.database_password
  machine_type = var.database_machine_type

  private_network_id = module.network.network_id
}

module "iam" {
  source = "./modules/iam"

  project = local.project
}

module "network" {
  source = "./modules/network"

  project = local.project
  region  = local.region

  analyser_port = var.analyser_port
  website_port  = var.website_port
}

module "project" {
  source = "./modules/project"

  project = local.project
}

module "website" {
  depends_on = [module.iam, module.network, module.database, module.analyser, module.cdn, module.artifact]

  source = "./modules/website"

  project  = local.project
  region   = local.region
  zone     = local.zone
  registry = local.registry

  machine_type = var.website_machine_type
  secret_key   = var.website_secret_key
  port         = var.website_port
  debug        = var.website_debug

  service_account_email = module.iam.email
  subnetwork_id         = module.network.subnetwork_id
  public_ip             = module.network.website_static_ip
  database_private_ip   = module.database.private_ip
  database_username     = var.database_user
  database_password     = var.database_password
  database_db_name      = var.database_db_name
  analyser_private_ip   = module.analyser.private_ip
  analyser_port         = var.analyser_port
  bucket_name           = module.cdn.static_bucket_name
}
