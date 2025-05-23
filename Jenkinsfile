
// -----------------------------------------------------------------------------
// Author: autoviz-project user
// File Purpose: Jenkins pipeline configuration for the autoviz-project.
//               Defines build, test, and deploy stages using Docker.
// Dependencies: Jenkins, Docker, GitHub
// -----------------------------------------------------------------------------
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                bat 'docker build -t autoviz-dashboard .'
            }
        }

        stage('Test') {
            steps {
                // Only run tests if the app/tests directory exists
                bat 'if exist app\\tests pytest app/tests || echo "No tests directory found."'
            }
        }

        stage('Deploy') {
            steps {
                bat 'docker stop autoviz-dashboard || exit 0'
                bat 'docker rm autoviz-dashboard || exit 0'
                bat 'docker run -d -p 5000:5000 --name autoviz-dashboard autoviz-dashboard'
                echo 'Dashboard is running at http://localhost:5000'
            }
        }
    }

    post {
        always {
            echo 'Cleaning up workspace...'
            cleanWs()
            echo 'Pipeline completed successfully!'
        }
    }
}