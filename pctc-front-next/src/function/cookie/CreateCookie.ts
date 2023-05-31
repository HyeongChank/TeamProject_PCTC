type User = {
  isLogin: boolean,
  user: {
    username: string,
    token: string,
  }
}

export function createCookie(userData: User) {
  if (typeof window !== "undefined") {
    document.cookie = `username=${userData.user.username}; max-age=3600`;
    document.cookie = `token=${userData.user.token}; max-age=3600`;
    document.cookie = `isLogin=${userData.isLogin}; max-age=3600`;
  }
}