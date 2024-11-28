import { type MRT_Column, type MRT_TableInstance } from '../types';
interface Props<TData extends Record<string, any> = {}> {
    column: MRT_Column<TData>;
    table: MRT_TableInstance<TData>;
}
export declare const MRT_FilterCheckbox: <TData extends Record<string, any> = {}>({ column, table, }: Props<TData>) => import("react/jsx-runtime").JSX.Element;
export {};
