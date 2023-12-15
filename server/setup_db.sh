#!/bin/bash

echo "The current user is: $USER"

# 检查postgres
./check_brew_postgres.sh

# 定义数据库参数
DB_NAME="iot"
DB_USER=$USER

# 创建数据库
psql -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;"

# 构建用于创建表的SQL命令
CREATE_TABLE_SQL="
CREATE TABLE fire (
  id SERIAL PRIMARY KEY,
  image_file BYTEA NOT NULL,
  conv FLOAT NOT NULL,
  detected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);"

# 在数据库中执行SQL命令来创建表
psql -d $DB_NAME -c "$CREATE_TABLE_SQL"
