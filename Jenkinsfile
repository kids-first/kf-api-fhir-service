@Library(value='kids-first/aws-infra-jenkins-shared-libraries', changelog=false) _
ecs_service_type_1_standard {
    projectName                = "kf-api-fhir-service"
    orgFullName                = "kids-first"
    environments               = "qa,prd"
    docker_image_type          = "debian"
    create_default_iam_role    = "1"
    entrypoint_command         = "/home/smile/smilecdr/bin/smilecdr run"
    quick_deploy               = "true"
    container_port             = "8000"
    health_check_path          = "/endpoint-health"
    external_config_repo       = "false"
    dependencies               = "ecr"
    deploy_scripts_version     = "master"
    vcpu_container             = "4096"
    memory_container           = "8192"
    internal_app               = "false"
    vcpu_task                  = "4096"
    memory_task                = "8192"
    create_service_discovery   = "1"
    additional_container_ports = "9000,9100"
    additional_ssl_cert_domain_name = "*.kidsfirstdrc.org"
    external_domain = "kidsfirstdrc.org"
    service_timeout = "50"
    service_interval = "100"
    main_branch = "bugfix/al/DEVOPS-1065-sg-change"
    app_sg_name                = "ElasticMapReduce-Master-Private-qa-20210122222002664300000002"
}
