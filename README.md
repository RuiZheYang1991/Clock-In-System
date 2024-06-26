
# My Flask Project
- 這是一個簡單的打卡專案，使用Python語言、Flask框架、MVC架構、Restful API風格撰寫。
- 整體架構使用 ` Nginx` + `uwsgi` + `Flask` + `Mysql` ， 已部署至AWS。
- API電子文件使用 `SWAGGER 1.0` 。
- 後台使用 `falsk_admin`

## 環境需求:
- Docker
- Docker Compose

## 配置:
1. 確保 Docker 和 Docker Compose 已經在你的系統上安裝。
2. 根據你的環境或需求修改 `.env` 文件中的設置。

## 部署:
1. 在專案的根目錄下運行以下命令:
```
docker-compose up -d
```
將會建立並啟動所需的所有容器。

2. 應用程序透過Nginx反向代理，現在應該在指定的端口上運行。你可以通過 `http://localhost:4000` 來訪問它。

## 注意:
- 如果你在 `.env` 文件中更改了任何設置，請確保重新啟動 Docker Compose 以應用這些更改。
- 如果你執行本地部署，資料庫並不會有員工資料及打卡資料，可以透過後台新增員工，並使用api電子文件的Try it 來打卡。
