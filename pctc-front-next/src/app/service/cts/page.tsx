import Table from "@/app/components/server/Table";

export default function CTS() {
  return (
    <>
      <Table tableTitle={"컨테이너터미널 반출입현황"} tableHead={["번호","터미널","모선코드","수출입구분","호출부호","입항횟수","시설코드","TEU","입출항일자","선사/대리점"]} />
    </>
  );
}