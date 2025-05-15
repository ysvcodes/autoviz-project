// Jenkinsfile for autoviz-project (inspired by example)
/*
 * Author: autoviz-project user
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
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }
        stage('Build and Test') {
            steps {
                script {
                    echo "Starting Build and Test stage..."
                    try {
                        // Ensure workspace is clean before build

                        echo "Building Docker image: ${DOCKER_IMAGE_NAME}:${DOCKER_TAG}"
                        bat "docker build -t ${DOCKER_IMAGE_NAME}:${DOCKER_TAG} -f app/Dockerfile app"
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
            }
        }

        stage('Deploy (Simulated)') {
            steps {
                script {
                    echo "Starting Deploy (Simulated) stage..."
                    // Stop and remove existing container if it exists, to avoid conflicts
                    try {
                        echo "Attempting to stop existing container: ${CONTAINER_NAME}"
                        bat "docker stop ${CONTAINER_NAME}"
                        echo "Attempting to remove existing container: ${CONTAINER_NAME}"
                        bat "docker rm ${CONTAINER_NAME}"
                        echo "Cleanup of existing container successful (if it existed)."
                    } catch (Exception e) {
                        // It's okay if stop/rm fails if the container doesn't exist.
                        // This is a common pattern.
                        echo "No existing container named '${CONTAINER_NAME}' to clean up, or an error occurred: ${e.message}"
                    }

                    try {
                        echo "Deploying new container: ${CONTAINER_NAME} from image ${DOCKER_IMAGE_NAME}:${DOCKER_TAG}"
                        // Run the new container in detached mode (-d)
                        // Map port 8001 on the host to port 5000 in the container
                        // (Flask app in Dockerfile runs on 5000)
                        bat "docker run -d -p 8001:5000 --name ${CONTAINER_NAME} ${DOCKER_IMAGE_NAME}:${DOCKER_TAG}"
                        echo "Deployment successful. Container '${CONTAINER_NAME}' started."
                        echo "Access at http://localhost:8001 if Jenkins runs locally."
                    } catch (Exception e) {
                        echo "Deployment failed: ${e.message}"
                        currentBuild.result = 'FAILURE'
                        error("Deployment stage failed: ${e.message}")
                    }
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finished. Cleaning up workspace..."
            cleanWs() // Cleans the Jenkins workspace after the build.
        }
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed!"
            // Consider adding notifications here for real projects
        }
    }
}
