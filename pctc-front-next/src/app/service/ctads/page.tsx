import Table from "@/app/components/server/Table";

export default function CTADS() {
  return (
    <>
      <Table tableTitle={"컨테이너터미널 입출항현황"} tableHead={["번호","터미널","구분","호출부호","입항목적","입항횟수","선사/대리점","선박명","국적","총 톤수","입항일시","출항일시","전 출항지", "차항지"]} />
    </>
  );
}