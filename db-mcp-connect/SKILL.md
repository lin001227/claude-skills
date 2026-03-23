---
name: db-mcp-connect
description: 数据库 MCP 连接助手，支持一键配置 MySQL、PostgreSQL、SQL Server、SQLite、MongoDB、Redis 等主流数据库的 MCP 服务器，自动写入配置文件并验证连接。当用户想要连接数据库、配置数据库MCP、添加数据库连接时触发。
---

# db-mcp-connect 技能

## 概述

`db-mcp-connect` 是一个数据库 MCP 连接配置助手，支持主流数据库的 MCP Server 自动配置。用户只需提供连接信息，技能自动生成配置、写入 `.claude.json`，并引导验证连接。

## 触发条件

当用户表达以下意图时触发：

- "连接数据库"
- "配置数据库 MCP"
- "添加数据库连接"
- "连接 MySQL / PostgreSQL / SQL Server / SQLite / MongoDB / Redis"
- "数据库 MCP 配置"
- "让 Claude 访问数据库"
- 或任何与数据库 MCP 配置相关的请求

## 支持的数据库

| 数据库 | MCP 包 | 所需信息 |
|--------|--------|----------|
| **PostgreSQL** | `@modelcontextprotocol/server-postgres` | host, port, database, user, password |
| **MySQL** | `mcp-server-mysql` | host, port, database, user, password |
| **SQL Server** | `mssql-mcp` | host, port, database, user, password |
| **SQLite** | `@modelcontextprotocol/server-sqlite` | 文件路径 |
| **MongoDB** | `@modelcontextprotocol/server-mongodb` | connection string |
| **Redis** | `mcp-server-redis` | host, port, password (可选) |

## 执行步骤

### 第一步：收集信息

向用户询问：
1. **数据库类型**：MySQL / PostgreSQL / SQL Server / SQLite / MongoDB / Redis
2. **连接信息**（根据类型询问对应字段）：
   - 关系型数据库：host、port、database、user、password
   - SQLite：数据库文件的完整路径
   - MongoDB：连接字符串（如 `mongodb://user:pass@host:27017/db`）
   - Redis：host、port、password（可选）
3. **配置名称**（可选，默认用数据库类型名称，如 `mysql`、`postgres`）
4. **配置范围**：用户级（`~/.claude.json`，所有项目生效）或项目级（`.mcp.json`，仅当前项目）

### 第二步：检查前置条件

```bash
# 检查 Node.js 是否安装
node --version

# 检查 npx 是否可用
npx --version
```

若未安装，提示用户先安装 Node.js（https://nodejs.org）。

### 第三步：生成配置

根据数据库类型生成对应的 MCP 配置：

#### PostgreSQL
```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://USER:PASSWORD@HOST:PORT/DATABASE"]
    }
  }
}
```

#### MySQL
```json
{
  "mcpServers": {
    "mysql": {
      "command": "npx",
      "args": ["-y", "mcp-server-mysql"],
      "env": {
        "MYSQL_HOST": "HOST",
        "MYSQL_PORT": "3306",
        "MYSQL_DATABASE": "DATABASE",
        "MYSQL_USER": "USER",
        "MYSQL_PASSWORD": "PASSWORD"
      }
    }
  }
}
```

#### SQL Server
```json
{
  "mcpServers": {
    "sqlserver": {
      "command": "npx",
      "args": ["-y", "mssql-mcp"],
      "env": {
        "DB_SERVER": "HOST",
        "DB_PORT": "1433",
        "DB_DATABASE": "DATABASE",
        "DB_USER": "USER",
        "DB_PASSWORD": "PASSWORD",
        "DB_ENCRYPT": "false",
        "DB_TRUST_SERVER_CERTIFICATE": "true"
      }
    }
  }
}
```

#### SQLite
```json
{
  "mcpServers": {
    "sqlite": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sqlite", "--db-path", "/path/to/database.db"]
    }
  }
}
```

#### MongoDB
```json
{
  "mcpServers": {
    "mongodb": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-mongodb", "MONGODB_CONNECTION_STRING"]
    }
  }
}
```

#### Redis
```json
{
  "mcpServers": {
    "redis": {
      "command": "npx",
      "args": ["-y", "mcp-server-redis"],
      "env": {
        "REDIS_HOST": "HOST",
        "REDIS_PORT": "6379",
        "REDIS_PASSWORD": "PASSWORD"
      }
    }
  }
}
```

### 第四步：写入配置文件

**用户级配置**（`~/.claude.json`）：
- 读取现有 `~/.claude.json` 内容（若不存在则创建）
- 合并新的 `mcpServers` 配置（不覆盖已有配置）
- 写回文件

**项目级配置**（`.mcp.json`）：
- 在当前工作目录创建或更新 `.mcp.json`

写入前展示预览，等待用户确认后执行。

### 第五步：验证连接

配置写入后，指导用户验证：

```
在 VSCode 的 Claude Code 聊天框中输入：
/mcp

查看数据库服务器是否显示为"已连接"状态。
```

若连接失败，常见排查项：
- 检查防火墙/端口是否开放
- 确认用户名密码是否正确
- SQL Server 需开启 TCP/IP 协议
- Windows 环境下使用 `cmd /c npx` 包装命令

### 第六步：使用示例

连接成功后，告知用户可以直接用自然语言操作数据库，例如：
- "查询 users 表的前10条数据"
- "显示所有表的结构"
- "统计订单表中今天的订单数量"

## Windows 环境特殊处理

Windows 下 `npx` 命令需要通过 `cmd /c` 包装才能正常工作：

```json
{
  "command": "cmd",
  "args": ["/c", "npx", "-y", "mcp-server-mysql"],
  "env": { ... }
}
```

技能执行时自动检测 Windows 环境并应用此配置。

## 安全注意事项

- 密码以明文存储在配置文件中，建议：
  - 使用低权限的只读数据库账户
  - 不要将包含密码的配置文件提交到 Git
  - 项目级 `.mcp.json` 应加入 `.gitignore`
- 执行前会展示完整配置供用户确认，不会自动写入

## 示例对话

```
用户: 帮我连接 MySQL 数据库

技能: 请提供以下信息：
1. 主机地址（默认 localhost）
2. 端口（默认 3306）
3. 数据库名称
4. 用户名
5. 密码
6. 配置范围：用户级还是项目级？

用户: localhost, 3306, mydb, root, 123456, 用户级

技能: 已生成配置，预览如下：[展示配置]
确认写入 ~/.claude.json？

用户: 确认

技能: ✓ 配置已写入 ~/.claude.json
请在 Claude Code 中输入 /mcp 验证连接状态。
```
