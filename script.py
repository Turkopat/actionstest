# coding: utf-8

# coding: utf-8

from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkvpc.v2.region.vpc_region import VpcRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkvpc.v2 import *
import subprocess

if __name__ == "__main__":
    # The AsdfaK and SK used for authentication are hard-coded or stored in plaintext, which has great security risks. It is recommended that the AK and SK be stored in ciphertext in configuration files or environment variables and decrypted during use to ensure security.
    # In this example, AK and SK are stored in environment variables for authentication. Before running this example, set environment variables CLOUD_SDK_AK and CLOUD_SDK_SK in the local environment
    ak = __import__('os').getenv("CLOUD_SDK_AK")
    sk = __import__('os').getenv("CLOUD_SDK_SK")
    sg = "04113e13-66ec-4acc-ad0e-e75ae981dcd8"
    ip = subprocess.run("dig +short myip.opendns.com @resolver1.opendns.com" , shell=True, check=True, text=True, stdout=subprocess.PIPE)
    ip_stdout= ip.stdout.strip()

    credentials = BasicCredentials(ak, sk) \

    client = VpcClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(VpcRegion.value_of("tr-west-1")) \
        .build()
    print(client)
    try:
        request = CreateSecurityGroupRuleRequest()
        securityGroupRulebody = CreateSecurityGroupRuleOption(
            security_group_id= sg,
            direction="ingress",
            protocol="tcp",
            remote_ip_prefix= ip_stdout
        )
        request.body = CreateSecurityGroupRuleRequestBody(
            security_group_rule=securityGroupRulebody
        )
        response = client.create_security_group_rule(request)
        print("Response alindi")
        print(response)
        subprocess.run('echo "sg_rule_id=' + response.security_group_rule.id + '" >> $GITHUB_ENV' , shell=True, check=True, text=True, stdout=subprocess.PIPE)

    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)
