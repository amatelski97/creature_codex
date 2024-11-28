import { type MRT_ColumnDef, type MRT_ColumnOrderState, type MRT_GroupingState, type MRT_DefinedTableOptions, type MRT_Row } from '../types';
interface Params<TData extends Record<string, any> = {}> {
    creatingRow: MRT_Row<TData> | null;
    columnOrder: MRT_ColumnOrderState;
    grouping: MRT_GroupingState;
    tableOptions: MRT_DefinedTableOptions<TData>;
}
export declare const useMRT_DisplayColumns: <TData extends Record<string, any> = {}>({ creatingRow, columnOrder, grouping, tableOptions, }: Params<TData>) => MRT_ColumnDef<TData>[];
export {};
