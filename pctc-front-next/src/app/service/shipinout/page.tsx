import Table from "@/app/components/server/Table";

export default function CTAS() {
  return (
    <>
      <Table tableTitle={"선박입출항 예정정보"} tableHead={["번호", "터미널", "재박장소", "호출부호", "선명", "총 톤수", "길이", "입항횟수", "흘수", "구분/목적", "접안(투묘)시간", "입항일시", "출항 예정 일시", "선사/대리점"]} />
    </>
  );
}