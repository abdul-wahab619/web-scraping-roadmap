interface StatusBadgeProps {
  status: string;
}

export function StatusBadge({ status }: StatusBadgeProps) {
  const normalizedStatus = status.toUpperCase();

  const styles = {
    FINISHED: "bg-green-100 text-green-700",
    FAILED: "bg-red-100 text-red-700",
    RUNNING: "bg-blue-100 text-blue-700",
  };

  const style =
    styles[normalizedStatus as keyof typeof styles] ??
    "bg-gray-100 text-gray-700";

  return (
    <span
      className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold`}
    >
      <span className={style}>{normalizedStatus}</span>
    </span>
  );
}
