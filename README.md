# Using Snowflake CLI ❄️❄️❄️❄️❄️🐙⏱️❄️❄️❄️❄️

A quick demo of using few killer features of [SNOW CLI](https://docs.snowflake.com/en/developer-guide/snowflake-cli/index)(`snow`) that will make your everyday Snowflake development tasks at breeze.

As part of this quick demo we will see how to use `snow` for,

- [x] [Snowflake's Git integration](https://docs.snowflake.com/en/developer-guide/git/git-setting-up)
- [x] Deploying [Streamlit in Snowflake](https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit)
- [x] Setup CI/CD using [Snowflake CLI](https://github.com/Snowflake-Labs/snowflake-cli-action) GitHub Action

> [!IMPORTANT]
> Make sure you have installed Snowflake CLI > 3.1.x, for all the demo scenarios to work.

## Pre-requisites

- Snowflake [Trial Account](https://signup.snowflake.com/)
- [GitHub](https://github.com) Account
- [SNOW CLI](https://docs.snowflake.com/en/developer-guide/snowflake-cli/index)

If you need to use GitHub Action set the following GitHub Environment Secrets to your fork,

- `SNOWFLAKE_ACCOUNT` - the Snowflake Accouunt ID
- `SNOWFLAKE_USER` - The user to perform all operations, for simple checks try with `ACCOUNTADMIN` before trying granular roles
- `PRIVATE_KEY_PASSPHRASE` - The Passphrase to be used to decrypt the Private Key 
- `PRIVATE_KEY_RAW`- The **ENCRYPTED** private key to be used when connecting via the GH Action.

### Snowflake Environment

Create a database, schema and a warehouse to use to hold all the git repos and related objects

We will set them as our default datbase, schema and warehouse for the rest of the demo,

```shell
export GIT_REPO_DB='MY_GIT_REPOS'
export GIT_REPO_SCHEMA='GITHUB'
export GIT_REPO_WAREHOUSE='MY_GIT_WH'
```

Create WareHouse,

```shell
snow object create warehouse \
  name="$GIT_REPO_WAREHOUSE" \
  comment='Warehouse that will be used in this demo.'
```

Create Database,

```shell
snow object create database \
  name="$GIT_REPO_DB" \
  comment='Database to hold all my Git repositories and related objects'
```

Create Schema,

```shell
snow object create schema \
  name="$GIT_REPO_SCHEMA" \
  comment='Schema to hold all GitHub repositories' \
  --database="$GIT_REPO_DB"
```


### Create Git Repos

Set few variables that we can interploate later in the script,

```shell
export GIT_REPO_NAME='snow_cli_demo'
export GITHUB_REF_NAME="$(git rev-parse --abbrev-ref HEAD)"
```

#### Git Integration Demo

```shell
#https://github.com/Snowflake-Labs/snow-cli-demo.git
snow git setup "$GIT_REPO_NAME" \
  --database="$GIT_REPO_DB" \
  --schema="$GIT_REPO_SCHEMA"
```

* `Repo URL`: https://github.com/Snowflake-Labs/snow-cli-demo.git
* Select `N` to secret as this`sf-git-integration-demo` for public repo or provide the secret usually the [GitHub PAT](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
* Default to create an git API integration

```shell
export GIT_REPO_FQN="$GIT_REPO_DB.$GIT_REPO_SCHEMA.$GIT_REPO_NAME"
```
Fetch all branches, tags and commits,

```shell
snow git fetch "$GIT_REPO_FQN"
```

List all branches

```shell
snow git list-branches "$GIT_REPO_FQN"
```

List all tags

```shell
snow git list-tags "$GIT_REPO_FQN"
```

List all files on branch snow-cli,

```shell
snow git list-files "@$GIT_REPO_FQN/branches/$GITHUB_REF_NAME/" --pattern '.*\.sql'
```

## Run SQL from Git Repo

We will create a simple `TODOS` table and load the data from `todos.sql`.

To make the setup and tear down easy and customizable, let use the following env

```shell
export TODO_APP_WH='TODO_APP_WH'
export TODO_APP_DB='TODO_APP_DB'
export TODO_APP_SCHEMA='APPS'
export TODOS_DATA_SCHEMA='DATA'
```

Setup TODO APP warehouse, database, schemas and tables,

```shell
snow git execute "@$GIT_REPO_FQN/branches/$GITHUB_REF_NAME/de" \
        --variable "db_name='$TODO_APP_DB'" \
        --variable "schema_name='$TODOS_DATA_SCHEMA'" \
        --variable "wh_name='$TODO_APP_WH'" \
        --variable "git_repo_name='$GIT_REPO_FQN'" \
        --variable "git_branch='$GITHUB_REF_NAME'" \
        --database $GIT_REPO_DB --schema $GIT_REPO_SCHEMA
```

Verify and check if objects has been created,

```shell
snow sql -q "select * from todos" \
  --database="$TODO_APP_DB" \
  --schema="$TODOS_DATA_SCHEMA"
```
> [!NOTE]
> **ONLY IF GH Action is Enabled**
> Update anything under app, de or data folders. Do a commit push to see GH Action trigger and updating your Snowflake data and app

## Deploy Streamlit Application

There is simple Streamlit application that is available under [app](./app) directory.

```shell
cd app
```

Deploy Streamlit app,

```shell
snow streamlit deploy --replace \
  --database $TODO_APP_DB --schema $TODO_APP_SCHEMA
```

You can use the URL from the output of the successful deployment to access the application.

>[!TIP]
> You can also get the URL of the application anytime using the command
>```shell
> snow streamlit get-url todo_app
> ```
> You can find the app name in [snowflake.yml](./app/snowflake.yml)

## Cleanup

```shell
snow git execute "@$GIT_REPO_FQN/branches/$GIT_BRANCH/cleanup.sql" \
  --variable "db_name='$TODO_APP_DB'" \
  --variable "git_repo_name='$GIT_REPO_FQN'" \
  --database "$GIT_REPO_DB"
```

It should delete the `$TODO_APP_DB` and the `MY_GIT_REPOS.GITHUB.SNOW_CLI_DEMO` Git repository.

Verify clean up and the `$TODO_APP_DB` should not be listed,

```shell
snow sql -q "SHOW DATABASES"
```

> [!TIP]
> If you are a [jq](https://jqlang.github.io/jq/) fan then use the following query to list the names of the databases
> ```shell
> snow sql -q "SHOW DATABASES" --format=json | jq -r '.[].name'
> ```
