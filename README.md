# Snowflake Git Integration: 60-Second Guide for Devs ❄️🐙⏱️

A quick demo of [Snowflake's Git integration](https://docs.snowflake.com/en/developer-guide/git/git-setting-up) , version control for your data workflows in under a minute? You bet! ⚡❄️.

This demo uses[SNOW CLI](https://docs.snowflake.com/en/developer-guide/snowflake-cli/index) to perform all tasks from the CLI.

## Pre-requisites

- Snowflake [Trial Account](https://signup.snowflake.com/)
- [GitHub](https://github.com) Account
- [SNOW CLI](https://docs.snowflake.com/en/developer-guide/snowflake-cli/index)

### Snowflake Environment

Create a database, schema and a warehouse to use to hold all the git repos and related objects

```shell
snow sql --stdin <<EOF
CREATE DATABASE IF NOT EXISTS MY_GIT_REPOS;
CREATE SCHEMA IF NOT EXISTS GITHUB;
CREATE WAREHOUSE IF NOT EXISTS MY_GIT_WH;
EOF
```

We will set them as our default datbase, schema and warehouse for the rest of the demo,

```shell
export SNOWFLAKE_CONNECTIONS_TRIAL_DATABASE='MY_GIT_REPOS'
export SNOWFLAKE_CONNECTIONS_TRIAL_SCHEMA='GITHUB'
export SNOWFLAKE_CONNECTIONS_TRIAL_WAREHOUSE='MY_GIT_WH'
```

### Create Git Repos

Set few variables that we can interploate later in the script,

```shell
export GIT_REPO_NAME='snow_cli_demo'
export GIT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
```

#### Git Integration Demo

```shell
#https://github.com/Snowflake-Labs/snow-cli-demo.git
snow git setup "$GIT_REPO_NAME"
```

* `Repo URL`: https://github.com/Snowflake-Labs/snow-cli-demo.git
* Select `N` to secret as this`sf-git-integration-demo` for public repo or provide the secret usually the [GitHub PAT](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
* Default to create an git API integration

Fetch all branches, tags and commits,

```shell
snow git fetch "$GIT_REPO_NAME"
```

List all branches

```shell
snow git list-branches "$GIT_REPO_NAME"
```

List all tags

```shell
snow git list-tags "$GIT_REPO_NAME"
```

List all files on branch snow-cli,

```shell
snow git list-files "@$GIT_REPO_NAME/branches/$GIT_BRANCH/" --pattern '.*\.sql'
```

## Run SQL from Git Repo

We will create a simple `TODOS` table and load the data from `todos.sql`.

To make the setup and tear down easy and customizable, let use the following env

```shell
export TODO_WH='TODO_APP_WH'
export TODO_DB_NAME='TODO_APP_DB'
export TODO_SCHEMA_NAME='DATA'
```

Setup TODO APP warehouse, database, schemas and tables,

```shell
snow git execute "@$GIT_REPO_NAME/branches/$GIT_BRANCH/todos.sql" \
  --variable "db_name='$TODO_DB_NAME'" \
  --variable "schema_name='$TODO_SCHEMA_NAME'" \
  --variable "wh_name='$TODO_WH'" \
  --variable "git_repo_name='$SNOWFLAKE_CONNECTIONS_TRIAL_DATABASE.$SNOWFLAKE_CONNECTIONS_TRIAL_SCHEMA.$GIT_REPO_NAME'" \
  --variable "git_branch='$GIT_BRANCH'"
```

Verify and check if objects has been created,

```shell
snow sql -q "select * from todos" \
  --dbname="$TODO_DB_NAME" \
  --schema="$TODO_SCHEMA_NAME"
```

## Deploy Streamlit Application

There is simple Streamlit application that is available under [app](./app) directory.

```shell
cd app
```

Let us create a schema to deploy the Todo APP,

```shell
snow sql -q 'create schema if not exists apps' --dbname="$TODO_DB_NAME"
```

Deploy Streamlit app,

```shell
snow streamlit deploy --dbname="$TODO_DB_NAME" --schema="apps"
```

You can use the URL from the output of the successful deployment to access the application.

>[!TIP]
> You can also get the URL of the application anytime using the command
>```shell
> snow streamlit get-url todo_app --dbname=--dbname="$TODO_DB_NAME" --schema="apps"
> ```
> You can find the app name in [snowflake.yml](./app/snowflake.yml)

## Cleanup

```shell
snow git execute "@$GIT_REPO_NAME/branches/$GIT_BRANCH/cleanup.sql" \
  --variable "db_name='$TODO_DB_NAME'"
```

Verify clean up and the `$TODO_DB_NAME` should be listed,

```shell
snow sql -q "SHOW DATABASES"
```

> [!TIP]
> If you are a [jq](https://jqlang.github.io/jq/) fan then use the following query to list the names of the databases
> ```shell
> snow sql -q "SHOW DATABASES" --format=json | jq -r '.[].name'
> ```