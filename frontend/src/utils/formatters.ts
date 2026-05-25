export function formatCurrency(amount: number, currency = "EUR"): string {
  return new Intl.NumberFormat("en-US", { style: "currency", currency }).format(amount);
}

export function formatPercent(value: number): string {
  return (value * 100).toFixed(1) + "%";
}

export function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString("en-US", {
    year: "numeric", month: "short", day: "numeric",
  });
}
