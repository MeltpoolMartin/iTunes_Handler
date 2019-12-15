pipeline {
  agent {
    dockerfile {
      filename 'Jenkinsfile'
    }

  }
  stages {
    stage('Example') {
      steps {
        sh 'echo \'Hello World!\''
      }
    }
  }
}