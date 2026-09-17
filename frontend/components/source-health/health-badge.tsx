interface HealthBadgeProps {
  health: string;
}

export function HealthBadge({ health }: HealthBadgeProps) {
  const normalizedHealth = health.toUpperCase();

  const styles = {
    NORMAL: "bg-green-100 text-green-700",
    WARNING: "bg-yellow-100 text-yellow-700",
    FAILED: "bg-red-100 text-red-700",
  };

  const style =
    styles[normalizedHealth as keyof typeof styles] ??
    "bg-gray-100 text-gray-700";

  return (
    <span
      className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${style}`}
    >
      {normalizedHealth}
    </span>
  );
}
