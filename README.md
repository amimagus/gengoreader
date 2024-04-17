# gengoreader
Reads Gengo RSS feed

A secrets yaml file of the following format is required. Items in brackets must be replaced with respective values.
apiVersion: v1
kind: Secret
metadata:
  name: secret-basic-auth
type: kubernetes.io/basic-auth
stringData:
  username: [EMAIL]
  password: [PASSWORD/API KEY]