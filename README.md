# Keyword Extraction EKS Deployment with Graviton Instances, Karpenter and CloudWatch Visibility

This project provides a complete guide to deploying a keyword extraction service on AWS EKS using Karpenter for node auto-scaling and CloudWatch for monitoring and logging. The service is containerized using Docker and deployed to an EKS cluster, with Karpenter handling dynamic scaling of EC2 instances.

## Prerequisites

- AWS CLI installed and configured.
- `eksctl` and `kubectl` installed.
- Docker installed for building and pushing the application image.
- Helm installed for deploying Karpenter.

```bash
brew install eksctl helm
```
## Project Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/chrisk60331/eks-graviton-small-language-model.git
   cd eks-graviton-small-language-model

2. Build and Push Docker Image:
```bash
account_id=123445
aws ecr create-repository --repository-name keyword-extraction-app --region us-west-1
aws ecr get-login-password --region us-west-1 | \
docker login --username AWS --password-stdin $account_id.dkr.ecr.us-west-1.amazonaws.com
docker buildx build --platform linux/arm64 -t keyword-extraction-app .
docker tag keyword-extraction-app:latest $account_id.dkr.ecr.us-west-1.amazonaws.com/keyword-extraction-app:latest
docker push $account_id.dkr.ecr.us-west-1.amazonaws.com/keyword-extraction-app:latest
```
3. Create the EKS Cluster Using eksctl:
```bash
eksctl create cluster \
  --name keyword-extraction-cluster \
  --region us-west-1 \
  --nodegroup-name on-demand-nodes \
  --node-type m6g.large \
  --nodes 2 \
  --nodes-min 1 \
  --nodes-max 4 \
  --managed
  
aws eks update-kubeconfig --region us-west-1 --name keyword-extraction-cluster
```
4. Install Karpenter CRDs:
```bash
kubectl apply -f https://raw.githubusercontent.com/aws/karpenter/main/pkg/apis/crds/karpenter.sh_provisioners.yaml
helm repo add karpenter https://charts.karpenter.sh
helm repo update

helm upgrade --install karpenter karpenter/karpenter \
  --namespace karpenter \
  --create-namespace \
  --set serviceAccount.create=false \
  --set serviceAccount.name=karpenter \
  --set clusterName=keyword-extraction-cluster \
  --set clusterEndpoint=$(aws eks describe-cluster --name keyword-extraction-cluster --query "cluster.endpoint" --output text) \
  --set aws.defaultInstanceProfile=KarpenterNodeInstanceProfile \
  --wait
  
kubectl apply -f provisioner.yaml
```
5. Deploy
```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```
6. Adding CloudWatch Observability
```bash
eksctl utils associate-iam-oidc-provider --region=us-west-1 --cluster=keyword-extraction-cluster --approve
eksctl create iamserviceaccount \
  --name cloudwatch-agent \
  --namespace kube-system \
  --cluster keyword-extraction-cluster \
  --attach-policy-arn arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy \
  --approve
kubectl create namespace amazon-cloudwatch
  
kubectl apply -f https://raw.githubusercontent.com/aws/amazon-cloudwatch-agent/main/doc/container-insights/cloudwatch-agent-configmap.yaml
```
