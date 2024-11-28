/// <reference types="react" />
import { type MRT_Cell, type MRT_TableInstance } from '../types';
interface Props<TData extends Record<string, any> = {}> {
    cell: MRT_Cell<TData>;
    table: MRT_TableInstance<TData>;
}
export declare const MRT_TableBodyCellValue: <TData extends Record<string, any> = {}>({ cell, table, }: Props<TData>) => import("react").ReactNode;
export {};
