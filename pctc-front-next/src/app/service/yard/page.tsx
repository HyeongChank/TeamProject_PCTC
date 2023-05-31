import Table from "@/app/components/server/Table";
import { selectAll } from "@/function/database/SelectAll";

export default async function BAS() {

  const tableName = "assignship";

  let resultSet = await selectAll(tableName);

  return (
    <>
      <Table 
        tableTitle={"야드 작업 현황"} 
        tableHead={["번호", "터미널", "선석", "모선항차", "년도", "선박명 Bitt(M)", "접안(예정)일시", "반입마감일시", "출항(예정)일시", "선사", "양하수량(VAN)", "적하수량(VAN)", "Shift"]} 
        tableBodyJSON={resultSet} />
    </>
  );
}