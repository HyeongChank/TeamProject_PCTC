export default function BASLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <div className="flex justify-center mt-10">{children}</div>;
}