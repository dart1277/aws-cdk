import aws_cdk
from constructs import Construct
from aws_cdk import (
    Stack,
    aws_ec2 as ec2
)


class VPC2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # vpc_id = self.node.try_get_context("vpc_id") # cdk diff -c vpc_id=vpc-017fdf3bba2c88916 or add in cdk.json
        vpc = ec2.Vpc.from_lookup(self, "VPC", is_default=True) #vpc_id="vpc-017fdf3bba2c88916")
        subnets = vpc.select_subnets(subnet_type=ec2.SubnetType.PUBLIC)

        aws_cdk.CfnOutput(self, "publicSubnets", value=str(subnets.subnet_ids))
