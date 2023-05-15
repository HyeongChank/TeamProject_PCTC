import Table from "@/app/components/server/Table";

export default function SWS() {
  return (
    <>
      <Table tableTitle={"본선작업현황"} tableHead={["번호","터미널","선석","작업QC번호","모선항차","작업시작시간","작업완료시간","양하작업물량-작업량","양하작업물량-완료량","양하작업물량-잔여량","적하작업물량-작업량","적하작업물량-완료량","적하작업물량-잔여량","합계-작업량","합계-완료량","합계-잔여량"]} />
    </>
  );
}