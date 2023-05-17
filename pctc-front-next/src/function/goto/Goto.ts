export function goto(path: string){
  if(path === null)
    path = "/";
  window.location.href = `${path}`;
}