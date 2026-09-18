# PostgreSQL 실습

기존 실습 SQL, DBeaver에 저장한 SQL, DB 실행 및 백업 방법을 함께 보관합니다.

## 2026-09-07 확인 상태

- DBeaver 저장 연결: `localhost:5432/postgres`.
- Windows PostgreSQL 18 서비스가 5432 포트를 사용하고 있습니다. 화면에 보이는 실습 DB는 이 연결입니다.
- 별도로 실행 중인 Docker `postgres-db`는 PostgreSQL 18.6이며, 내부 `postgres` DB의 사용자 테이블은 0개였습니다.
- 사용자 화면에는 public 스키마에 brands, categories, club_members, customers, items, members, order_items, orders, products, staffs, stocks, stores 총 12개 테이블이 보입니다. 서버 쿼리를 통한 구조 및 행 수 확인은 아직 수행하지 못했습니다.
- **Windows DB 암호 입력이 필요해 실제 DB 덤프와 복원 검증은 아직 완료하지 않았습니다.** Docker의 빈 DB 덤프는 혼동을 피하려고 제거했습니다.
- `practice/2026-09-07_Script.sql`, `practice/2026-09-07_Script-1.sql`은 DBeaver 저장 파일을 그대로 복사했습니다. 편집기의 저장하지 않은 내용은 포함하지 않습니다.
- 기존 루트의 실습 SQL 3개와 원본 Docker DB, Windows DB, DBeaver 파일은 유지했습니다.
- 실습 SQL에는 DROP, DELETE 등 학습 과정이 포함되므로 복원용 초기화 스크립트로 자동 실행하지 않습니다.

## 현재 Windows DB 백업

이 폴더에서 PowerShell로 실행합니다. 암호는 PostgreSQL이 터미널에서 직접 입력받으며 파일에 저장하지 않습니다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\backup.ps1
```

성공하면 `backup/postgres.sql`이 생성됩니다. 실패하면 이전 백업은 유지합니다.
덤프에는 DB 구조와 데이터가 포함되며, 서버 전체 계정과 암호, 소유권과 접근 권한은 제외합니다.
DBeaver에서 SQL 파일을 저장하는 것과 DB 변경을 커밋하는 것은 별개입니다. 백업 전 필요한 변경을 커밋하세요.

## 별도 실습 환경 실행

기존 DB의 5432 포트와 충돌하지 않도록 새 환경은 **5433** 포트를 사용합니다.

```powershell
Copy-Item .env.example .env
# .env를 열어 POSTGRES_PASSWORD를 본인 로컬 암호로 변경
# .env는 Git에서 제외됩니다.
docker compose up -d --wait
```

| DBeaver 연결 항목 | 값 |
|---|---|
| Host | localhost |
| Port | 5433 |
| Database | postgres |
| Username | postgres |
| Password | .env에 설정한 암호 |

## 스냅샷 복원

백업을 생성한 다음, 처음 만든 빈 DB에서 한 번 실행합니다. 기존 테이블이 있는 DB에 반복 실행하는 용도가 아닙니다.

```powershell
docker compose cp ./backup/postgres.sql db:/tmp/ax-study-restore.sql
docker compose exec -T db psql -U postgres -d postgres -v ON_ERROR_STOP=1 --single-transaction -f /tmp/ax-study-restore.sql
```

## 새 Compose 환경에서 백업 갱신

5433 포트의 새 환경으로 실습을 옮긴 뒤에는 다음 명령으로 새 DB를 백업합니다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\backup.ps1 -Port 5433
```

DB 변경이 Git에 자동 반영되지는 않으므로 보관할 시점에 백업을 갱신하세요. 실제 개인정보나 인증정보를 실습 데이터로 넣었다면 Git에 추가하기 전에 제거하세요.

## 종료

```powershell
docker compose down
```

데이터 볼륨은 유지됩니다. `down -v`는 데이터를 삭제하므로 보존할 DB에는 사용하지 않습니다.
