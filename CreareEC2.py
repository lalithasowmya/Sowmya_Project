#!/usr/bin/env python
# coding: utf-8

# In[1]:


import boto3
ec2 = boto3.client('ec2')
ec2.describe_instances()


# In[2]:


import boto3
resp = ec2.create_key_pair(KeyName = 'User')
resp['KeyMaterial']


# In[3]:
# Open and test the file to check the key got copied to the file

file = open('User.pem','w')
file.write(resp['KeyMaterial'])
file.close


# In[4]:
# this will populate existing security groups: 

ec2.describe_security_groups()



# In[6]:
#Create a security Group in default VPC

resp = ec2.create_security_group(
GroupName = 'User',
    Description = 'User sg',
    VpcId = 'vpc-3168ca4b'
)


# In[7]:


resp


# In[8]:


gid = resp['GroupId']
gid


# In[9]:
#AUthorize ports to create EC2 instance

ec2.authorize_security_group_ingress(
GroupId = gid,
    IpPermissions = [
        {
            'IpProtocol': 'tcp',
            'FromPort': 80,
            'ToPort': 80,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        },
        {
            'IpProtocol':  'tcp',
            'FromPort': 22,
            'ToPort': 22,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }   
    ]
)


# In[10]:


ec2_resource = boto3.resource('ec2')


# In[11]:
#Create EC2 Intance using aboe security groups and Keys: Attach an EBS volume of sixe 20GB.

instances = ec2_resource.create_instances (
    ImageId = 'ami-0533f2ba8a1995cf9',
    MinCount = 1,
    MaxCount = 1,
    InstanceType = 't2.micro',
    KeyName = 'User',
    BlockDeviceMappings = [
        {
            'DeviceName' : "/dev/xvda",
            'Ebs':{
                'DeleteOnTermination': True,
                'VolumeSize': 20
            }
        }
    ],
    SecurityGroups = ['User']
)


# In[12]:
#Populte the created instances list 

instances


# In[13]:
#Describes th ecreated instance configuration

ec2.describe_instances()


# In[14]:


import boto3
client = boto3.client('iam')


# In[19]:


import boto3
response = client.create_user(
    Path='/',
    UserName= 'User1',
    PermissionsBoundary= 'arn:aws:iam::aws:policy/AmazonEC2FullAccess',
    Tags=[
        {
            'Key': 'modeluser',
            'Value': 'IAMUSER'
        },
    ]
)


# In[20]:


import boto3
response = client.create_user(
    Path='/',
    UserName= 'User2',
    PermissionsBoundary= 'arn:aws:iam::aws:policy/AmazonEC2FullAccess',
    Tags=[
        {
            'Key': 'modeluser',
            'Value': 'IAMUSER'
        },
    ]
)







