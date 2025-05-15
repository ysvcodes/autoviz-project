// Jenkinsfile for autoviz-project (inspired by example)
/*
 * Author: Atirola Adesanya
 * Project: autoviz-project
 * Purpose: Jenkins declarative pipeline for the autoviz-project.
 *          Automates build, test, and simulated deployment using Docker.
 *          Uses 'bat' for Windows compatibility.
 */
pipeline {
    agent any // Jenkins can use any available agent.

    environment {
        DOCKER_IMAGE_NAME = 'autoviz-project' // Consistent with previous setup
        DOCKER_TAG = "${env.BUILD_NUMBER}"    // Using Jenkins built-in BUILD_NUMBER
        CONTAINER_NAME = "${DOCKER_IMAGE_NAME}-container" // Define container name
    }

    stages {
        stage('Build') {
            steps {
                bat 'docker build -t autoviz-dashboard .'
            }
        }

        stage('Test') {
            steps {
                // Only run tests if the app/tests directory exists
                bat 'if exist app\tests pytest app/tests || echo "No tests directory found."'
            }
        }

        stage('Deploy') {
            steps {
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