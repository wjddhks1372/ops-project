provider "kind" {}

resource "kind_cluster" "default" {
  name = "opsmind-local" # 요청하신 클러스터 이름

  kind_config {
    kind        = "Cluster"
    api_version = "kind.x-k8s.io/v1alpha4"

    # --- Node 1: Control Plane (Ingress 포트 매핑 포함) ---
    node {
      role = "control-plane"

      # Ingress Controller를 위해 호스트의 80 포트를 컨테이너의 80 포트로 연결
      extra_port_mappings {
        container_port = 80
        host_port      = 80
        listen_address = "0.0.0.0" # 모든 인터페이스에서 접근 허용
      }

      # Ingress Controller를 위해 호스트의 443 포트를 컨테이너의 443 포트로 연결
      extra_port_mappings {
        container_port = 443
        host_port      = 443
        listen_address = "0.0.0.0"
      }
      
      # Ingress 사용 시 필요한 레이블 설정 (선택 사항이지만 권장)
      kubeadm_config_patches = [
        "kind: InitConfiguration\nnodeRegistration:\n  kubeletExtraArgs:\n    node-labels: \"ingress-ready=true\"\n"
      ]
    }

    # --- Node 2: Worker ---
    node {
      role = "worker"
    }

    # --- Node 3: Worker ---
    node {
      role = "worker"
    }
  }
}