'use client'

export default function Table({tableTitle, tableHead, tableBodyJSON}: any): any {
  
  const th = tableHead.map((item: string) => {
    return <th key={item} className="border border-gray-800 px-5 py-2">{item}</th>
  })

  let tableBody: any[] = [];

  for (let [key, value] of Object.entries(tableBodyJSON ?? {})) {
    let tableRow = [];
    tableRow.push(<td className="border border-gray-800 text-center p-1">{key}</td>);

    for(let [key_, item] of Object.entries(value ?? {})){
      tableRow.push(<td key={key_} className="border border-gray-800 text-center p-1">{item}</td>);
    }

    tableBody.push([<tr key={key}>{...tableRow}</tr>]);
  }


  return (
    <div className="flex flex-col items-center">
      <h1 className="text-3xl font-bold my-10">{tableTitle}</h1>
      <table className="border border-gray-800 w-3/4 mb-20">
        <thead>
          <tr>
            {th}
          </tr>
        </thead>
        <tbody>
          {tableBody}
        </tbody>
      </table>
    </div>
  );
}