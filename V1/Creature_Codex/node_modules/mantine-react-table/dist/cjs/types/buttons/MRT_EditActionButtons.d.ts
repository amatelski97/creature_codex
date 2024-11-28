import { type MRT_Row, type MRT_TableInstance } from '../types';
interface Props<TData extends Record<string, any> = {}> {
    row: MRT_Row<TData>;
    table: MRT_TableInstance<TData>;
    variant?: 'icon' | 'text';
}
export declare const MRT_EditActionButtons: <TData extends Record<string, any> = {}>({ row, table, variant, }: Props<TData>) => import("react/jsx-runtime").JSX.Element;
export {};
