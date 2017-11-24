#!/bin/bash
usage() {
    echo "Usage: $0 [-p S3Prefix | --prefix S3Prefix] [-r Region | --region Region] [-f Profile | --profile Profile] -- S3Bucket"
}
OPTS=`getopt -o p: --long prefix: -n $0 --- "$@"`

while true; do
    case "$1" in
        -p|--prefix)
            case "$2" in
                "") shift 2 ;;
                *) PREFIX="--s3-prefix $2"; shift 2 ;;
            esac ;;
        -r|--region)
            case "$2" in
                "") shift 2 ;;
                *) REGION="--region $2"; shift 2 ;;
            esac ;;
        -f|--profile)
            case "$2" in
                "") shift 2 ;;
                *) PROFILE="--profile $2"; shift 2;;
            esac ;;
        --) shift; break ;;
        "") usage; exit 1 ;;
        *) echo "Unsupported option: $1"; usage; exit 1 ;;
    esac
done

case $1 in
    "") echo "No bucket provided!"; exit 1 ;;
    *) BUCKET=$1 ;;
esac
zip lambda-function.zip lambda-function.py
aws cloudformation package --template-file retention_policy.yml --s3-bucket $BUCKET $PREFIX --output-template-file packaged_retention_policy.yml $REGION $PROFILE
aws cloudformation deploy --template-file packaged_retention_policy.yml --stack-name CloudWatchLogsRetentionPolicy --capabilities CAPABILITY_IAM $REGION $PROIFLE
rm -f lambda-function.zip packaged_retention_policy.yml
