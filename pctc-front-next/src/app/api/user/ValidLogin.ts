export function validLogin(parameters: any, user: any) {
  if (parameters?.id == user?.id && parameters?.pw == user?.pw)
    return true;
  return false;
}