# Self hosted runner on GitHub

#### Build image
`docker build --tag runner-image .`

#### Run image
`docker run
  --detach
  --env ORGANIZATION="dart1277/aws-cdk"
  --env ACCESS_TOKEN=$ACCESS_TOKEN
  --name runner
  runner-image`

#### Stop runner
docker kill --signal=SIGINT runner

curl -X POST -H "Authorization: token $ACCESS_TOKEN" https://api.github.com/repos/dart1277/aws-cdk/actions/runners/registration-token

curl -X GET -H "Authorization: token $ACCESS_TOKEN" https://api.github.com/repos/dart1277/aws-cdk/deployments

curl -X DELETE -H "Authorization: token $ACCESS_TOKEN" https://api.github.com/repos/dart1277/aws-cdk/deployments/

-- not working with private repo -- curl -X POST -H "Authorization: token $ACCESS_TOKEN" https://api.github.com/orgs/dart1277/aws-cdk/actions/runners/registration-token

git-format-patch, apply with git-am