pipeline {
  agent { label 'dind' }

  environment {
    REGISTRY = 'acrclock105915912.azurecr.io'
    IMAGE    = 'clock-backend'
    TAG      = 'dev'
  }

  stages {

    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Wait for Docker') {
      steps {
        container('dind') {
          sh '''
            echo "Waiting for Docker daemon..."
            until docker info > /dev/null 2>&1; do
              sleep 2
            done
            echo "Docker is ready"
          '''
        }
      }
    }

    stage('Build Image') {
      steps {
        container('dind') {
          sh '''
            echo "Building Docker image..."
            docker build -t $REGISTRY/$IMAGE:$TAG .
          '''
        }
      }
    }

    stage('Push Image') {
      steps {
        withCredentials([usernamePassword(
          credentialsId: 'acr-creds',
          usernameVariable: 'ACR_USER',
          passwordVariable: 'ACR_PASS'
        )]) {
          container('dind') {
            sh '''
              echo "Logging in to ACR..."
              echo $ACR_PASS | docker login $REGISTRY -u $ACR_USER --password-stdin

              echo "Pushing image..."
              docker push $REGISTRY/$IMAGE:$TAG
            '''
          }
        }
      }
    }

    stage('Deploy to AKS') {
      steps {
        withCredentials([usernamePassword(
          credentialsId: 'github-creds',
          usernameVariable: 'GIT_USER',
          passwordVariable: 'GIT_PASS'
        )]) {
          container('jnlp') {
            sh '''
              echo "Installing kubectl..."
              curl -LO "https://dl.k8s.io/release/$(curl -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
              chmod +x kubectl

              echo "Cloning infra repo..."
              if [ ! -d "clock-infra" ]; then
                git clone https://$GIT_USER:$GIT_PASS@github.com/jayalekshmyps/clock-infra.git
              fi

              cd clock-infra

              echo "Deploying to AKS (dev)..."
              ./kubectl apply -k k8s/overlays/dev
            '''
          }
        }
      }
    }

  }

  post {
    success {
      echo "Backend build, push, and deployment successful"
    }
    failure {
      echo "Pipeline failed"
    }
  }
}
``