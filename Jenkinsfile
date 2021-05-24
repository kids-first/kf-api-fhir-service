@Library(value='kids-first/aws-infra-jenkins-shared-libraries', changelog=false) _
ecs_service_type_1_standard {
    projectName                = "kf-api-fhir-service"
    orgFullName                = "kids-first"
    environments               = "dev,qa,prd"
    docker_image_type          = "debian"
    create_default_iam_role    = "1"
    entrypoint_command         = "/home/smile/smilecdr/bin/smilecdr run"
    quick_deploy               = "true"
    container_port             = "8000"
    health_check_path          = "/endpoint-health"
    external_config_repo       = "false"
    dependencies               = "ecr"
    deploy_scripts_version     = "master"
    vcpu_container             = "2048"
    memory_container           = "4096"
    internal_app               = "false"
    vcpu_task                  = "2048"
    internal_app               = "false"
    memory_task                = "4096"
    additional_container_ports = "9000,9100"
    snapshot_identifier_prd    = "kf-api-fhir-service-prd-migration-kms-rds"
}
