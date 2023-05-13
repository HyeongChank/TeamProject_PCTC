

export default function CreateTable({ cols }) {

  const rows = 10; // 임의로 부여한 숫자(실제 데이터 필요)
  const rendering = [];
  const colsList = Array.from({length: cols}, () => "");

  rendering.push(<tr>
    <th>No</th>
    <th>터미널</th>
    <th>선석</th>
    <th>모선항차<br />입항차/출항차</th>
    <th>연도</th>
    <th>선박명 Bitt(M)	</th>
    <th>접안(예정)일시</th>
    <th>반입마감일시</th>
    <th>출항(예정)일시</th>
    <th>선사</th>
    <th>양하수량(VAN)</th>
    <th>적하수량(VAN)</th>
    <th>Shift</th>
    </tr>)

  for (let i = 1; i <= rows; i++) {
    rendering.push(<tr key={i}>{colsList.map((data, index) => <td className="table-td" key={i + "-" + index}>실제 내용이 들어가야</td>)}</tr>)
  }

  return (
    <div className="menuTableArea">
      <table border={1} style={{borderCollapse:'collapse'}}>
        {rendering}
      </table>
    </div>
  );
}