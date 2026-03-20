# Sample Python Web App (Flask + MongoDB)

App mẫu này dùng để bạn test deploy AWS và kiểm tra các tính năng MongoDB (replica set/sharding qua `mongos`).

## 1) Chạy local (không Docker)

```bash
cd app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
export $(grep -v '^#' .env | xargs)
python src/main.py
```

Test nhanh:

```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name":"test-item","value":123}'
curl http://localhost:8000/items
```

## 2) Chạy bằng Docker

```bash
cd app
docker build -t nt132-sample-app .
docker run --rm -p 8000:8000 \
  -e MONGO_URI='mongodb://admin:admin123@host.docker.internal:27017/?authSource=admin' \
  -e MONGO_DB='nt132_app' \
  nt132-sample-app
```

Nếu chạy Linux và `host.docker.internal` không hoạt động, thay bằng IP host hoặc chạy chung network phù hợp.

## 3) Endpoint chính

- `GET /` thông tin service
- `GET /health` ping MongoDB
- `POST /items` tạo item (`name` bắt buộc)
- `GET /items?limit=20` lấy danh sách item
- `GET /items/<id>` lấy item theo id
- `DELETE /items/<id>` xoá item theo id

## 4) Deploy AWS (gợi ý nhanh: ECS Fargate)

1. Tạo ECR repository, ví dụ: `nt132-sample-app`
2. Build và push image lên ECR
3. Tạo ECS Task Definition (container port `8000`)
4. Truyền biến môi trường:
   - `MONGO_URI`
   - `MONGO_DB`
   - `MONGO_COLLECTION`
5. Tạo ECS Service + ALB để public endpoint
6. Health check dùng path: `/health`

> Nếu MongoDB nằm ngoài AWS hoặc chạy Atlas, chỉ cần đổi `MONGO_URI` tương ứng.
