pipeline {
  agent {
    dockerfile {
      filename 'Jenkins'
    }

  }
  stages {
    stage('Example') {
      steps {
        sh 'echo "Hello World"'
      }
    }
  }
}