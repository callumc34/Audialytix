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
