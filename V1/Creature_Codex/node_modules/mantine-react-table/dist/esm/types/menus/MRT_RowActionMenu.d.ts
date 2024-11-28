import { type MouseEvent } from 'react';
import { type MRT_Row, type MRT_TableInstance } from '../types';
interface Props<TData extends Record<string, any> = {}> {
    handleEdit: (event: MouseEvent) => void;
    row: MRT_Row<TData>;
    table: MRT_TableInstance<TData>;
}
export declare const MRT_RowActionMenu: <TData extends Record<string, any> = {}>({ handleEdit, row, table, }: Props<TData>) => import("react/jsx-runtime").JSX.Element;
export {};
