import boto3
import os

# Statics
rentention_policy_check = (1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1827, 3653)
default_retention_policy = 365

# Environment Variables
RETENTION_POLICY = os.getenv('RETENTION_POLICY')

# Setup
aws_log_regions = boto3.session.Session().get_available_regions('logs')
aws_log_clients = {}
for index, item in enumerate(aws_log_regions):
    aws_log_clients[item] = boto3.client('logs',item)

# Input validation
if RETENTION_POLICY is not None:
    if RETENTION_POLICY.isdigit() and int(RETENTION_POLICY) in rentention_policy_check:
        RETENTION_POLICY = int(RETENTION_POLICY)
    else:
        print "WARNING: RETENTION_POLICY value is not a valid value, valid values are: %s" % str(rentention_policy_check)
        RETENTION_POLICY = None

# Functions
def describe_log_groups_for_region(region):
    response = aws_log_clients[region].describe_log_groups()
    logGroups = response['logGroups']
    while 'nextToken' in response:
        response = aws_log_clients[region].describe_log_groups(nextToken=response['nextToken'])
        logGroups += response['logGroups']

    return logGroups

def filter_no_retention_policy(logGroups):
    returnGroup = []
    for index, item in enumerate(logGroups):
        if 'rententionInDays' not in item:
            returnGroup.append(item)
    return returnGroup

def apply_retention_policy(region, logGroups, policy):
    if policy:
        print 'Checking Retention Policys for Region %s...' % region
        for logGroup in logGroups:
            response = aws_log_clients[region].put_retention_policy(logGroupName=logGroup['logGroupName'],retentionInDays=policy)

def handler(event, context):
    for index, item in enumerate(aws_log_regions):
        apply_retention_policy(item, filter_no_retention_policy(describe_log_groups_for_region(item)),RETENTION_POLICY or default_retention_policy)

if __name__ == "__main__":
    handler(None, None)
