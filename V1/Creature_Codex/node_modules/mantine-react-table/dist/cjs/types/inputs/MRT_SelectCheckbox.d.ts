import { type MRT_Row, type MRT_TableInstance } from '../types';
interface Props<TData extends Record<string, any> = {}> {
    row?: MRT_Row<TData>;
    selectAll?: boolean;
    table: MRT_TableInstance<TData>;
}
export declare const MRT_SelectCheckbox: <TData extends Record<string, any> = {}>({ row, selectAll, table, }: Props<TData>) => import("react/jsx-runtime").JSX.Element;
export {};
