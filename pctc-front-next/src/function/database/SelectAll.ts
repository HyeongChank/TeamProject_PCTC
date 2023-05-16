import { promisify } from "util";
import { connectionDB } from "./ConnectionDB";

export async function selectAll(tableName: string){
  const connection = connectionDB();
  let resultSet = null;

  connection.connect();

  let query = promisify(connection.query).bind(connection);

  try {
    resultSet = await query(`SELECT * FROM ${tableName}`)
    resultSet = resultSet ?? {};
  } catch (err) {
    console.error('SQL error: ', err);
    return;
  } finally {
    connection.end(); // DB 접속 종료
  }

  return resultSet;
}