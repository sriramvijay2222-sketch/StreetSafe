export type Duplicate = {incident_id:string;category:string;latitude:number;longitude:number;status:string};
export type Report = { incident_id:string; category:string; title:string; description:string; severity:string; priority_score:number; priority_label:string; category_weight:number; severity_points:number; latitude:number; longitude:number; status:string; is_demo:boolean; created_at:string; possible_duplicate_ids:string[]; possible_duplicates:Duplicate[] };
export type Stats = {total:number;open:number;high_priority:number;resolved:number};
export type StatusHistory = {previous_status:string;new_status:string;note:string|null;changed_at:string};
export type ReportDraft = {category:string;title:string;description:string;severity:string;latitude:number;longitude:number};
export const categories=['open drain','flooding','exposed electrical wire','broken streetlight','unsafe crossing','other'];
export const statuses=['submitted','under review','in progress','resolved','rejected'];
