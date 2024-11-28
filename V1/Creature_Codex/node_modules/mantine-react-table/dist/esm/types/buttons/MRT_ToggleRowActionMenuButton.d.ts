import { type MRT_Cell, type MRT_Row, type MRT_TableInstance } from '../types';
interface Props<TData extends Record<string, any> = {}> {
    cell: MRT_Cell<TData>;
    row: MRT_Row<TData>;
    table: MRT_TableInstance<TData>;
}
export declare const MRT_ToggleRowActionMenuButton: <TData extends Record<string, any> = {}>({ cell, row, table, }: Props<TData>) => import("react/jsx-runtime").JSX.Element;
export {};
