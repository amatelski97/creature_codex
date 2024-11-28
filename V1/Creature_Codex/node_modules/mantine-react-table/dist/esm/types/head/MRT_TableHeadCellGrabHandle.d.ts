import { type RefObject } from 'react';
import { type MRT_Column, type MRT_TableInstance } from '../types';
interface Props<TData extends Record<string, any> = {}> {
    column: MRT_Column<TData>;
    table: MRT_TableInstance<TData>;
    tableHeadCellRef: RefObject<HTMLTableCellElement>;
}
export declare const MRT_TableHeadCellGrabHandle: <TData extends Record<string, any> = {}>({ column, table, tableHeadCellRef, }: Props<TData>) => import("react/jsx-runtime").JSX.Element;
export {};
