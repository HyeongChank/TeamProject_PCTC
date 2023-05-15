export default function Table(props: any): any {

  const th = props.tableHead.map((item: string) => {
    return <th key={item} className="border border-gray-800 px-5 py-2">{item}</th>
  })

  return (
    <div className="flex flex-col items-center">
      <h1 className="text-3xl font-bold my-10">{props.tableTitle}</h1>
      <table className="border border-gray-800">
        <thead>
          <tr>
            {th}
          </tr>
        </thead>
        <tbody>

        </tbody>
      </table>
    </div>
  );
}