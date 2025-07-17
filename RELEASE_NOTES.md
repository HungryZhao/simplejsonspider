# Release 发布说明

## 自动化发布系统已配置完成

### 已完成的配置：

1. **GitHub Actions 工作流**：
   - `.github/workflows/ci.yml` - 持续集成，在每次推送时运行测试
   - `.github/workflows/release.yml` - 发布工作流，在推送 tag 时自动发布

2. **版本管理**：
   - 使用 `setuptools_scm` 自动从 git tag 生成版本号
   - 配置了 `pyproject.toml` 现代化构建系统
   - 更新了 `setup.py` 以支持自动版本管理

3. **测试系统**：
   - 支持 Python 3.8-3.11 的矩阵测试
   - 19 个测试用例全部通过

4. **发布工具**：
   - `release.py` - 本地测试和发布脚本
   - `MANIFEST.in` - 包含文件清单
   - 完整的包构建和测试流程

### 如何创建新的发布：

#### 方法 1：使用 GitHub（推荐）

1. **提交更改**：
   ```bash
   git add .
   git commit -m "Prepare release v0.3.0"
   git push
   ```

2. **创建并推送 tag**：
   ```bash
   git tag v0.3.0
   git push origin v0.3.0
   ```

3. **自动化流程**：
   - GitHub Actions 会自动运行测试
   - 构建包 (.whl 和 .tar.gz)
   - 创建 GitHub Release
   - 上传到 PyPI（需要配置 PYPI_TOKEN）

#### 方法 2：本地发布

```bash
# 运行本地发布脚本
python release.py
```

### 配置 PyPI 自动发布：

1. 在 [PyPI](https://pypi.org/) 创建 API Token
2. 在 GitHub 仓库的 Settings > Secrets and variables > Actions 中添加：
   - Name: `PYPI_TOKEN`
   - Value: `pypi-YOUR_TOKEN_HERE`

### 用户安装方式：

```bash
# 从 PyPI 安装
pip install simplejsonspider

# 从 GitHub 安装最新版本
pip install git+https://github.com/HungryZhao/simplejsonspider.git

# 从 GitHub Release 安装指定版本
pip install https://github.com/HungryZhao/simplejsonspider/releases/download/v0.3.0/simplejsonspider-0.3.0-py3-none-any.whl
```

### 当前状态：

- ✅ 代码已准备好发布
- ✅ 测试全部通过
- ✅ 包构建成功
- ✅ GitHub Actions 配置完成
- ✅自动发布到 PyPI
- ⏳ 等待创建第一个 tag 来触发发布

### 下一步：

1. 检查并提交所有更改
2. 创建 v0.3.0 tag
3. 推送 tag 到 GitHub
4. 观察 GitHub Actions 自动发布流程
