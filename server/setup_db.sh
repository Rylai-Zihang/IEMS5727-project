#!/bin/bash

echo "The current user is: $USER"

# 检查postgres
./check_brew_postgres.sh

# 定义数据库参数
DB_NAME="iot"
DB_USER=$USER

# 创建数据库
psql -U $DB_USER -h localhost -c "CREATE DATABASE $DB_NAME;"

# 构建用于创建表的SQL命令
CREATE_TABLE_FIRE_SQL="
CREATE TABLE fire (
  id SERIAL PRIMARY KEY,
  device TEXT NOT NULL,
  image_file BYTEA NOT NULL,
  conv FLOAT NOT NULL,
  detected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);"

CREATE_TABLE_TEMPERATURE_SQL="
CREATE TABLE temperature (
  id SERIAL PRIMARY KEY,
  device TEXT NOT NULL,
  temperature INT NOT NULL,
  detected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);"

# 在数据库中执行SQL命令来创建表
psql -d $DB_NAME -c "$CREATE_TABLE_FIRE_SQL"
psql -d $DB_NAME -c "$CREATE_TABLE_TEMPERATURE_SQL"
