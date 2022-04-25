from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_ecs as ecs,
    aws_ecr_assets as ecs_assets,
    aws_ecs_patterns as ecs_patterns
)


class EcsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        cluster = ecs.Cluster(self, "MyCluster", vpc=vpc)
        container_name = "ContainerName1"
        image_asset = ecs_assets.DockerImageAsset(self, container_name, directory="./docker-app")
        image = ecs.ContainerImage.from_docker_image_asset(image_asset)
        ecs_patterns.ApplicationLoadBalancedFargateService(self, "MyService",
                                                           cluster=cluster,
                                                           cpu=256,
                                                           memory_limit_mib=512,
                                                           desired_count=2,
                                                           listener_port=80,
                                                           task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                                                               image=image,
                                                               container_name=container_name,
                                                               container_port=80
                                                           ),
                                                           public_load_balancer=True

                                                           )
