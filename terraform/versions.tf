terraform {
  required_version = ">= 1.0.0"

  required_providers {
    kind = {
      source  = "tehcyx/kind"
      version = "~> 0.6.0"  # 안정적인 최신 버전 대역 사용
    }
  }
}