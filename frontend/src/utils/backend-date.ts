const IST_TIME_ZONE = "Asia/Kolkata";

function normalizeBackendTimestamp(
  value: string | Date,
): string {
  if (value instanceof Date) {
    return value.toISOString();
  }

  let normalized = value.trim();

  if (!normalized) {
    return "";
  }

  normalized = normalized.replace(" ", "T");

  const hasTimezone =
    /(?:Z|[+-]\d{2}:\d{2})$/i.test(normalized);

  if (!hasTimezone) {
    normalized += "Z";
  }

  return normalized;
}

export function parseBackendDate(
  value: string | Date,
): Date {
  return new Date(
    normalizeBackendTimestamp(value),
  );
}

export function formatBackendDateTime(
  value: string | Date,
): string {
  const date = parseBackendDate(value);

  if (Number.isNaN(date.getTime())) {
    return "";
  }

  return date.toLocaleString("en-IN", {
    timeZone: IST_TIME_ZONE,
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: true,
  });
}

export function formatBackendDate(
  value: string | Date,
): string {
  const date = parseBackendDate(value);

  if (Number.isNaN(date.getTime())) {
    return "";
  }

  return date.toLocaleDateString("en-IN", {
    timeZone: IST_TIME_ZONE,
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}
