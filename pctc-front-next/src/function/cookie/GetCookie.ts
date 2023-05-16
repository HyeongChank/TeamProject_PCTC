import { cookies } from 'next/headers'

export function getCookie(){
  return { name: cookies().get('name')?.value, islogin: cookies().get('islogin')?.value };
}