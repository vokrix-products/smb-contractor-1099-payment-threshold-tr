import { TriangleAlert, CircleCheckBig, Clock } from 'lucide-react'

export const labels = [
  {
    value: 'bug',
    label: 'Bug',
  },
  {
    value: 'feature',
    label: 'Feature',
  },
  {
    value: 'documentation',
    label: 'Documentation',
  },
]

// Severity tiers drive badge color. Every status maps to exactly one tier:
//   critical -> red (destructive)   e.g. expired, denied, failed
//   warning  -> amber (warning)     e.g. expiring soon, needs review
//   good     -> green (success)     e.g. valid, approved, done
//   neutral  -> gray (secondary)    e.g. pending, queued, n/a
export type Severity = 'critical' | 'warning' | 'good' | 'neutral' | 'info'

export const severityToBadgeVariant: Record<Severity, 'destructive' | 'warning' | 'success' | 'secondary'> = {
  critical: 'destructive',
  warning: 'warning',
  good: 'success',
  neutral: 'secondary',
  info: 'secondary',
}

// PRODUCT_CUSTOMIZE: replace this list with the real statuses this product
// produces (must match exactly what the backend poller writes to
// records.status). Every status must declare a severity tier above. Default
// values below are generic placeholders only — do not ship as-is.
// __STATUSES_BLOCK_START__
export const statuses: {
  label: string
  value: string
  icon: typeof TriangleAlert
  severity: Severity
}[] = [
  { label: 'W9 Missing', value: 'w9_missing:critical', icon: TriangleAlert, severity: 'critical' as Severity },
  { label: 'W9 Valid', value: 'w9_valid:good', icon: CircleCheckBig, severity: 'good' as Severity },
  { label: 'W9 Expired Stale', value: 'w9_expired_stale:warning', icon: Clock, severity: 'warning' as Severity },
  { label: 'W9 Flagged', value: 'w9_flagged:critical', icon: TriangleAlert, severity: 'critical' as Severity },
  { label: 'W9 Awaiting Signature', value: 'w9_awaiting_signature:warning', icon: Clock, severity: 'warning' as Severity },
  { label: 'W9 Not Verified', value: 'w9_not_verified:warning', icon: Clock, severity: 'warning' as Severity },
  { label: 'Tin Mismatch', value: 'tin_mismatch:critical', icon: TriangleAlert, severity: 'critical' as Severity },
  { label: 'Payment Threshold Approaching', value: 'payment_threshold_approaching:warning', icon: Clock, severity: 'warning' as Severity },
  { label: 'Payment Threshold Crossed', value: 'payment_threshold_crossed:info', icon: Clock, severity: 'info' as Severity },
  { label: 'Over Threshold Without W9', value: 'over_threshold_without_w9:critical', icon: TriangleAlert, severity: 'critical' as Severity },
  { label: 'Backup Withholding Risk', value: 'backup_withholding_risk:critical', icon: TriangleAlert, severity: 'critical' as Severity },
  { label: 'Chase Active', value: 'chase_active:info', icon: Clock, severity: 'info' as Severity },
  { label: 'Chase Overdue', value: 'chase_overdue:warning', icon: Clock, severity: 'warning' as Severity },
  { label: 'Chase Failed', value: 'chase_failed:critical', icon: TriangleAlert, severity: 'critical' as Severity },
  { label: 'Contractor Duplicate', value: 'contractor_duplicate:warning', icon: Clock, severity: 'warning' as Severity },
  { label: 'Contractor Incomplete Data', value: 'contractor_incomplete_data:warning', icon: Clock, severity: 'warning' as Severity },
  { label: 'Non Us Payee', value: 'non_us_payee:info', icon: Clock, severity: 'info' as Severity },
  { label: 'Archived Paid Under Threshold', value: 'archived_paid_under_threshold:good', icon: CircleCheckBig, severity: 'good' as Severity },
  { label: 'Ready To File', value: 'ready_to_file:good', icon: CircleCheckBig, severity: 'good' as Severity },
]
// __STATUSES_BLOCK_END__
