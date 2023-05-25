export function goto(path: string) {
  if (typeof window !== "undefined") {
    if (path === null) path = "/";
    window.location.href = `${path}`;
  }
}
