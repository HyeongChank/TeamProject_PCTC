type User = {
  isLogin: boolean,
  user: {
    id: string,
    pw: string,
    name: string,
  }
}

export function createCookie(userData: User) {
  console.log(">> " , userData);
  if (window !== undefined) {
    document.cookie = `id=${userData.user.id}; max-age=3600`;
    document.cookie = `pw=${userData.user.pw}; max-age=3600`;
    document.cookie = `name=${userData.user.name}; max-age=3600`;
    document.cookie = `isLogin=${userData.isLogin}; max-age=3600`;
  }
}