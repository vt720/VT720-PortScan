# 简易多线程并发式端口扫描器

[![Python](https://img.shields.io/badge/Python-3.14+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

一个采用多线程并发方式,对指定 IP / 域名和指定端口进行探测的简易端口扫描脚本。

> ⚠️ 本工具仅供网络安全学习、授权渗透测试和自有资产自查使用。请勿用于任何未经授权的扫描行为。

## ✨ 功能特性

- 🚀 **多线程并发**:可自定义并发数量,扫描速度快
- 🎯 **灵活的目标指定**:支持 IP 地址和域名
- 🔢 **多种端口输入方式**:单个端口 / 多个端口 / 端口范围
- 🔍 **服务指纹识别**:可选开启 banner 抓取,识别开放端口的服务信息
- ⏱️ **超时控制**:自定义连接超时时间
- 📁 **结果导出**:可将扫描结果以 JSON 格式保存到本地

## 📦 环境要求

- Python 3.14+(低版本理论兼容,但未经测试)
- **无需安装第三方依赖**,仅使用 Python 标准库

## 🔧 安装

```bash
# 1. 克隆仓库
git clone https://github.com/vt720/port-scanner.git
cd port-scanner

# 2. 直接运行(无需安装任何第三方依赖)
python port-scanner.py -t 192.168.1.1 -p 80
```

## 🚀 使用方法

```bash
python port-scanner.py -t <目标> [选项]
```

### 参数说明

| 参数 | 说明 | 是否必填 | 默认值 |
|------|------|---------|--------|
| `-t, --target` | 目标 IP 或域名 | ✅ | - |
| `-p, --ports` | 端口。支持单个端口、多个端口(逗号分隔)、端口范围(起始-终点) | ❌ | 默认端口 |
| `-c, --concurrency` | 并发数量上限 | ❌ | 脚本内置默认值 |
| `--timeout` | 连接超时时间(秒) | ❌ | 脚本内置默认值 |
| `-b, --banner` | 开启后尝试抓取服务指纹信息 | ❌ | 关闭 |
| `-o, --output` | 以 JSON 格式保存结果到 `scan_result.json` | ❌ | 关闭 |

### 使用示例

**1️⃣ 扫描单个端口**
```bash
python port-scanner.py -t 192.168.1.1 -p 80
```

**2️⃣ 扫描多个指定端口**
```bash
python port-scanner.py -t 192.168.1.1 -p 80,3306,8080,443
```

**3️⃣ 扫描端口范围**
```bash
python port-scanner.py -t 192.168.1.1 -p 720-888
```

**4️⃣ 扫描域名(使用默认端口)**
```bash
python port-scanner.py -t example.com
```

**5️⃣ 自定义并发数 + 超时时间**
```bash
python port-scanner.py -t 192.168.1.1 -p 1-1000 -c 200 --timeout 2
```

**6️⃣ 抓取服务指纹 + 保存结果**
```bash
python port-scanner.py -t 192.168.1.1 -p 1-1000 -b -o
```

## 📤 输出说明

- **终端输出**:实时显示开放端口。携带 `-b` 时附带服务指纹信息。
- **文件输出**:携带 `-o` 时,结果保存为当前目录下的 `scan_result.json`,结构大致如下:

```json
{
    "scan_info": {
        "target": "192.168.56.11",
        "ip": "192.168.56.11",
        "port_count_scanned": 1,
        "concurrency": 50,
        "timeout_sec": 1.5
    },
    "results": [
        {
            "port": "22",
            "state": "目标端口开启",
            "banner": "端口回复:SSH-2.0-OpenSSH_10.2p1 Debian-2\r\n"
        }
    ]
}
```

## 🗂️ 项目结构

```text
port-scanner/
├── port-scanner.py      # 主程序
├── README.md            # 项目说明
├── LICENSE              # MIT 开源协议
├── requirements.txt     # 依赖清单
├── .gitignore           # Git 忽略规则
└── scan_result.json     # 扫描结果(运行后生成)
```

## ⚠️ 免责声明

1. 本工具仅供**网络安全学习、授权渗透测试**和**自有资产自查**使用。
2. 使用者必须确保对扫描目标拥有**合法授权**,否则一切后果自负。
3. 严禁将本工具用于任何未经授权的扫描、攻击或非法用途。
4. 因使用本工具产生的一切法律责任,由使用者自行承担,与作者无关。

## 📄 License

本项目基于 [MIT License](LICENSE) 开源。
