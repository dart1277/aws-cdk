from constructs import Construct
from aws_cdk import (
    Stack,
    aws_ec2 as ec2
)


class VpcStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 cidr="10.10.0.0/16",
                 subnet_mask=24,
                 nat_gateways=1,
                 db_port=5432
                 , **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc(self,
                           "VPC1",
                           max_azs=2,
                           cidr=cidr,
                           nat_gateways=nat_gateways,
                           subnet_configuration=[
                               ec2.SubnetConfiguration(
                                   subnet_type=ec2.SubnetType.PUBLIC,
                                   name="Public1",
                                   cidr_mask=subnet_mask
                               ),
                               ec2.SubnetConfiguration(
                                   subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                                   name="Private1",
                                   cidr_mask=subnet_mask
                               ),
                               ec2.SubnetConfiguration(
                                   subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,  # no route to a nat gw
                                   name="DbSubnet",
                                   cidr_mask=subnet_mask
                               ),
                           ]
                           )
        private_subnets = self.vpc.private_subnets
        isolated_subnets = self.vpc.isolated_subnets

        isolated_nacl = ec2.NetworkAcl(self, "DBNAcl",
                                       vpc=self.vpc,
                                       subnet_selection=ec2.SubnetSelection(subnets=isolated_subnets)
                                       )

        for subnet_id, subnet in enumerate(private_subnets, start=1):
            isolated_nacl.add_entry("DbNACLIngress{0}".format(subnet_id * 100),
                                    rule_number=subnet_id * 100,
                                    cidr=ec2.AclCidr.ipv4(subnet.node.default_child.cidr_block),
                                    traffic=ec2.AclTraffic.tcp_port_range(db_port, db_port),
                                    rule_action=ec2.Action.ALLOW,
                                    direction=ec2.TrafficDirection.INGRESS
                                    )
            
            isolated_nacl.add_entry("DbNACLEgress{0}".format(subnet_id * 100),
                                    rule_number=subnet_id * 100,
                                    cidr=ec2.AclCidr.ipv4(subnet.node.default_child.cidr_block),
                                    traffic=ec2.AclTraffic.tcp_port_range(1024, 65535),
                                    rule_action=ec2.Action.ALLOW,
                                    direction=ec2.TrafficDirection.EGRESS
                                    )
