@Library(value='kids-first/aws-infra-jenkins-shared-libraries', changelog=false) _
ecs_service_type_1_standard {
    projectName                = "kf-api-fhir-service"
    orgFullName                = "kids-first"
    account                    = "chopd3b"
    environments               = "dev,qa,prd"
    docker_image_type          = "debian"
    create_default_iam_role    = "1"
    entrypoint_command         = "/home/smile/smilecdr/bin/smilecdr run"
    quick_deploy               = "true"
    container_port             = "8000"
    health_check_path          = "/endpoint-health"
    external_config_repo       = "false"
    dependencies               = "postgres_rds"
    deploy_scripts_version     = "master"
    vcpu_container             = "4096"
    memory_container           = "16384"
    vcpu_task                  = "2048"
    memory_task                = "16384"
    additional_container_ports = "9000,9100"
}
