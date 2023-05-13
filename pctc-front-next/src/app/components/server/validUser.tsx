import { createConnection } from "mysql";
import { promisify } from "util";

/**
 * @param userInfo user ID
 * @returns true is User
 * @returns false is not User
 */
export default async function validUser(userInfo: string) {
  // 유효한 회원인가 검증
  let connection = connectionDB() // DB 커넥션 생성
  let user = {};

  connection.connect();

  let query = promisify(connection.query).bind(connection);

  try {
    let resultSet = await query(`SELECT * FROM USER WHERE ID='${userInfo}'`)
    user = resultSet ?? {};
  } catch (err) {
    console.error('SQL error: ', err);
    return;
  } finally {
    connection.end(); // DB 접속 종료
  }

  return user;
}

function connectionDB() {
  return createConnection({  // mysql 접속 설정
    host: process.env.DB_HOST,
    port: 3306,
    user: process.env.DB_ID,
    password: process.env.DB_PW,
    database: process.env.DB_NAME
  }); // DB 커넥션 생성
}