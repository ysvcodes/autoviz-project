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
stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }
    stages {
        stage('Build') {
            steps {
<<<<<<< HEAD
                bat 'docker build -t autoviz-dashboard .'
=======
                script {
                    echo "Starting Build and Test stage..."
                    try {
                        // Ensure workspace is clean before build

                        echo "Building Docker image: ${DOCKER_IMAGE_NAME}:${DOCKER_TAG}"
                        bat "docker build -t ${DOCKER_IMAGE_NAME}:${DOCKER_TAG} ."
                        echo "Docker image built successfully."

                        echo "Running tests inside the container..."
                        // This command runs pytest within a new container from the image we just built.
                        // The container is automatically removed after tests (--rm).
                        bat "docker run --rm ${DOCKER_IMAGE_NAME}:${DOCKER_TAG} pytest tests/"
                        echo "Tests completed."

                    } catch (Exception e) {
                        echo "Build or test failed: ${e.message}"
                        currentBuild.result = 'FAILURE'
                        error("Build or test stage failed: ${e.message}") // error step will mark stage as failed
                    }
                }
>>>>>>> 86e3ba1d43b0abb1819bff3055317b3e55b19535
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
