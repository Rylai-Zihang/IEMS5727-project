#!/bin/bash


install_homebrew() {
    echo "installing Homebrew ... "
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
}

install_postgresql(){
    echo "installing PostgreSQL ... "
    # 安装postgresql
    brew install postgresql@15

    # 设置环境
    echo 'export PATH="/usr/local/opt/postgresql@15/bin:$PATH"' >> ~/.zshrc
    source  ~/.zshrc
}

running_postgres_service(){
    echo "starting postgresql service ..."
    brew services start postgresql@15
}


# 检查 Homebrew 是否安装
if which brew > /dev/null; then
    echo "Homebrew is installed."
    # 检查 PostgreSQL 是否安装
    if brew list postgresql@15 > /dev/null 2>&1; then
        echo "PostgreSQL is installed."
        # 检查 PostgreSQL 服务是否正在运行
        if brew services list | grep postgresql | grep started > /dev/null; then
            echo "PostgreSQL service is running."
        else
            echo "PostgreSQL service is not running."
            running_postgres_service
        fi
    else
        echo "PostgreSQL is not installed."
        install_postgresql
    fi
else
    echo "Homebrew is not installed."
    install_homebrew
    install_postgresql
fi
