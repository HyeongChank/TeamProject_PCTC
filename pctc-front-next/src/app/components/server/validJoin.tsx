import { createConnection } from "mysql";
import { promisify } from "util";

/**
 * @param userInfo user ID
 * @returns true is User
 * @returns false is not User
 */
export default async function validJoin(userInfo: {
  id: string;
  pw: string;
  name: string;
}) {
  // 유효한 회원가입 요청인가 검증
  let connection = connectionDB(); // DB 커넥션 생성

  connection.connect();

  let query = promisify(connection.query).bind(connection);

  try {
    await query(
      "INSERT INTO USER(`id`,`pw`,`name`) VALUES('" +
        userInfo?.id +
        "','" +
        userInfo?.pw +
        "','" +
        userInfo?.name +
        "')"
    );
  } catch (err) {
    console.error("SQL error: ", err);
    return false;
  } finally {
    connection.end(); // DB 접속 종료
  }

  return true;
}

function connectionDB() {
  return createConnection({
    // mysql 접속 설정
    host: process.env.DB_HOST,
    port: 3306,
    user: process.env.DB_ID,
    password: process.env.DB_PW,
    database: process.env.DB_NAME,
  }); // DB 커넥션 생성
}
