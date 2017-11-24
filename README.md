# cloudwatch-logs-expiry-set
Lambda Function to set expiry on CloudWatch Logs that don't have it set.

This is useful for keeping your CloudWatch logs in check as by default you can have the logs accumulating quite a lot.

To use, clone and execute the setup script:

    Usage: ./setup.sh [-p S3Prefix | --prefix S3Prefix] [-r Region | --region Region] [-f Profile | --profile Profile] -- S3Bucket

This relies on the AWS CLI being installed and configured. You can select a region or profile using the options, and an S3 prefix. Make sure that the S3 Bucket you are using is in the same region.
