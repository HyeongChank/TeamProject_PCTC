export type ShipDataValue = {
  arrival: string;
  departure: string;
  id: string;
  loading: string;
  name: string;
  portorder: string;
  progress: string;
  unloading: string;
}

export async function makeShipDataValue(){
  const res = await fetch("http://10.125.121.222:8080/port");
  const result = await res.json();
  return result as ShipDataValue[];
}