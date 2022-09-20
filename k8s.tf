variable "kubeconfigpath" {
  type     = string
  nullable = false
}
variable "kubeconfigcontext" {
  type     = string
  nullable = false
}
variable "image" {
  type     = string
  nullable = false
}
variable "port" {
  type     = string
  nullable = false
}
variable "target_port" {
  type     = string
  nullable = false
}
variable "replicas" {
  type     = string
  nullable = false
}

resource "kubernetes_namespace" "systeminfo" {
  metadata {
    name = "systeminfo"
  }
}

resource "kubernetes_service" "systeminfo-service" {
  metadata {
    name = "systeminfo-service"
  }
  spec {
    selector = {
      app = kubernetes_deployment.systeminfo.metadata.0.labels.app
    }
    session_affinity = "None"
    port {
	  node_port   = 30201
      protocol    = "TCP"
      port        = var.port
      target_port = var.target_port
    }
    type = "NodePort"
  }
}


resource "kubernetes_deployment" "systeminfo" {
  metadata {
    name = "systeminfo-app"
    labels = {
      app = "systeminfoapp"
    }
  }

  spec {
    replicas = var.replicas

    selector {
      match_labels = {
        app = "systeminfoapp"
      }
    }

    template {
      metadata {
        labels = {
          app = "systeminfoapp"
        }
      }

      spec {
        container {
          image = var.image
          name  = "systeminfo"
		  port {
            container_port = 5000
		  }
          env {
            name = "PORT"
            value = "5000"
          }
          resources {
            limits = {
              cpu    = "0.5"
              memory = "512Mi"
            }
            requests = {
              cpu    = "250m"
              memory = "50Mi"
            }
          }
        }
      }
    }
  }
}