import { createConnection } from "mysql";

export function connectionDB() {
  return createConnection({  // mysql 접속 설정
    host: process.env.DB_HOST,
    port: 3306,
    user: process.env.DB_ID,
    password: process.env.DB_PW,
    database: process.env.DB_NAME
  }); // DB 커넥션 생성
}