import { connectionDB } from "@/function/database/ConnectionDB";
import { promisify } from "util";

interface QueryResult {
  id: string,
  pw: string,
  name: string
}

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
    let [resultSet] = await query(`SELECT * FROM USER WHERE ID='${userInfo}'`) as QueryResult[]
    user = {id: resultSet.id, pw: resultSet.pw, name: resultSet.name}
  } catch (err) {
    console.error('SQL error: ', err);
    return;
  } finally {
    connection.end(); // DB 접속 종료
  }

  return user;
}