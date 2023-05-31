import Table from "@/app/components/server/Table";

export default function CTS() {
  return (
    <>
      <Table tableTitle={"공컨테이너 현황(신선대)"} tableHead={["번호","터미널","모선코드","수출입구분","호출부호","입항횟수","시설코드","TEU","입출항일자","선사/대리점"]} />
    </>
  );
}