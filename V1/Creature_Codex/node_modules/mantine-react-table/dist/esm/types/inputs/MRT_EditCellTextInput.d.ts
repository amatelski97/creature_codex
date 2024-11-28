/// <reference types="react" />
import { type MRT_Cell, type MRT_TableInstance } from '../types';
interface Props<TData extends Record<string, any> = {}> {
    cell: MRT_Cell<TData>;
    table: MRT_TableInstance<TData>;
}
export declare const MRT_EditCellTextInput: <TData extends Record<string, any> = {}>({ cell, table, }: Props<TData>) => string | number | boolean | Iterable<import("react").ReactNode> | import("react/jsx-runtime").JSX.Element | null | undefined;
export {};
