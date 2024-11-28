import { type RefObject } from 'react';
import { type MRT_Row, type MRT_TableInstance } from '../types';
interface Props<TData extends Record<string, any> = {}> {
    row: MRT_Row<TData>;
    rowRef: RefObject<HTMLTableRowElement>;
    table: MRT_TableInstance<TData>;
}
export declare const MRT_TableBodyRowGrabHandle: <TData extends Record<string, any> = {}>({ row, rowRef, table, }: Props<TData>) => import("react/jsx-runtime").JSX.Element;
export {};
