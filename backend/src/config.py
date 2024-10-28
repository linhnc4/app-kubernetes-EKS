import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DEFAULT_EKS_CLUSTER_NAME = os.getenv('DEFAULT_EKS_CLUSTER_NAME')
DEFAULT_GITHUB_REPO = os.getenv('DEFAULT_GITHUB_REPO')
DEFAULT_GITHUB_USER = os.getenv('DEFAULT_GITHUB_USER')
DEFAULT_KUBECTL_ROLE = os.getenv('DEFAULT_KUBECTL_ROLE')